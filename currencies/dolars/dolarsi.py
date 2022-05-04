from decimal import Decimal

from currencies.dolars.constants import DolarsiConstants
from utils.errors import ServiceInitializationError, ServiceUnavailableError

import requests


class DolarsiService(object):
    """
    Class in charge of DOLARS
    currency covertion
    """

    def __init__(self, dollar_type, *args, **kwargs) -> None:
        if dollar_type not in DolarsiConstants.DOLLAR_TYPES:
            raise ServiceInitializationError(error='Currency not supported.')
        self.dollar_type = dollar_type
        self.url = DolarsiConstants.SERVICE_URL

        super().__init__(*args, **kwargs)

    def get_current_currency_value(self) -> Decimal:
        response = requests.get(self.url, timeout=2)
        if response.status_code != 200:
            raise ServiceUnavailableError(
                error=f'Service cannot be reached, response status code: {response.status_code}')
        for dollar_type in response.json():
            house = dollar_type.get('casa')
            if self.dollar_type == house.get('nombre'):
                return (Decimal(house.get('compra').replace(',', '.')))
        return 0

    def get_price_in_dollars(self, amount: float) -> Decimal:
        return Decimal(amount) * self.get_current_currency_value()
