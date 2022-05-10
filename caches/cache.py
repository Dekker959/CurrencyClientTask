from caches.currency_cache import CurrencyCache

class Cache:

    def __init__(self, currency_cache=CurrencyCache()):
        self.currency_cache = currency_cache

    def get_cached_currency(self, base_currency: str, currency: str):
        return self.currency_cache.get_cached_currency(base_currency, currency)

    def cache_currencies(self, base_currency: str, currencies: dict):
        self.currency_cache.cache_currencies(base_currency, currencies)
