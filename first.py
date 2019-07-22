"""
First try, read the README.md

@date: 16/07/2019
@author: Quentin Lieumont
"""
from matplotlib import pyplot as plt
import copy
from trader import Trader
import numpy as np


class BTCHistory:
    """
    The history class that remember actions and opportunities
    """

    def __init__(self, start, colors=None):
        if colors is None:
            self.colors = ["b", "r", "k"]
        else:
            self.colors = colors
        self.labels = ["USD", "BTC", "USD vs BTC"]
        self._prices_history = [dict(zip(self.labels, [0, 1, start]))]

    def update_prices(self, founds: dict, change: float) -> None:
        self._prices_history.append({**founds, **{self.labels[2]: change}})

    @property
    def plot(self) -> plt.Figure:
        # noinspection PyTypeChecker
        fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)

        for i in range(3):
            axs[i].plot(
                [e[self.labels[i]] for e in self._prices_history],
                "+--",
                color=self.colors[i],
            )
            axs[i].set_ylabel(self.labels[i])

        return fig

    @property
    def result(self):
        return self._prices_history[-1]["USD"]


class FirstBTCTrader(Trader):

    btc_price: float
    obj: float
    step: float
    price_history: BTCHistory

    def __init__(self, obj: float, step: float):
        """
        :param obj: in USD
        :param step: in USD
        """
        self.obj = obj
        self.step = step
        self.current_step = 0
        self.price_history = BTCHistory(self.obj)
        super().__init__(["USD", "BTC"], {"BTC": 1})

    def update(self, btc_price: float) -> None:
        self.btc_price = btc_price

    def run(self) -> None:
        if self._check_block():
            self.got_to_obj()
        else:
            pass

    def got_to_obj(self) -> None:
        goal = self.obj / self.btc_price
        # print(f"{goal} BTC = {goal*self.btc_price} USD")
        delta = goal - self.founds["BTC"]
        self.trade("USD", "BTC", delta, self.btc_price)
        self.price_history.update_prices(self.founds, self.btc_price)

    def plot_history(self) -> None:
        self.price_history.plot.show()

    def _check_block(self) -> bool:
        middle = self.obj + self.current_step * self.step
        if self.btc_price >= middle + self.step:
            self.current_step += 1
            return True
        elif self.btc_price <= middle - self.step:
            self.current_step -= 1
            return True
        else:
            return False

    @property
    def result(self):
        return self.price_history.result


def test_trader(prices: list, step: float, start: float = 1000):
    trader = FirstBTCTrader(start, step)

    for price in prices:
        trader.update(price)
        trader.run()
    trader.got_to_obj()

    return trader.result


if __name__ == "__main__":
    prices = list(range(1000, 1500)) + list(range(1500, 1000, -1))
    steps = range(50, 650, 5)
    result = [test_trader(prices, st) for st in steps]

    fig, ax = plt.subplots()
    ax.plot(steps, result, ".k")
    fig.show()
