from decimal import Decimal
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
        ]

    def calcular_precio_venta(self) -> Decimal:
        factor = Decimal("1") + (self.porcentaje_ganancia / Decimal("100"))
        return (self.precio_unitario * factor).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        self.precio_venta = self.calcular_precio_venta()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre