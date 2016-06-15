

class Base(object):
    def __init__(self, payload):
        self._payload = payload

    def is_successful(self):
        return True if self.error_code == '0' else False

    def __getattr__(self, item):
        name = ''.join(map(str.capitalize, item.split('_')))
        name = name[0].lower() + name[1:]
        return getattr(self._payload, name)


class NewOrder(Base):
    """registerOrder resposne model
    """

    @property
    def payment_url(self):
        return self.form_url


class OrderStatus(Base):
    """getOrderStatus/getOrderStatusExtended response model
    """

    def is_paid(self):
        if self.is_successful() and self.order_status == 2:
            return True
        return False

    @property
    def rejection_reason(self):
        return self.action_code_description or self.action_code
