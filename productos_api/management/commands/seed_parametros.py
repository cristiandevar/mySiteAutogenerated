from django.core.management.base import BaseCommand

# TODO: reemplazar "core" si tus modelos reales viven en otra app.
from core.models import (
    Parametro,
    PARAM_ORDEN_VENCIMIENTO_DIAS,
    PARAM_ORDEN_CANCELACION_HORAS,
    PARAM_VENTA_CANCELACION_HORAS,
)

# (nombre, tipo, valor, descripción) de cada parámetro que ya usa el
# sistema. Se puede volver a correr el comando sin problema: los que ya
# existen no se pisan (get_or_create), para no perder un valor que el
# Administrador ya haya ajustado a mano desde el admin.
PARAMETROS_INICIALES = [
    (
        PARAM_ORDEN_VENCIMIENTO_DIAS,
        Parametro.TIPO_ENTERO,
        "3",
        "Días que el link de confirmación de una Orden queda activo desde "
        "que se genera. Pasado este tiempo sin respuesta del proveedor, la "
        "orden pasa a VENCIDA.",
    ),
    (
        PARAM_ORDEN_CANCELACION_HORAS,
        Parametro.TIPO_ENTERO,
        "24",
        "Horas desde que se generó la Orden durante las cuales el "
        "Administrador todavía puede cancelarla (si está GENERADA o "
        "CONFIRMADA). Ajustar este valor según corresponda.",
    ),
    (
        PARAM_VENTA_CANCELACION_HORAS,
        Parametro.TIPO_ENTERO,
        "72",
        "Horas desde la Venta durante las cuales se puede cancelar/"
        "devolver un producto de esa venta.",
    ),
]


class Command(BaseCommand):
    help = "Crea los parámetros iniciales del sistema (si todavía no existen)."

    def handle(self, *args, **options):
        for nombre, tipo, valor, descripcion in PARAMETROS_INICIALES:
            _, creado = Parametro.objects.get_or_create(
                nombre=nombre,
                defaults={"tipo": tipo, "valor": valor, "descripcion": descripcion},
            )
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Parámetro '{nombre}' creado con valor '{valor}'."))
            else:
                self.stdout.write(f"Parámetro '{nombre}' ya existía, no se modificó.")
