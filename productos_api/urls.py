from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CategoriaViewSet,
    MarcaViewSet,
    ProveedorViewSet,
    ProductoViewSet,
    UsuarioActualView,
)

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("marcas", MarcaViewSet, basename="marca")
router.register("proveedores", ProveedorViewSet, basename="proveedor")
router.register("productos", ProductoViewSet, basename="producto")

urlpatterns = [
    path("", include(router.urls)),
    path("me/", UsuarioActualView.as_view(), name="me"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
