"""
First try, read the README.md

@date: 16/07/2019
@author: Quentin Lieumont
"""
from matplotlib import pyplot as plt
from usefull import plot_color, get_json
from trader import Trader


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
        _fig, _axs = plt.subplots(nrows=3, ncols=1, sharex=True)

        for i in range(3):
            _axs[i].plot(
                [e[self.labels[i]] for e in self._prices_history],
                "+--",
                color=self.colors[i],
            )
            _axs[i].set_ylabel(self.labels[i])

        return _fig

    @property
    def result(self):
        return self._prices_history[-1]["USD"]


class FirstBTCTrader(Trader):
    btc_price: float
    obj: float
    step: float
    price_history: BTCHistory

    def __init__(self, obj: float, step: float, is_debuging: bool = False, **kargs):
        """
        :param obj: in USD
        :param step: in USD
        """
        self.is_debugging = is_debuging
        self.obj = obj
        self.step = step
        self.current_step = 0
        self.price_history = BTCHistory(self.obj)
        super().__init__(["USD", "BTC"], {"BTC": 1}, **kargs)
        self.debug(f"obj={self.obj}\tstep={self.step}")

    def update(self, btc_price: float) -> None:
        self.btc_price = btc_price

    def debug(self, msg) -> None:
        if self.is_debugging:
            print(msg)

    def run(self) -> None:
        self.debug(f"Trying with {self.btc_price}")
        if self._check_block():
            self.debug("\t YES")
            self.got_to_obj()
        else:
            self.debug("\t NO")

    def got_to_obj(self) -> None:
        goal = self.obj / self.btc_price
        delta = goal - self.founds["BTC"]
        self.trade("USD", "BTC", delta, 1 / self.btc_price)
        self.price_history.update_prices(self.founds, self.btc_price)
        self.debug(f"{goal} BTC = {goal*self.btc_price} USD")
        if self.is_debugging:
            self.print_all()

    def plot_history(self) -> None:
        self.price_history.plot.show()

    def _check_block(self) -> bool:
        middle = self.obj + self.current_step * self.step
        self.debug(f"testing with {middle - self.step} - {middle + self.step}")
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


def test_trader(
    prices: list,
    start: float,
    step: float,
    debug: bool = False,
    trading_price: float = 10,
):
    trader = FirstBTCTrader(start, step, trading_price=trading_price, is_debuging=debug)

    for price in prices:
        trader.update(price)
        trader.run()
    trader.got_to_obj()

    return trader.result


def test_trader_2d(
    prices: list,
    price_range: iter,
    step_range: iter,
    nb_points: int = 20,
    trading_price: float = 10,
):
    _steps = range(
        min(step_range),
        max(step_range),
        int((max(step_range) - min(step_range)) / nb_points),
    )
    _starts = range(
        max(price_range),
        min(price_range),
        -int((max(price_range) - min(price_range)) / nb_points),
    )
    result = [
        [
            test_trader(prices, start, step, trading_price=trading_price)
            for step in _steps
        ]
        for start in _starts
    ]

    return plot_color(result, _steps, _starts)


if __name__ == "__main__":
    # _prices = list(range(1000, 1500)) + list(range(1500, 1000, -1))
    _prices = [e["price"] for e in get_json("all_prices.json")]
    _prices = _prices + list(reversed(_prices))

    fig = test_trader_2d(
        _prices, [1000, 12000], [1, 1000], nb_points=10, trading_price=0
    )
    fig.show()
