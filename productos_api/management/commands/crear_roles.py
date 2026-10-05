from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from productos_api.permissions import ROL_ADMINISTRADOR, ROL_OPERADOR


class Command(BaseCommand):
    help = "Crea los grupos Administrador y Operador si todavía no existen."

    def handle(self, *args, **options):
        for nombre in (ROL_ADMINISTRADOR, ROL_OPERADOR):
            _, creado = Group.objects.get_or_create(name=nombre)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo '{nombre}' creado."))
            else:
                self.stdout.write(f"Grupo '{nombre}' ya existía.")
