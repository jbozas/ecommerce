from utils.models import TimeStampedModel
from django.db import models


class Product(TimeStampedModel):
    """
    Base class to model a Product object
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    stock = models.IntegerField(default=0)

    def update_stock(self, quantity: int):
        self.stock -= quantity
        self.save()

    def has_stock(self, quantity: int) -> bool:
        return self.stock >= quantity
