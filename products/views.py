from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.serializers import ProductSerializer


class ProductApiViewSet(ModelViewSet):
    """
    This view resolve:
        * Registrar/Editar un producto
        * Eliminar un producto
        * Consultar un producto
        * Listar todos los productos
        * Modificar stock de un producto
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch', ]
    permission_classes = [IsAuthenticated]
