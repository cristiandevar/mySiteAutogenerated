from decimal import Decimal

from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

# TODO: reemplazar "tu_app" por el nombre real de la app donde están tus modelos.
from core.models import Categoria, Marca, Proveedor, Producto
from .listados import generar_listado_excel, generar_listado_pdf
from .permissions import EsAdministrador
from .serializers import (
    CategoriaSerializer,
    MarcaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    UsuarioActualSerializer,
    ActualizacionMasivaSerializer,
    GenerarListadoSerializer,
)


class CatalogoMaestroViewSet(viewsets.ModelViewSet):
    """
    Base común para Categoría/Marca/Proveedor.

    Cualquier usuario autenticado puede listar/ver (un Operador los necesita
    igual para los filtros de Productos y Actualización masiva), pero solo
    Administrador puede crear, editar o dar de baja.

    "Eliminar" es en realidad una baja lógica (activo=False), nunca un
    borrado físico: Producto los referencia con on_delete=PROTECT, así que
    un DELETE real fallaría apenas hubiera algún producto asociado.
    """

    def get_queryset(self):
        qs = self.queryset.model.objects.filter(activo=True)
        if texto := self.request.query_params.get("search"):
            qs = qs.filter(nombre__icontains=texto)
        return qs.order_by("nombre")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), EsAdministrador()]

    def destroy(self, request, *args, **kwargs):
        instancia = self.get_object()

        # Regla de negocio: no se puede dar de baja si tiene al menos un
        # producto activo con stock > 0 asociado.
        tiene_stock = instancia.productos.filter(activo=True, stock__gt=0).exists()
        if tiene_stock:
            return Response(
                {
                    "detalle": (
                        "No se puede eliminar: existen productos activos con "
                        "stock mayor a cero asociados."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        # Si no tiene productos activos con stock > 0 (puede tener productos
        # activos con stock 0), se da de baja también a esos productos para
        # no dejarlos huérfanos de una marca/categoría/proveedor inactivo.
        instancia.productos.filter(activo=True).update(activo=False)
        instancia.activo = False
        instancia.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriaViewSet(CatalogoMaestroViewSet):
    queryset = Categoria.objects.filter(activo=True)
    serializer_class = CategoriaSerializer


class MarcaViewSet(CatalogoMaestroViewSet):
    queryset = Marca.objects.filter(activo=True)
    serializer_class = MarcaSerializer


class ProveedorViewSet(CatalogoMaestroViewSet):
    queryset = Proveedor.objects.filter(activo=True)
    serializer_class = ProveedorSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    """
    CRUD de productos. Filtrable con query params, por ejemplo:
    /api/productos/?categoria=3&proveedor=7&search=coca
    """

    serializer_class = ProductoSerializer

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True).select_related(
            "categoria", "marca", "proveedor"
        )
        params = self.request.query_params

        if categoria_id := params.get("categoria"):
            qs = qs.filter(categoria_id=categoria_id)
        if marca_id := params.get("marca"):
            qs = qs.filter(marca_id=marca_id)
        if proveedor_id := params.get("proveedor"):
            qs = qs.filter(proveedor_id=proveedor_id)
        if texto := params.get("search"):
            qs = qs.filter(nombre__icontains=texto)

        return qs

    def get_permissions(self):
        # La actualización masiva es la única acción restringida a
        # Administrador; el resto del CRUD lo puede usar cualquier usuario
        # autenticado (Administrador u Operador).
        if self.action == "actualizar_precios_masivo":
            return [permissions.IsAuthenticated(), EsAdministrador()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"])
    def agrupado(self, request):
        """
        /api/productos/agrupado/?campo=proveedor  (o categoria, o marca)
        Devuelve los productos agrupados por el campo pedido.
        """
        campo = request.query_params.get("campo", "proveedor")
        if campo not in ("proveedor", "categoria", "marca"):
            return Response(
                {"detalle": "campo debe ser proveedor, categoria o marca"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        productos = self.get_queryset().order_by(f"{campo}__nombre", "nombre")

        grupos = {}
        orden_grupos = []
        for producto in productos:
            relacionado = getattr(producto, campo)
            clave = relacionado.nombre if relacionado else "Sin asignar"
            if clave not in grupos:
                grupos[clave] = []
                orden_grupos.append(clave)
            grupos[clave].append(ProductoSerializer(producto).data)

        resultado = [
            {"grupo": clave, "productos": grupos[clave]} for clave in orden_grupos
        ]
        return Response(resultado)

    @action(detail=False, methods=["post"])
    def actualizar_precios_masivo(self, request):
        """
        Recibe la lista explícita de IDs de productos a actualizar (ya
        filtrados y confirmados del lado del cliente), no filtros: así se
        actualiza exactamente lo que el usuario vio y aprobó en pantalla,
        ni un producto más.
        """
        datos = ActualizacionMasivaSerializer(data=request.data)
        datos.is_valid(raise_exception=True)
        productos_ids = datos.validated_data["productos_ids"]
        campo = datos.validated_data["campo"]
        operacion = datos.validated_data["operacion"]
        valor = datos.validated_data["valor"]

        qs = Producto.objects.filter(activo=True, id__in=productos_ids)

        actualizados = 0
        # Se recorre y guarda uno por uno (en vez de un update() masivo del
        # ORM) porque precio_venta se recalcula en save() y no queremos
        # duplicar esa lógica acá.
        for producto in qs:
            actual = getattr(producto, campo)
            if operacion == "porcentaje":
                nuevo = actual * (Decimal("1") + valor / Decimal("100"))
            elif operacion == "monto_fijo":
                nuevo = actual + valor
            else:  # valor_nuevo
                nuevo = valor

            if nuevo < 0:
                nuevo = Decimal("0.00")

            setattr(producto, campo, nuevo.quantize(Decimal("0.01")))
            producto.save()
            actualizados += 1

        return Response({"actualizados": actualizados})

    @action(detail=False, methods=["post"])
    def generar_listado(self, request):
        """
        Recibe la lista explícita de IDs de productos (ya filtrados y
        confirmados del lado del cliente, igual que en actualización
        masiva) más las columnas elegidas y el formato, y devuelve el
        archivo (PDF o Excel) listo para guardar/compartir.
        """
        datos = GenerarListadoSerializer(data=request.data)
        datos.is_valid(raise_exception=True)
        productos_ids = datos.validated_data["productos_ids"]
        columnas = datos.validated_data["columnas"]
        formato = datos.validated_data["formato"]

        productos = list(
            Producto.objects.filter(activo=True, id__in=productos_ids)
            .select_related("categoria", "marca", "proveedor")
            .order_by("nombre")
        )

        if formato == "excel":
            return generar_listado_excel(productos, columnas)
        return generar_listado_pdf(productos, columnas)


class UsuarioActualView(APIView):
    """/api/me/ — la app lo consulta después del login para saber el rol."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UsuarioActualSerializer(request.user).data)
