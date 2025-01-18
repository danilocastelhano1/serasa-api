from rest_framework.viewsets import ModelViewSet

from .models import Productor
from .serializers import ProductorSerializer


class ProductorViewSet(ModelViewSet):
    queryset = Productor.objects.all().order_by("-created_at")
    serializer_class = ProductorSerializer
