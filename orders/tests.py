from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from orders.models import Order, OrderDetail
from utils.tests import authenticate


class AccountTests(APITestCase):
    """
    Tests created to check HTTP methods
    on order's ModelViewSet.
    """

    def setUp(self):
        authenticate(self.client)
        self.url_list = reverse('orders:orders-list')
        self.url_create = reverse('orders:transaction-list')
        self.order = Order.objects.create()
        self.product = Product.objects.create(**{
            'name': 'Truck',
            'price': 1000.12,
            'stock': 4
        })
        self.order_detail = OrderDetail.create(
            order=self.order, product=self.product, quantity=1)

    def test_list_order_should_return_200(self):
        """
        Ensure we can list a just created Order and OrderDetail object.
        """
        response = self.client.get(self.url_list, format='json')
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        # Check the detail
        self.assertEqual(len(response.json()[0].get('details')), 1)
        # Check the order totals
        self.assertEqual(self.order.get_total,
                         round(Decimal(response.json()[0].get('total_ARS')), 2))
        self.assertEqual(self.order.get_total_in_dollars,
                         round(Decimal(response.json()[0].get('total_USD')), 2))

    def test_create_order_should_return_201(self):
        """
        Ensure we can create a new Order and OrderDetail object.
        """
        self.product.refresh_from_db()
        data = {
            'details': [
                {
                    'product': {
                        'id': self.product.id,
                        'name': self.product.name
                    },
                    'quantity': 1

                }
            ]
        }
        response = self.client.post(self.url_create, data, format='json')
        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check the detail
        new_order = Order.objects.last()
        self.assertEqual(new_order.id, response.json().get('id'))

        stock_before_ordering = self.product.stock
        self.product.refresh_from_db()
        stock_after_ordering = self.product.stock
        self.assertEqual(stock_before_ordering -
                         new_order.details.first().quantity, stock_after_ordering)

    def test_delete_order_should_return_201(self):
        """
        Test delete a Order successfully.
        """
        url = reverse('orders:transaction-detail', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.exists(), False)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)
