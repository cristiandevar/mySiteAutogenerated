from rest_framework.permissions import BasePermission

ROL_ADMINISTRADOR = "Administrador"
ROL_OPERADOR = "Operador"


class EsAdministrador(BasePermission):
    """
    Permite el acceso solo a usuarios que pertenecen al grupo Administrador
    (o a un superusuario). Se usa para las acciones que un Operador no debe
    poder ejecutar: actualización masiva de precios, y en el admin de Django,
    la gestión de usuarios.

    Importante: esto se valida siempre del lado del servidor. Que la app
    Android oculte un botón para el Operador es solo una comodidad de UI,
    nunca la única barrera de seguridad.
    """

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name=ROL_ADMINISTRADOR).exists()


def rol_de(user) -> str:
    """Devuelve el nombre de rol a mostrar/usar en la app para este usuario."""
    if user.is_superuser or user.groups.filter(name=ROL_ADMINISTRADOR).exists():
        return ROL_ADMINISTRADOR
    if user.groups.filter(name=ROL_OPERADOR).exists():
        return ROL_OPERADOR
    return "Sin rol asignado"
