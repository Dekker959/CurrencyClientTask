class TestingCache:
    __slots__ = ["cache", "test_value"]

    def __init__(self, test_value):
        self.cache = {}
        self.test_value = test_value

    def get_cached_currency(self, base_currency, currency):
        return self.test_value

    def cache_currencies(self, base_currency: str, currencies: dict):
        self.cache[base_currency] = currencies
