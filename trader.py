

class Trader:
    """
    The trader class which can sell and buy a list of currencies with a given exchange rate
    """
    def __init__(self, currencies: list, base_founds: dict = None):
        """
        Basic initialisation
        :param currencies: all currencies that can be hold by the trader.
        :param base_founds: some founds to start trading
        """
        self.founds = {c: 0 for c in currencies}
        if base_founds is not None:
            for cur, value in base_founds.items():
                if self._check_in_currencies(cur):
                    self.founds[cur] += value

    def __getitem__(self, currency) -> float:
        return self.founds[currency]

    def print_all(self):
        for cur in self.currencies:
            print(f"{cur}\t{self[cur]}")

    def trade(self, c1: str, c2: str, amount: float, exchange: float):
        """
        Trade from currency 1 to currency 2
        :param c1: currency 1
        :param c2: currency 2
        :param amount: amount of currency 1 that will be convert in currency 2 with the exchange rate of exchange
        :param exchange: the exchange rate : c1 = exchange * c2
        :return: the trading success or fail (bool)
        """
        if self._check_in_currencies(c1) and self._check_in_currencies(c2):
            if self[c1] >= amount:
                self.founds[c1] -= amount
                self.founds[c2] += amount*exchange
                return True

    # Properties

    @property
    def currencies(self):
        return self.founds.keys()

    # Private

    def _check_in_currencies(self, key):
        if key not in self.currencies:
            raise AttributeError(f"currencie in founds not recognized :\n\t{key} not in {self.currencies}")
        else:
            return True
