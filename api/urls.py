from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductorViewSet

router = DefaultRouter()
router.register(r"productor", ProductorViewSet, basename="productor")

urlpatterns = [
    path(r"", include(router.urls)),
]
