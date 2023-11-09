from datetime import datetime, timedelta
from bot.binance_api import get_offers
from bot.telegram_bot.common import send_telegram_message


class Alert:
    def __init__(self, alert_id, user_id, asset, fiat, trade_type, threshold_price, pay_type):
        self.alert_id = alert_id
        self.user_id = user_id
        self.asset = asset
        self.fiat = fiat
        self.trade_type = trade_type
        self.threshold_price = threshold_price
        self.pay_type = pay_type
        self.active = True
        self.last_triggered = None  # Track when the alert was last triggered
        self.trigger_interval = 15  # in minutes

    async def check_alert(self):
        """
        Check if the current offers meet the alert condition.
        """
        if self.active and (self.last_triggered is None or datetime.now() >= self.last_triggered + timedelta(minutes=self.trigger_interval)):
            offers = await get_offers(self.asset, self.fiat, self.trade_type, pay_type=self.pay_type)
            for offer in offers:
                price = float(offer['price'])
                if (self.trade_type == 'SELL' and price >= self.threshold_price) or \
                        (self.trade_type == 'BUY' and price <= self.threshold_price):
                    await self.trigger_alert(price)
                    break

    async def trigger_alert(self, price):
        """
        Trigger the alert. This should notify the user.
        """
        message = (f"Alert {self.alert_id}: {self.asset}/{self.fiat} {self.trade_type} at {price}, Pay type: {self.pay_type}\n"
                   f"https://p2p.binance.com/en/trade/{self.pay_type}/{self.asset}?fiat={self.fiat}")
        send_telegram_message(self.user_id, message)
        # Send a message to the user using the Telegram Bot API
        self.last_triggered = datetime.now()
