"""
Trader class with example

@date: 16/07/2019
@author: Quentin Lieumont
"""
import copy


class Trader:
    """
    The trader class which can sell and buy a list of currencies with a given exchange rate
    """

    def __init__(
        self, currencies: list, base_founds: dict = None, trading_price: float = 0
    ):
        """
        Basic initialisation
        :param currencies: all currencies that can be hold by the trader.
        :param base_founds: some founds to start trading
        """
        self.trading_price = trading_price
        self.founds = {c: 0 for c in currencies}
        if base_founds is not None:
            for cur, value in base_founds.items():
                if self._check_in_currencies(cur):
                    self.founds[cur] += value
        self._history = [copy.deepcopy(self.founds)]

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
        """
        if self._check_in_currencies(c1) and self._check_in_currencies(c2):
            self.founds[c1] -= amount + self.trading_price
            self.founds[c2] += amount * exchange
            self.history.append(copy.deepcopy(self.founds))

    # Properties

    @property
    def currencies(self):
        return self.founds.keys()

    @property
    def history(self):
        return self._history

    # Private

    def _check_in_currencies(self, key):
        if key not in self.currencies:
            raise AttributeError(
                f"Currency in founds not recognized :\n\t{key} not in {self.currencies}"
            )
        else:
            return True


if __name__ == "__main__":
    print("Trader class manipulation :")

    print("")
    print('>>> list_of_coins = ["USD","BTC"]')
    print('>>> starting_founds = {"a": 2}')
    print(">>> trader = Trader(list_of_coins,starting_founds)")
    print(">>> trader.print_all()")
    print("")

    list_of_coins = ["USD", "BTC"]
    starting_founds = {"USD": 2000}
    trader = Trader(list_of_coins, starting_founds, trading_price=10)
    trader.print_all()

    print("")
    print('>>> trader.trade("USD", "BTC", 1, 100)')
    print(">>> trader.print_all()")
    print("")

    trader.trade("USD", "BTC", 1000, 1 / 1000)
    trader.print_all()
