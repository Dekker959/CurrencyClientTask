import time
from unittest import mock
from unittest.mock import Mock, patch

import pytest
import requests

from caches.cache import Cache
from clients.currency_client import CurrencyClient, CurrencyCache
from requests import HTTPError, Response
from tests.testing_cache import TestingCache


class TestCurrencyClient:

    def test_get_currency_positive(self):
        currency = "USD"
        currency_client = CurrencyClient()

        currency_rate = currency_client.get_currency(currency)

        assert currency_rate.get(currency) > 0

    def test_get_currency_uses_cached_data(self):
        currency = "USD"
        test_value = -999
        currency_client = CurrencyClient(minutes=5, cache=Cache(TestingCache(test_value)))

        currency_client.get_currency(currency)
        cached_currency_rate = currency_client.get_currency(currency)

        assert cached_currency_rate[currency] == test_value

    def test_get_currency_caches_data(self):
        currency_name = "USD"
        base_currency_name = "EUR"
        cache = Cache(CurrencyCache())
        currency_client = CurrencyClient(cache=cache)

        currency_rate = currency_client.get_currency(currency_name, base_currency_name)

        assert cache.get_cached_currency(base_currency_name, currency_name) == currency_rate[currency_name]

    def test_get_currency_repeats_call_after_timeout(self):
        currency_name = "USD"
        test_value = -999
        currency_client = CurrencyClient(seconds=1, cache=Cache(TestingCache(test_value)))

        currency_client.get_currency(currency_name)
        time.sleep(1)
        currency_rate = currency_client.get_currency(currency_name)

        assert currency_rate.get(currency_name) > 0

    def test_get_currency_raises_http_error(self):
        currency = "USD"
        currency_client = CurrencyClient()
        mock_response = Response()
        mock_response.status_code = 404

        with pytest.raises(HTTPError):
            with patch.object(requests, 'get', return_value=mock_response):
                currency_rate = currency_client.get_currency(currency)

