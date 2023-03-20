class ETF:
    """
    Class that describes an ETF (Exchange Traded Fund)
    """

    def __init__(self, contract_id, symbol, full_name, price_history):
        """
        Constructor method for an ETF
        :param contract_id: integer, id of the contract fo identifying it on IBKR
        :param symbol: string, symbol of the ETF
        :param full_name: string, full name of the ETF
        :param price_history: list of dictionaries,
                              each dictionary has a timestamp (double) and a close price (double) for a different day
        """

        self._contract_id = contract_id
        self._symbol = symbol
        self._full_name = full_name
        self._price_history = price_history

    def get_contract_id(self):
        return self._contract_id

    def get_symbol(self):
        return self._symbol

    def set_symbol(self, value):
        self._symbol = value

    def get_full_name(self):
        return self._full_name

    def set_full_name(self, value):
        self._full_name = value

    def get_price_history(self):
        return self._price_history

    def set_price_history(self, value):
        self._price_history = value
