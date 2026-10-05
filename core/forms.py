from django import forms

from .models import Categoria, Marca, Proveedor, Producto

_INPUT = {'class': 'form-control'}
_SELECT = {'class': 'form-select'}


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs=_INPUT),
            'descripcion': forms.Textarea(attrs={**_INPUT, 'rows': 3}),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs=_INPUT),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs=_INPUT),
            'contacto': forms.TextInput(attrs=_INPUT),
            'email': forms.EmailInput(attrs=_INPUT),
            'telefono': forms.TextInput(attrs=_INPUT),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio_unitario', 'stock',
            'categoria', 'marca', 'proveedor',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs=_INPUT),
            'descripcion': forms.Textarea(attrs={**_INPUT, 'rows': 3}),
            'precio_unitario': forms.NumberInput(attrs={**_INPUT, 'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={**_INPUT, 'min': '0'}),
            'categoria': forms.Select(attrs=_SELECT),
            'marca': forms.Select(attrs=_SELECT),
            'proveedor': forms.Select(attrs=_SELECT),
        }
