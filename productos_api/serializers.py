from rest_framework import serializers

# TODO: reemplazar "tu_app" por el nombre real de la app donde están tus modelos.
from core.models import Categoria, Marca, Proveedor, Producto
from .listados import COLUMNAS_LISTADO
from .permissions import rol_de


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion", "activo"]


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ["id", "nombre", "activo"]


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ["id", "nombre", "contacto", "email", "telefono", "activo"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    marca_nombre = serializers.CharField(source="marca.nombre", read_only=True)
    proveedor_nombre = serializers.CharField(source="proveedor.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "descripcion",
            "categoria",
            "categoria_nombre",
            "marca",
            "marca_nombre",
            "proveedor",
            "proveedor_nombre",
            "precio_unitario",
            "porcentaje_ganancia",
            "precio_venta",
            "stock",
            "activo",
            "creado",
            "actualizado",
        ]
        read_only_fields = ["precio_venta", "creado", "actualizado"]


class UsuarioActualSerializer(serializers.Serializer):
    """Lo que la app consulta al loguearse para saber qué mostrar en el menú."""

    username = serializers.CharField()
    rol = serializers.SerializerMethodField()

    def get_rol(self, user):
        return rol_de(user)


class ActualizacionMasivaSerializer(serializers.Serializer):
    CAMPOS_VALIDOS = ["precio_unitario", "porcentaje_ganancia"]
    OPERACIONES_VALIDAS = ["porcentaje", "monto_fijo", "valor_nuevo"]

    # Antes se mandaban "filtros" y el backend aplicaba a lo que matcheara
    # en ese instante. Ahora la app ya resolvió los filtros del lado del
    # cliente, le mostró el resultado al usuario y le permitió deseleccionar
    # productos, así que acá llega la lista final y explícita de IDs
    # confirmados: ni un producto más, ni uno menos.
    productos_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    campo = serializers.ChoiceField(choices=CAMPOS_VALIDOS)
    operacion = serializers.ChoiceField(choices=OPERACIONES_VALIDAS)
    valor = serializers.DecimalField(max_digits=12, decimal_places=2)


class GenerarListadoSerializer(serializers.Serializer):
    FORMATOS_VALIDOS = ["pdf", "excel"]

    # Igual que en la actualización masiva: la app ya mostró el resultado
    # de los filtros en pantalla y el usuario deseleccionó lo que no
    # quería, así que acá llega la lista final y explícita de IDs.
    productos_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    columnas = serializers.ListField(
        child=serializers.ChoiceField(choices=list(COLUMNAS_LISTADO.keys())),
        allow_empty=False,
    )
    formato = serializers.ChoiceField(choices=FORMATOS_VALIDOS)
