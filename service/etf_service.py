import threading

import requests

from model.exceptions.service_exception import ServiceException
from utils.data_preprocessing import get_ibkr_price_history_for_etfs


class ETFService:

    def __init__(self, repository):
        self._repository = repository
        self.ibkr_tickle()
        self.check_for_latest_etf_data()

    def ibkr_tickle(self):
        """
        Keep the connection to IBKR open
        Make a request every 5 minutes
        :return: nothing
        """

        threading.Timer(300.0, self.ibkr_tickle).start()
        response = requests.post("https://localhost:5000/v1/api/tickle", verify=False)

        if not response.ok:
            raise ServiceException("IBKR server did not respond when trying to call /tickle!")

    def check_for_latest_etf_data(self):
        """
        Check for new ETF price data every 24h
        :return: nothing
        """

        threading.Timer(86400.0, self.check_for_latest_etf_data).start()
        etf_list = get_ibkr_price_history_for_etfs()

        self._repository.clear_repository_collection()
        for etf in etf_list:
            self._repository.save(etf)
