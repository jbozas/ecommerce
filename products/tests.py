from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product


class ProductTests(APITestCase):
    """
    Tests created to check HTTP methods
    on product's ModelViewSet.
    """

    def setUp(self):
        self.url = reverse('products:products-list')

    def _mocked_product_data(self):
        return {
            'name': 'Truck',
            'price': 1000.12,
            'stock': 4
        }

    def _modified_product_data(self):
        return {
            'stock': 3
        }

    def _create_dummy_product(self):
        return Product.objects.create(**self._mocked_product_data())

    def test_create_product_should_return_201(self):
        """
        Ensure we can create a new account object.
        """
        data = self._mocked_product_data()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, data.get('name'))

    def test_create_product_should_return_400(self):
        """
        Invalid post
        """
        data = self._modified_product_data()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

    def test_list_product_should_return_201(self):
        """
        Create a Product and then try to list it.
        """
        self._create_dummy_product()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_product_should_return_201(self):
        """
        Test patch a Product successfully.
        """
        product = self._create_dummy_product()
        url = reverse('products:products-detail', args=[product.id])
        response = self.client.patch(
            url,
            data=self._modified_product_data(),
            format='json'
        )
        product.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product.stock, 3)

    def test_delete_product_should_return_201(self):
        """
        Test delete a Product successfully.
        """
        product = self._create_dummy_product()
        url = reverse('products:products-detail', args=[product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.exists(), False)

    def test_delete_product_should_return_404(self):
        """
        Test delete a Product who doesnt exist.
        """
        url = reverse('products:products-detail', args=[10])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.exists(), False)
