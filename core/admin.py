from django.contrib import admin

from .models import Categoria, Marca, Proveedor, Producto, FormaDePago, Parametro
from decimal import Decimal


def aplicar_porcentaje(modeladmin, request, queryset, porcentaje):
    factor = Decimal("1") + Decimal(str(porcentaje)) / Decimal("100")
    for producto in queryset:
        producto.precio_unitario = (producto.precio_unitario * factor).quantize(Decimal("0.01"))
        producto.save()


@admin.action(description="Aumentar precio unitario 10%%")
def aumentar_10_por_ciento(modeladmin, request, queryset):
    aplicar_porcentaje(modeladmin, request, queryset, 10)


@admin.action(description="Disminuir precio unitario 10%%")
def disminuir_10_por_ciento(modeladmin, request, queryset):
    aplicar_porcentaje(modeladmin, request, queryset, -10)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'email', 'telefono')
    search_fields = ('nombre', 'contacto', 'email')


@admin.register(FormaDePago)
class FormaDePagoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)


@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'valor', 'descripcion')
    list_filter = ('tipo',)
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'proveedor', "precio_unitario", "porcentaje_ganancia", "precio_venta", "stock", "codigo_barra", "activo")
    list_filter = ('categoria', 'marca', 'proveedor')
    search_fields = ('nombre', 'codigo_barra')
    autocomplete_fields = ('categoria', 'marca', 'proveedor')
    actions = [aumentar_10_por_ciento, disminuir_10_por_ciento]
