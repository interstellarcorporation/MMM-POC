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
            self.colors = ['b', 'r', 'k']
        else:
            self.colors = colors
        self.labels = ["USD", "BTC", "USD vs BTC"]
        self._prices_history = [dict(zip(self.labels, [0, 1, start]))]

    def update_prices(self, founds: dict, change: float) -> None:
        self._prices_history.append({**founds, **{self.labels[2]: change}})

    @property
    def plot(self) -> plt.Figure:
        # noinspection PyTypeChecker
        fig, axs = plt.subplots(
            nrows=3,
            ncols=1,
            sharex=True
        )

        for i in range(3):
            axs[i].plot([e[self.labels[i]] for e in self._prices_history], '+--', color=self.colors[i])
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
        goal = self.obj/self.btc_price
        # print(f"{goal} BTC = {goal*self.btc_price} USD")
        delta = goal - self.founds["BTC"]
        self.trade("USD", "BTC", delta, self.btc_price)
        self.price_history.update_prices(self.founds, self.btc_price)

    def plot_history(self) -> None:
        self.price_history.plot.show()

    def _check_block(self) -> bool:
        middle = self.obj + self.current_step*self.step
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


def test_trader(step: float, delta: float, start: float = 1000, market_step: float = 1):
    trader_up = FirstBTCTrader(start, step)
    trader_do = FirstBTCTrader(start, step)
    up = np.concatenate((np.arange(start, start + delta, market_step), np.arange(start + delta, start, -1 * market_step)))
    do = np.concatenate((np.arange(start, start - delta, -1 * market_step), np.arange(start - delta, start, market_step)))

    for i in range(len(up)):
        trader_up.update(up[i])
        trader_do.update(do[i])
        trader_up.run()
        trader_do.run()
    trader_up.got_to_obj()
    trader_do.got_to_obj()

    return trader_up.result, trader_do.result


if __name__ == '__main__':
    for i in range(50, 550, 50):
        print(test_trader(i, 500))
