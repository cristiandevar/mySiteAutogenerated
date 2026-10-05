from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)  # NUEVO

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        indexes = [
            models.Index(fields=['nombre'], name='idx_categoria_nombre'),
        ]

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)  # NUEVO

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        indexes = [
            models.Index(fields=['nombre'], name='idx_marca_nombre'),
        ]

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    contacto = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)  # NUEVO

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        indexes = [
            models.Index(fields=['nombre'], name='idx_proveedor_nombre'),
        ]

    def __str__(self):
        return self.nombre


class FormaDePago(models.Model):
    """
    Maestro de formas de pago (efectivo, tarjeta de débito, transferencia,
    etc.), usado en Ventas (Fase 2) para registrar con qué se cobró. Mismo
    patrón simple que Categoria/Marca/Proveedor: nombre único + baja lógica.
    """

    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Forma de pago'
        verbose_name_plural = 'Formas de pago'
        indexes = [
            models.Index(fields=['nombre'], name='idx_formadepago_nombre'),
        ]

    def __str__(self):
        return self.nombre


class Parametro(models.Model):
    """
    Valores configurables del sistema (ventanas de tiempo para vencimiento
    y cancelación de Órdenes y Ventas, stock mínimo, etc.) sin tener que
    tocar código para ajustarlos. Todo se guarda como texto (varchar) y
    "tipo" indica cómo interpretarlo; valor_tipado() hace la conversión.

    Por ahora se administra desde el admin de Django (lo usa el
    Administrador del negocio, no hace falta pantalla en la app). Si más
    adelante se necesita editarlos desde la app, se agrega esa pantalla
    reusando este mismo modelo.
    """

    TIPO_TEXTO = 'texto'
    TIPO_ENTERO = 'entero'
    TIPO_DECIMAL = 'decimal'
    TIPO_BOOLEANO = 'booleano'
    TIPOS = [
        (TIPO_TEXTO, 'Texto'),
        (TIPO_ENTERO, 'Número entero'),
        (TIPO_DECIMAL, 'Número decimal'),
        (TIPO_BOOLEANO, 'Sí / No'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default=TIPO_TEXTO)
    valor = models.CharField(max_length=255)
    descripcion = models.TextField(
        blank=True,
        help_text="Para qué se usa este parámetro y qué formato espera.",
    )

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Parámetro'
        verbose_name_plural = 'Parámetros'

    def __str__(self):
        return f"{self.nombre} = {self.valor}"

    def clean(self):
        # Valida que "valor" tenga el formato que "tipo" promete, para no
        # descubrir un parámetro mal cargado recién cuando se intenta usar.
        if self.tipo == self.TIPO_ENTERO:
            try:
                int(self.valor)
            except (TypeError, ValueError):
                raise ValidationError(
                    {"valor": "Este parámetro es de tipo entero: el valor debe ser un número entero (ej: 3)."}
                )
        elif self.tipo == self.TIPO_DECIMAL:
            try:
                Decimal(self.valor)
            except (TypeError, InvalidOperation):
                raise ValidationError(
                    {"valor": "Este parámetro es de tipo decimal: el valor debe ser un número (ej: 1.5)."}
                )
        elif self.tipo == self.TIPO_BOOLEANO:
            if self.valor.strip().lower() not in ("true", "false", "1", "0", "si", "sí", "no"):
                raise ValidationError(
                    {"valor": "Este parámetro es de tipo Sí/No: usá 'true'/'false' (o 'si'/'no')."}
                )

    def valor_tipado(self):
        """Devuelve "valor" ya convertido según "tipo"."""
        if self.tipo == self.TIPO_ENTERO:
            return int(self.valor)
        if self.tipo == self.TIPO_DECIMAL:
            return Decimal(self.valor)
        if self.tipo == self.TIPO_BOOLEANO:
            return self.valor.strip().lower() in ("true", "1", "si", "sí")
        return self.valor


# Nombres de los parámetros que ya usa el sistema (Fase 1/2). Centralizarlos
# acá evita errores de tipeo al pedirlos desde otras partes del código.
PARAM_ORDEN_VENCIMIENTO_DIAS = "orden_vencimiento_dias"
PARAM_ORDEN_CANCELACION_HORAS = "orden_cancelacion_horas"
PARAM_VENTA_CANCELACION_HORAS = "venta_cancelacion_horas"


def obtener_parametro(nombre: str, default=None):
    """
    Devuelve el valor ya tipado del parámetro "nombre", o "default" si no
    existe. Pensado para usarse en la lógica de Órdenes/Ventas sin repetir
    el try/except en cada lugar donde se necesite un parámetro.
    """
    try:
        return Parametro.objects.get(nombre=nombre).valor_tipado()
    except Parametro.DoesNotExist:
        return default


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    # Antes: precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # RENOMBRADO desde "precio"
    porcentaje_ganancia = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal("0.00")
    )  # NUEVO
    precio_venta = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), editable=False
    )  # NUEVO — se recalcula solo en save(), no se edita a mano

    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)  # NUEVO

    # NUEVO (Fase 0c): código de barra para escanear el producto al crear
    # una Venta. Opcional porque no todos los productos de un polirubro
    # traen código (ej: productos sueltos/fraccionados), pero si se carga,
    # tiene que ser único.
    codigo_barra = models.CharField(
        max_length=64, blank=True, null=True, unique=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='productos',
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        indexes = [
            models.Index(fields=['nombre'], name='idx_producto_nombre'),
            models.Index(fields=['categoria', 'marca'], name='idx_producto_cat_marca'),
            models.Index(fields=['codigo_barra'], name='idx_producto_codigo_barra'),
        ]

    def calcular_precio_venta(self) -> Decimal:
        factor = Decimal("1") + (self.porcentaje_ganancia / Decimal("100"))
        return (self.precio_unitario * factor).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        self.precio_venta = self.calcular_precio_venta()
        # codigo_barra es blank=True + null=True: si se guarda como "" (lo
        # que hacen los formularios cuando se deja vacío) en vez de None,
        # el unique=True explota apenas haya 2 productos sin código, porque
        # "" sí se considera un valor repetido (a diferencia de NULL). Se
        # normaliza acá para que "sin código" sea siempre NULL.
        self.codigo_barra = self.codigo_barra or None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
