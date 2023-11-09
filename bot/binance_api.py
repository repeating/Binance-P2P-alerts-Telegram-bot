import pprint
import aiohttp
import asyncio

# Binance P2P API endpoint
BINANCE_P2P_API_URL = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


def to_float(s):
    if s is None:
        return None
    else:
        return float(s)


async def get_offers(asset: str, fiat: str, trade_type: str, rows: int = 5, page: int = 1, trans_amount: str = None,
               pay_type: str = "WISE") -> dict:
    """
    Fetch the best offers from Binance P2P.

    :param asset: Cryptocurrency asset, e.g., 'USDT', 'BTC'.
    :param fiat: Fiat currency, e.g., 'USD', 'EUR'.
    :param trade_type: Trade type, either 'BUY' or 'SELL'.
    :param rows: Number of offers to retrieve, default is 5.
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
    # Fetch best offers for USDT/USD for a BUY trade
    offers = await get_offers('USDT', 'USD', 'BUY')
    pprint.pprint(offers, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
