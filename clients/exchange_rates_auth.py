from requests import Request
from requests.auth import AuthBase


class ExchangeRatesAuth(AuthBase):

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, r: Request):
        r.headers["apikey"] = self.api_key
        return r
