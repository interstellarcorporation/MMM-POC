"""
First try, read the README.md

@date: 16/07/2019
@author: Quentin Lieumont
"""
from matplotlib import pyplot as plt
from trader import Trader
import numpy as np


class FirstTrader(Trader):

    btc_price: float
    obj: float
    step: float
    price_history: list

    def __init__(self, obj: float, step: float):
        """
        :param obj: in USD
        :param step: in USD
        """
        self.obj = obj
        self.step = step
        self.current_step = 0
        self.price_history = []
        super().__init__(["USD", "BTC"], {"BTC": 1})

    def update(self, btc_price: float) -> None:
        self.btc_price = btc_price
        self.price_history.append(self.btc_price)

    def run(self):
        if self._check_block():
            goal = self.obj/self.btc_price
            # print(f"{goal} BTC = {goal*self.btc_price} USD")
            delta = goal - self.founds["BTC"]
            self.trade("USD", "BTC", delta, self.btc_price)
        else:
            pass

    def plot_history(self):
        fig, ax = plt.subplots()
        usd = [e["USD"] for e in self.history]
        ax.plot(usd, label="USD")
        ax.legend()
        fig.show()

    def _check_block(self) -> bool:
        middle = self.obj + self.current_step*self.step
        if self.btc_price > middle + self.step:
            self.current_step += 1
            return True
        elif self.btc_price < middle - self.step:
            self.current_step -= 1
            return True
        else:
            return False


if __name__ == '__main__':
    trader = FirstTrader(1000, 200)
    up = np.concatenate((np.arange(1000, 2500, 100), np.arange(2500, 900, -100)))
    do = np.concatenate((np.arange(1000, 600, -100), np.arange(600, 1100, 100)))

    for price in up:
        trader.update(price)
        trader.run()
        print([e["BTC"] for e in trader.history])

    trader.plot_history()
