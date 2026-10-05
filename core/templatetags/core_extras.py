from django import template

register = template.Library()


@register.filter
def getattribute(objeto, nombre_atributo):
    """Permite acceder a un atributo de un objeto usando un nombre dinámico
    (string) desde el template, ej: {{ objeto|getattribute:'nombre' }}.
    Usado por generic_list.html para renderizar columnas configurables.
    """
    return getattr(objeto, nombre_atributo, '')
