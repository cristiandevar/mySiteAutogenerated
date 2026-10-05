from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    # Categoría
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_lista'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria_detalle'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_eliminar'),

    # Marca
    path('marcas/', views.MarcaListView.as_view(), name='marca_lista'),
    path('marcas/nueva/', views.MarcaCreateView.as_view(), name='marca_crear'),
    path('marcas/<int:pk>/', views.MarcaDetailView.as_view(), name='marca_detalle'),
    path('marcas/<int:pk>/editar/', views.MarcaUpdateView.as_view(), name='marca_editar'),
    path('marcas/<int:pk>/eliminar/', views.MarcaDeleteView.as_view(), name='marca_eliminar'),

    # Proveedor
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_lista'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('proveedores/<int:pk>/', views.ProveedorDetailView.as_view(), name='proveedor_detalle'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.ProveedorDeleteView.as_view(), name='proveedor_eliminar'),

    # Producto
    path('productos/', views.ProductoListView.as_view(), name='producto_lista'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detalle'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
]
