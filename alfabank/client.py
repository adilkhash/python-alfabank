from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport

from .models import NewOrder, OrderStatus


class AlfabankSoapClient(object):

    def __init__(self, username, password, timeout=30,
                 endpoint='https://test.paymentgate.ru/testpayment/webservices/merchant-ws?wsdl'):
        self._client = Client(
            endpoint, wsse=UsernameToken(username, password), transport=Transport(timeout=timeout))

    def register_order(self, merchant_order_id, amount, return_url, currency_code,
                       params=None, description='', session_timeout=1200):

        response = self._client.service.registerOrder({
            'merchantOrderNumber': merchant_order_id,
            'amount': amount,
            'returnUrl': return_url,
            'currency': currency_code,
            'params': params if params else {},
            'description': description,
            'sessionTimeoutSecs': session_timeout
        })

        order = NewOrder(response)
        return order

    def get_order_status(self, order_id, lang='ru'):
        response = self._client.service.getOrderStatus({'orderId': order_id, 'language': lang})
        return OrderStatus(response)

    def get_order_status_extended(self, order_id, merchant_order_id, lang='ru'):
        response = self._client.service.getOrderStatusExtended({
            'orderId': order_id,
            'merchantOrderNumber': merchant_order_id,
            'language': lang})
        return OrderStatus(response)
