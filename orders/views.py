from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from utils.errors import TransactionCreationError

from orders.serializers import OrderSerializer
from orders.models import Order


class OrderApiViewSet(ModelViewSet):
    """
    This view resolves:
        * Consultar una orden y sus detalles
        * Listar todas las ordenes
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]


class CreateDestroyOrderApiViewSet(ModelViewSet):
    """
    This view resolves:
        * Registrar/Editar una orden (inclusive sus detalles). Debe actualizar el stock del producto
        * Eliminar una orden. Restaura stock del producto
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    http_method_names = ['post', 'delete']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise TransactionCreationError(error=serializer.errors)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
            order.delete()
        except Exception:
            return Response('Order not found.', status=status.HTTP_400_BAD_REQUEST)
        return Response('Order deleted successfully.', status=status.HTTP_204_NO_CONTENT)
