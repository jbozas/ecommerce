import datetime

from utils.models import TimeStampedModel
from django.db import models

from currencies.dolars.dolarsi import DolarsiService
from utils.errors import ProductOrStockNotFound

from products.models import Product


class Order(TimeStampedModel):
    """
    Base class to model a Order object
    """
    date_time = models.DateTimeField(
        auto_now_add=False, null=True, blank=True, db_index=True)

    @property
    def get_total(self) -> float:
        """
        Returns the total to pay
        """
        return sum(detail.total for detail in self.details.all())

    @property
    def get_total_in_dollars(self) -> float:
        """
        Returns the total to pay in dollars.
        """
        return DolarsiService(dollar_type="Dolar Blue").get_price_in_dollars(
            self.get_total)

    @property
    def cancel_transaction(self):
        for detail in self.details.all():
            detail.restore_stock

    def delete(self):
        self.cancel_transaction
        super(Order, self).delete()


class OrderDetail(TimeStampedModel):
    """
    Order's details
    """
    order = models.ForeignKey(Order, related_name='details',
                              on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    @property
    def total(self) -> float:
        return self.quantity * self.product.price

    @property
    def restore_stock(self):
        self.product.update_stock(-self.quantity)

    @classmethod
    def create(self, product: Product, quantity: int, order: Order, args=None, **kwargs):
        """
        Creates a new detail. For this checks that the actual Product's
        quantity is enough for the purchase.
        """
        if not product.has_stock(quantity):
            raise ProductOrStockNotFound('Stock not found.')

        order.date_time = datetime.datetime.now()
        product.update_stock(quantity)

        data = {
            'product': product,
            'order': order,
            'quantity': quantity,
        }

        return self.objects.get_or_create(**data)
