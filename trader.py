

class Trader:
    """
    The trader class which can sell and buy a list of currencies with a given exchange rate
    """
    def __init__(self, currencies: list, base_founds: dict = None):
        self.founds = {c:0 for c in currencies}
        if base_founds is not None:
            for cur, value in base_founds:
                if cur not in currencies:
                    raise AttributeError(f"currencie in founds not recognized :\n\t{cur} not in {currencies}")
                else:
                    self.founds[cur] += value

    def __getitem__(self, currency):
        return self.founds[currency]
