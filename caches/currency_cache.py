class CurrencyCache:
    __slots__ = ["cache"]

    def __init__(self):
        self.cache = {}

    def get_cached_currency(self, base_currency, currency):
        currencies = self.cache.get(base_currency)
        return None if currencies is None else currencies.get(currency)

    def cache_currencies(self, base_currency: str, currencies: dict):
        self.cache[base_currency] = currencies
