from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Categoria, Marca, Proveedor, Producto
from .forms import CategoriaForm, MarcaForm, ProveedorForm, ProductoForm


# ---------------------------------------------------------------------------
# Categoría
# ---------------------------------------------------------------------------

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'core/generic_list.html'
    context_object_name = 'objetos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Categorías',
            'columnas': [('Nombre', 'nombre'), ('Descripción', 'descripcion')],
            'crear_url': reverse_lazy('core:categoria_crear'),
            'detalle_url_name': 'core:categoria_detalle',
            'editar_url_name': 'core:categoria_editar',
            'eliminar_url_name': 'core:categoria_eliminar',
        })
        return context


class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'core/generic_detail.html'
    context_object_name = 'objeto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = self.object
        context.update({
            'titulo': c.nombre,
            'campos': [
                ('Nombre', c.nombre),
                ('Descripción', c.descripcion or '—'),
            ],
            'editar_url': reverse_lazy('core:categoria_editar', args=[c.pk]),
            'eliminar_url': reverse_lazy('core:categoria_eliminar', args=[c.pk]),
            'volver_url': reverse_lazy('core:categoria_lista'),
            'relacionados_titulo': 'Productos en esta categoría',
            'relacionados': c.productos.all(),
        })
        return context


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:categoria_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva categoría'
        context['volver_url'] = reverse_lazy('core:categoria_lista')
        return context


class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:categoria_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar categoría: {self.object.nombre}'
        context['volver_url'] = reverse_lazy('core:categoria_lista')
        return context


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('core:categoria_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'categoría'
        context['volver_url'] = reverse_lazy('core:categoria_lista')
        return context


# ---------------------------------------------------------------------------
# Marca
# ---------------------------------------------------------------------------

class MarcaListView(ListView):
    model = Marca
    template_name = 'core/generic_list.html'
    context_object_name = 'objetos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Marcas',
            'columnas': [('Nombre', 'nombre')],
            'crear_url': reverse_lazy('core:marca_crear'),
            'detalle_url_name': 'core:marca_detalle',
            'editar_url_name': 'core:marca_editar',
            'eliminar_url_name': 'core:marca_eliminar',
        })
        return context


class MarcaDetailView(DetailView):
    model = Marca
    template_name = 'core/generic_detail.html'
    context_object_name = 'objeto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.object
        context.update({
            'titulo': m.nombre,
            'campos': [('Nombre', m.nombre)],
            'editar_url': reverse_lazy('core:marca_editar', args=[m.pk]),
            'eliminar_url': reverse_lazy('core:marca_eliminar', args=[m.pk]),
            'volver_url': reverse_lazy('core:marca_lista'),
            'relacionados_titulo': 'Productos de esta marca',
            'relacionados': m.productos.all(),
        })
        return context


class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:marca_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva marca'
        context['volver_url'] = reverse_lazy('core:marca_lista')
        return context


class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:marca_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar marca: {self.object.nombre}'
        context['volver_url'] = reverse_lazy('core:marca_lista')
        return context


class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('core:marca_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'marca'
        context['volver_url'] = reverse_lazy('core:marca_lista')
        return context


# ---------------------------------------------------------------------------
# Proveedor
# ---------------------------------------------------------------------------

class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'core/generic_list.html'
    context_object_name = 'objetos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Proveedores',
            'columnas': [('Nombre', 'nombre'), ('Contacto', 'contacto'), ('Email', 'email'), ('Teléfono', 'telefono')],
            'crear_url': reverse_lazy('core:proveedor_crear'),
            'detalle_url_name': 'core:proveedor_detalle',
            'editar_url_name': 'core:proveedor_editar',
            'eliminar_url_name': 'core:proveedor_eliminar',
        })
        return context


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'core/generic_detail.html'
    context_object_name = 'objeto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = self.object
        context.update({
            'titulo': p.nombre,
            'campos': [
                ('Nombre', p.nombre),
                ('Contacto', p.contacto or '—'),
                ('Email', p.email or '—'),
                ('Teléfono', p.telefono or '—'),
            ],
            'editar_url': reverse_lazy('core:proveedor_editar', args=[p.pk]),
            'eliminar_url': reverse_lazy('core:proveedor_eliminar', args=[p.pk]),
            'volver_url': reverse_lazy('core:proveedor_lista'),
            'relacionados_titulo': 'Productos de este proveedor',
            'relacionados': p.productos.all(),
        })
        return context


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo proveedor'
        context['volver_url'] = reverse_lazy('core:proveedor_lista')
        return context


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar proveedor: {self.object.nombre}'
        context['volver_url'] = reverse_lazy('core:proveedor_lista')
        return context


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('core:proveedor_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'proveedor'
        context['volver_url'] = reverse_lazy('core:proveedor_lista')
        return context


# ---------------------------------------------------------------------------
# Producto
# ---------------------------------------------------------------------------

class ProductoListView(ListView):
    model = Producto
    template_name = 'core/generic_list.html'
    context_object_name = 'objetos'

    def get_queryset(self):
        return Producto.objects.select_related('categoria', 'marca', 'proveedor').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': 'Productos',
            'columnas': [
                ('Nombre', 'nombre'),
                ('Categoría', 'categoria'),
                ('Marca', 'marca'),
                ('Proveedor', 'proveedor'),
                ('Precio', 'precio'),
                ('Stock', 'stock'),
            ],
            'crear_url': reverse_lazy('core:producto_crear'),
            'detalle_url_name': 'core:producto_detalle',
            'editar_url_name': 'core:producto_editar',
            'eliminar_url_name': 'core:producto_eliminar',
        })
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'core/generic_detail.html'
    context_object_name = 'objeto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = self.object
        context.update({
            'titulo': p.nombre,
            'campos': [
                ('Nombre', p.nombre),
                ('Descripción', p.descripcion or '—'),
                ('Precio', f'${p.precio}'),
                ('Stock', p.stock),
                ('Categoría', p.categoria.nombre),
                ('Marca', p.marca.nombre),
                ('Proveedor', p.proveedor.nombre),
                ('Creado', p.creado),
                ('Actualizado', p.actualizado),
            ],
            'editar_url': reverse_lazy('core:producto_editar', args=[p.pk]),
            'eliminar_url': reverse_lazy('core:producto_eliminar', args=[p.pk]),
            'volver_url': reverse_lazy('core:producto_lista'),
        })
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo producto'
        context['volver_url'] = reverse_lazy('core:producto_lista')
        return context


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('core:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar producto: {self.object.nombre}'
        context['volver_url'] = reverse_lazy('core:producto_lista')
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('core:producto_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'producto'
        context['volver_url'] = reverse_lazy('core:producto_lista')
        return context
