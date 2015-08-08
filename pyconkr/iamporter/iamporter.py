# -*- coding: utf-8 -*-
import requests


class IamporterError(Exception):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message


def get_access_token(api_key, api_secret):
    url = 'https://api.iamport.kr/users/getToken'
    response = requests.post(url, data=dict(
        imp_key=api_key,
        imp_secret=api_secret,
    ))

    if response.status_code != 200:
        raise IOError  # TODO

    # TODO : validate expire time
    result = response.json()

    if result['code'] is not 0:
        raise IamporterError(result['code'], result['message'])

    return result['response']['access_token']


class Iamporter(object):
    TOKEN_HEADER = 'X-ImpTokenHeader'

    def __init__(self, access_token):
        self._access_code = access_token

    def _post(self, url, data, headers=None):
        if not headers:
            headers = {}
        headers[self.TOKEN_HEADER] = self._access_code

        response = requests.post(url, headers=headers, data=data)

        if response.status_code != 200 or not response.content:
            raise IOError

        result = response.json()

        if result['code'] is not 0:
            raise IamporterError(result['code'], result['message'])

        return result

    def onetime(self, **params):
        url = 'https://api.iamport.kr/subscribe/payments/onetime/'

        keys = ['token', 'merchant_uid', 'amount', 'vat', 'card_number', 'expiry', 'birth', 'pwd_2digit', 'remember_me', 'customer_uid']
        data = {k: v for k, v in params.items() if k in keys}

        return self._post(url, data)
