from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.transports import Transport


class AlfabankSoapClient(object):

    def __init__(self, username, password, timeout=30,
                 endpoint='https://test.paymentgate.ru/testpayment/webservices/merchant-ws?wsdl'):
        self._client = Client(
            endpoint, wsse=UsernameToken(username, password), transport=Transport(timeout=timeout))

    def register_order(self, merchant_order_id, amount, return_url, currency_code,
                       params={}, description='', session_timeout=1200):

        return self._client.service.registerOrder({
            'merchantOrderNumber': merchant_order_id,
            'amount': amount,
            'returnUrl': return_url,
            'currency': currency_code,
            'params': params,
            'description': description,
            'sessionTimeoutSecs': session_timeout
        })

    def get_order_status(self, order_id, lang='ru'):
        return self._client.service.getOrderStatus({'orderId': order_id, 'language': lang})

    def get_order_status_extended(self, order_id, merchant_order_id, lang='ru'):
        return self._client.service.getOrderStatusExtended({'orderId': order_id,
                                                            'merchantOrderNumber': merchant_order_id,
                                                            'language': lang})
