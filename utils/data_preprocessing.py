import requests

from model.etf import ETF


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
    for key, val in etfs.items():
        request = requests.get(f"https://localhost:5000/v1/api/iserver/marketdata/history?conid={val}&period=5y&bar=1d",
                               verify=False)

        response = request.json()

        price_history = []
        for price_data in response["data"]:
            price_history.append({
                "timestamp": price_data["t"],
                "close_price": price_data["c"]
            })

        all_etfs.append(ETF(
            val,
            response["symbol"],
            response["text"],
            price_history
        ))

    return all_etfs
