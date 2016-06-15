# -*- coding: utf-8 -*-
import os

import responses


from alfabank.client import AlfabankSoapClient
from alfabank.models import NewOrder, OrderStatus


URL = 'https://test.paymentgate.ru/testpayment/webservices/merchant-ws'

WSDL_FILE = os.path.join(os.path.dirname(__file__), 'wsdl', 'Merchant.wsdl').replace('\\', '/')

client = AlfabankSoapClient('test', 'passwd', endpoint='file://%s' % (WSDL_FILE,))



@responses.activate
def test_register_order_fault():

    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <ns1:registerOrderResponse xmlns:ns1="http://engine.paymentgate.ru/webservices/merchant">
                            <return errorCode="1" errorMessage="Order already processed"/>
                        </ns1:registerOrderResponse>
                    </soap:Body>
                </soap:Envelope>"""

    responses.add(responses.POST, URL, body=payload, status=200)
    response = client.register_order(999, 999, 'http://test.com', 398)

    assert isinstance(response, NewOrder) is True
    assert response.error_code == '1'
    assert response.is_successful() is False
    assert response.error_message.lower() == 'order already processed'


@responses.activate
def test_register_order_success():

    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <ns1:registerOrderResponse xmlns:ns1="http://engine.paymentgate.ru/webservices/merchant">
                            <return orderId="45e6a28c-b782-442e-b24a-33b5d3be5585" errorCode="0" errorMessage="Success">
                                <formUrl>https://test.paymentgate.ru/testpayment/merchants/aviata_kz/payment_ru.html?mdOrder=45e6a28c-b782-442e-b24a-33b5d3be5585</formUrl>
                            </return>
                        </ns1:registerOrderResponse>
                    </soap:Body>
                </soap:Envelope>"""

    responses.add(responses.POST, URL, body=payload, status=200)
    response = client.register_order(999, 999, 'http://test.com', 398)

    assert isinstance(response, NewOrder) is True
    assert response.error_code == '0'
    assert response.is_successful() is True
    assert response.payment_url == 'https://test.paymentgate.ru/testpayment/merchants/aviata_kz/payment_ru.html?mdOrder=45e6a28c-b782-442e-b24a-33b5d3be5585'
    assert response.error_message.lower() == 'success'


@responses.activate
def test_get_order_status_fault():

    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <ns1:getOrderStatusResponse xmlns:ns1="http://engine.paymentgate.ru/webservices/merchant">
                            <return orderStatus="0" amount="0" authCode="0" errorCode="6" errorMessage="Unknown order id"/>
                        </ns1:getOrderStatusResponse>
                    </soap:Body>
                </soap:Envelope>"""

    responses.add(responses.POST, URL, body=payload, status=200)
    response = client.get_order_status('213123123123', 'ru')

    assert isinstance(response, OrderStatus) is True
    assert response.error_code == '6'
    assert response.is_successful() is False
    assert response.error_message.lower() == 'unknown order id'


@responses.activate
def test_get_order_status_pending():

    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <ns1:getOrderStatusResponse xmlns:ns1="http://engine.paymentgate.ru/webservices/merchant">
                            <return orderStatus="0" orderNumber="9935" amount="10000" currency="398" authCode="2" date="2016-06-15T21:55:05.063+03:00" actionCodeDescription="" errorCode="0"/>
                        </ns1:getOrderStatusResponse>
                    </soap:Body>
                </soap:Envelope>"""

    responses.add(responses.POST, URL, body=payload, status=200)
    response = client.get_order_status('213123123123', 'ru')

    assert isinstance(response, OrderStatus) is True
    assert response.error_code == '0'
    assert response.is_successful() is True
    assert response.is_paid() is False
    assert response.action_code_description.lower() == ''
    assert response.auth_code == '2'
    assert response.order_number == '9935'


@responses.activate
def test_get_order_status_successful_payment():

    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <ns1:getOrderStatusResponse xmlns:ns1="http://engine.paymentgate.ru/webservices/merchant">
                            <return orderStatus="2" orderNumber="9935" pan="411111**1111" expiration="201912" cardholderName="ivan ivanov" amount="10000" currency="398" approvalCode="123456" authCode="2" ip="95.56.82.188" date="2016-06-15T21:55:05.063+03:00" actionCodeDescription="" errorCode="0">
                            <params name="browser_version_param" value="51.0.2704.84"/>
                                <params name="browser_name_param" value="CHROME"/>
                                <params name="browser_os_param" value="WINDOWS"/>
                                <params name="user_agent" value="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"/>
                                <params name="browser_language_param" value="ru"/>
                            </return>
                        </ns1:getOrderStatusResponse>
                    </soap:Body>
                </soap:Envelope>"""

    responses.add(responses.POST, URL, body=payload, status=200)
    response = client.get_order_status('213123123123', 'ru')

    assert isinstance(response, OrderStatus) is True
    assert response.error_code == '0'
    assert response.is_successful() is True
    assert response.is_paid() is True
    assert response.order_number == '9935'
    assert response.params
    assert response.cardholder_name.lower() == 'ivan ivanov'
    assert response.approval_code.lower() == '123456'
    assert response.ip == '95.56.82.188'
