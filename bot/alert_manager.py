import asyncio
from datetime import datetime, timedelta
from itertools import count
from binance_api import get_offers

# Unique ID generator
_id_generator = count(start=1)


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
        print(datetime.now(), f"Alert {self.alert_id} for user {self.user_id}: {self.asset}/{self.fiat} {self.trade_type} at {price}, Pay type: {self.pay_type}")
        # Send a message to the user using the Telegram Bot API
        self.last_triggered = datetime.now()


class AlertManager:
    def __init__(self):
        self.alerts = {}
        self.lock = asyncio.Lock()  # Use an asyncio Lock instead of threading.Lock

    async def add_alert(self, user_id, asset, fiat, trade_type, threshold_price, pay_type):
        async with self.lock:
            alert_id = next(_id_generator)
            alert = Alert(alert_id, user_id, asset, fiat, trade_type, threshold_price, pay_type)
            self.alerts[alert_id] = alert
            return alert_id

    async def remove_alert(self, user_id, alert_id) -> (bool, str):
        async with self.lock:
            alert = self.alerts.get(alert_id)
            if alert:
                if alert.user_id == user_id:
                    del self.alerts[alert_id]
                    return True, f"Alert {alert_id} has been removed."
                else:
                    return False, f"Alert {alert_id} does not belong to user {user_id}."
            else:
                return False, 'Alert does not exist!'

    async def check_alerts(self):
        """
        Check all active alerts concurrently against current offers.
        """
        tasks = []
        for alert_id, alert in list(self.alerts.items()):
            if alert.active:
                # Schedule the alert check for concurrent execution
                tasks.append(alert.check_alert())

        # Use asyncio.gather to run tasks concurrently
        await asyncio.gather(*tasks)

    async def start_checking(self, interval=15):
        """
        Start the asynchronous loop that checks alerts.
        """
        while True:
            await self.check_alerts()
            await asyncio.sleep(interval)


# Example usage
async def main():
    alert_manager = AlertManager()
    asyncio.create_task(alert_manager.start_checking())

    alert_id = await alert_manager.add_alert(user_id='Alex', asset='USDT', fiat='USD', trade_type='BUY', threshold_price=1.02, pay_type='WISE')
    alert_id = await alert_manager.add_alert(user_id='Alex', asset='USDT', fiat='USD', trade_type='BUY', threshold_price=1.06, pay_type='REVOLUT')
    alert_id = await alert_manager.add_alert(user_id='Alex', asset='USDT', fiat='USD', trade_type='BUY', threshold_price=1.07, pay_type='BANK')

    alert_id = await alert_manager.add_alert(user_id='Fadi', asset='USDT', fiat='USD', trade_type='SELL', threshold_price=0.92, pay_type='WISE')
    alert_id = await alert_manager.add_alert(user_id='Fadi', asset='USDT', fiat='USD', trade_type='SELL', threshold_price=0.96, pay_type='REVOLUT')
    alert_id = await alert_manager.add_alert(user_id='Fadi', asset='USDT', fiat='USD', trade_type='SELL', threshold_price=0.97, pay_type='BANK')

    # Run indefinitely
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
