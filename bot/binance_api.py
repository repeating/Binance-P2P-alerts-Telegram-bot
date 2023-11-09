import requests
import pprint

# Binance P2P API endpoint
BINANCE_P2P_API_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


def to_float(s):
    if s is None:
        return None
    else:
        return float(s)


def get_offers(asset: str, fiat: str, trade_type: str, rows: int = 3, page: int = 1, trans_amount: str = None,
               pay_type: str = "WISE") -> dict:
    """
    Fetch the best offers from Binance P2P.

    :param asset: Cryptocurrency asset, e.g., 'USDT', 'BTC'.
    :param fiat: Fiat currency, e.g., 'USD', 'EUR'.
    :param trade_type: Trade type, either 'BUY' or 'SELL'.
    :param rows: Number of offers to retrieve, default is 3.
    :param page: Page number for pagination, default is 1.
    :param trans_amount: Transaction amount for filtering offers.
    :param pay_type: payment type, default is "WISE".
    :return: List of offers from Binance P2P.
    """
    data = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": 'true',  # Assuming this should always be true for more reliable offers.
        "page": page,
        "payTypes": [pay_type],
        "publisherType": None,  # Assuming we don't filter by publisher type.
        "rows": rows,
        "tradeType": trade_type.upper(),
        "transAmount": trans_amount
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BINANCE_P2P_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        offers_data = response.json().get('data', [])
        offers = []
        for item in offers_data:
            adv = item.get('adv', {})
            offer = {
                'price': to_float(adv.get('price')),
                'min_amount': to_float(adv.get('minSingleTransAmount')),
                'max_amount': to_float(adv.get('maxSingleTransAmount'))
            }
            offers.append(offer)
        return offers
    else:
        raise Exception(f"Error fetching offers from Binance P2P: {response.status_code} - {response.text}")


# Example usage:
if __name__ == "__main__":
    # Fetch best offers for USDT/NGN for a SELL trade
    offers = get_offers('USDT', 'USD', 'BUY')
    pprint.pprint(offers, indent=2)
