import requests

from model.etf import ETF
from model.exceptions.service_exception import ServiceException


def get_ibkr_price_history_for_etfs():
    etfs = {
        "SPY": 756733,
        "IVV": 8991352,
        "VTI": 12340041,
        "VOO": 136155102,
        "QQQ": 320227571,
        "VEA": 45444192,
        "VTV": 27638093,
        "IEFA": 123972859,
        "BND": 43645828,
        "AGG": 25985141,
        "VUG": 27638099,
        "VWO": 27684033,
        "IEMG": 115826951,
        "IJR": 9579976,
        "IJH": 9579987,
        "VIG": 38746069,
        "IWF": 8991557,
        "VXUS": 83512168,
        "VO": 27638087,
        "VYM": 41647036
    }

    all_etfs = []
    for etf_symbol, contract_id in etfs.items():
        request = requests.get(
            f"https://localhost:5000/v1/api/iserver/marketdata/history?conid={contract_id}&period=5y&bar=1d",
            verify=False
        )

        if not request.ok:
            raise ServiceException(f"Could not fetch data for {etf_symbol}")

        response = request.json()

        price_history = []
        for price_data in response["data"]:
            price_history.append({
                "timestamp": price_data["t"],
                "close_price": price_data["c"]
            })

        all_etfs.append(ETF(
            contract_id=contract_id,
            symbol=response["symbol"],
            full_name=response["text"],
            price_history=price_history
        ))

    return all_etfs
