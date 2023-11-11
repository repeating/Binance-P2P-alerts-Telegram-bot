from datetime import datetime, timedelta
from bot.binance_api import get_offers, get_link
from bot.utils import send_telegram_message


class Alert:
    def __init__(self, alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method):
        self.alert_id = alert_id
        self.user_id = user_id
        self.asset = asset
        self.fiat = fiat
        self.trade_type = trade_type
        self.threshold_price = threshold_price
        self.payment_method = payment_method
        self.active = True
        self.last_triggered = None  # Track when the alert was last triggered
        self.trigger_interval = 15  # in minutes
        self.link = get_link(self.fiat, self.asset, self.payment_method, self.trade_type)

    async def check_alert(self):
        """
        Check if the current offers meet the alert condition.
        """
        if self.active and (self.last_triggered is None or datetime.now() >= self.last_triggered + timedelta(minutes=self.trigger_interval)):
            offers = await get_offers(self.asset, self.fiat, self.trade_type, payment_method=self.payment_method)
            for offer in offers:
                price = float(offer['price'])
                if (self.trade_type == 'Sell' and price >= self.threshold_price) or \
                        (self.trade_type == 'Buy' and price <= self.threshold_price):
                    await self.trigger_alert(price, offer['min_amount'], offer['max_amount'])
                    break

    async def trigger_alert(self, price, min_amount, max_amount):
        """
        Trigger the alert. This should notify the user.
        """
        message = (f"<b>Alert</b> {self.alert_id}:\n\n"
                   f"{self.payment_method} {self.asset}/{self.fiat} {self.trade_type} at {price}\n"
                   f"Min amount: {min_amount}, Max amount: {max_amount}\n\n"
                   f"{get_link(self.fiat, self.asset, self.payment_method, self.trade_type)}")
        send_telegram_message(self.user_id, message)
        # Send a message to the user using the Telegram Bot API
        self.last_triggered = datetime.now()
