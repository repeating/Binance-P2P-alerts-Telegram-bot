import pprint
import aiohttp
import asyncio
from bot.utils import to_float
from typing import List

# Binance P2P API endpoint
BINANCE_P2P_API_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


def get_link(fiat: str, asset: str, payment_method: str, order_type: str):
    """
    Get the link to the offers from Binance P2P.

    :param asset: Cryptocurrency asset, e.g., 'USDT', 'BTC'.
    :param fiat: Fiat currency, e.g., 'USD', 'EUR'.
    :param payment_method: payment type, default is "Wise".
    :param order_type: Order type, either 'Buy' or 'Sell'.
    :return: str, link to the offers from Binance P2P.
    """
    url = f"https://p2p.binance.com/en/trade/{order_type}/{payment_method}/{asset}?fiat={fiat}"
    return url


async def get_offers(asset: str, fiat: str, trade_type: str, payment_method: str,
                     rows: int = 5, page: int = 1, trans_amount: str = None) -> List[dict]:
    """
    Fetch the best offers from Binance P2P.

    :param asset: Cryptocurrency asset, e.g., 'USDT', 'BTC'.
    :param fiat: Fiat currency, e.g., 'USD', 'EUR'.
    :param trade_type: Trade type, either 'Buy' or 'Sell'.
    :param rows: Number of offers to retrieve, default is 5.
    :param page: Page number for pagination, default is 1.
    :param trans_amount: Transaction amount for filtering offers.
    :param payment_method: payment type, default is "Wise".
    :return: List of offers from Binance P2P.
    """
    data = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": 'true',  # Assuming this should always be true for more reliable offers.
        "page": page,
        "payTypes": [payment_method],
        "publisherType": None,  # Assuming we don't filter by publisher type.
        "rows": rows,
        "tradeType": trade_type,
        "transAmount": trans_amount
    }
    headers = {
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(BINANCE_P2P_API_URL, json=data, headers=headers) as response:
            if response.status == 200:
                response_json = await response.json()
                offers_data = response_json.get('data', [])
                offers = [{
                    'price': to_float(adv.get('price')),
                    'min_amount': to_float(adv.get('minSingleTransAmount')),
                    'max_amount': to_float(adv.get('maxSingleTransAmount'))
                } for item in offers_data for adv in [item.get('adv', {})]]
                return offers
            else:
                raise Exception(f"Error fetching offers from Binance P2P: {response.status} - {await response.text()}")


async def main():
    # Fetch best offers for USDT/USD for a Buy trade
    offers = await get_offers('USDT', 'USD', 'Buy')
    pprint.pprint(offers, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
