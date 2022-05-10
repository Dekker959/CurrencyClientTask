import os
import requests
import json
import datetime
from caches.cache import Cache
from clients.exchange_rates_auth import *
from caches.currency_cache import *
from loggers.console_logger import CurrencyClientLogger
import config
from requests import HTTPError


class CurrencyClient:
    __slots__ = ["__cache", "__cache_lifetime", "__url", "__api_key", "__prev_cache_time", "__logger"]

    def __init__(self, days: float = 0, seconds: float = 0, microseconds: float = 0,
                 milliseconds: float = 0, minutes: float = 0, hours: float = 0,
                 weeks: float = 0, cache: Cache = Cache(CurrencyCache()), logger=CurrencyClientLogger()):
        """Initializes CurrencyClient Object.

        :param days: float, days component of caches lifetime
        :param seconds: float, seconds component of caches lifetime
        :param microseconds: float, microseconds component of caches lifetime
        :param milliseconds: float, milliseconds component of caches lifetime
        :param minutes: float, minutes component of caches lifetime
        :param hours: float, hours component of caches lifetime
        :param weeks: float, weeks component of caches lifetime
        :param cache: object responsible for caching currency
        """
        self.__cache_lifetime = datetime.timedelta(
            days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes,
            hours=hours, weeks=weeks)
        self.__cache = cache
        self.__url = config.EXCHANGERATE_URL
        self.__api_key = os.getenv(
            'EXCHANGERATE_API_KEY') if config.EXCHANGERATE_API_KEY is "" else config.EXCHANGERATE_API_KEY
        self.__prev_cache_time = None
        self.__logger = logger

    def get_currency(self, currency: str, base_currency: str = "EUR"):
        """Gets exchange rate from base currency to specified currency.

        :param currency: str, currency for witch to get exchange rate
        :param base_currency: str, base currency for witch to get exchange rate
        :return: exchange rate of specified currency
        """
        self.__logger.info(f"Getting exchange rate between '{base_currency}' and '{currency}'.")
        cached_currency = self.__cache.get_cached_currency(base_currency, currency)
        if self.__prev_cache_time is None or cached_currency is None or self.__prev_cache_time + self.__cache_lifetime < datetime.datetime.now():
            response = self._request_latest_rates(base_currency)
            rates = json.loads(response.content)["rates"]
            self.__cache.cache_currencies(base_currency, rates)
            currency_rate = rates[currency]
            self.__prev_cache_time = datetime.datetime.now()
        else:
            self.__logger.info(f"Getting cached exchange rate between '{base_currency}' and '{currency}'.")
            currency_rate = cached_currency
        self.__logger.info(f"Got exchange rate between '{base_currency}' and '{currency}' : {currency_rate}.")
        return {currency: currency_rate}

    def set_interval(self, days: float = 0, seconds: float = 0, microseconds: float = 0,
                     milliseconds: float = 0, minutes: float = 0, hours: float = 0,
                     weeks: float = 0):
        """Sets cache lifetime.

        :param days: float, days component of caches lifetime
        :param seconds: float, seconds component of caches lifetime
        :param microseconds: float, microseconds component of caches lifetime
        :param milliseconds: float, milliseconds component of caches lifetime
        :param minutes: float, minutes component of caches lifetime
        :param hours: float, hours component of caches lifetime
        :param weeks: float, weeks component of caches lifetime
        """
        self.__cache_lifetime = datetime.timedelta(
            days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes,
            hours=hours, weeks=weeks)

    def _request_latest_rates(self, base_currency):
        response = requests.get(
            self.__url, auth=ExchangeRatesAuth(self.__api_key), params=[("base", base_currency)])
        self.__logger.info(f"GET {self.__url} - {response.status_code}")
        self._handle_http_errors(response)
        return response

    def _handle_http_errors(self, response):
        try:
            response.raise_for_status()
        except HTTPError:
            self.__logger.exception("Incorrect status code.")
            raise

