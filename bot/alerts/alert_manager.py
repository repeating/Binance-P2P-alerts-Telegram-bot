import asyncio
from itertools import count
from . import Alert
from bot.database import Database


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AlertManager(metaclass=Singleton):
    def __init__(self):
        self.lock = asyncio.Lock()  # Use an asyncio Lock instead of threading.Lock
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.start_checking())
        self.db = Database('alerts.db')  # Initialize the Database class
        self.db.init_db()  # Ensure the database is set up
        self.alerts = self.db.load_alerts()
        start_id = 1 + max([0] + [alert.alert_id for alert in self.alerts.values()])
        self._id_generator = count(start=start_id)  # Unique ID generator

    async def add_alert(self, user_id, asset, fiat, trade_type, threshold_price, payment_method):
        async with self.lock:
            alert_id = next(self._id_generator)
            alert = Alert(alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method)
            self.db.insert_alert(alert)
            self.alerts[alert_id] = alert
            return alert_id, alert.link

    async def remove_alert(self, alert_id):
        async with self.lock:
            del self.alerts[alert_id]
            self.db.delete_alert(alert_id)

    async def inactivate_alert(self, alert_id):
        async with self.lock:
            alert = self.alerts.get(alert_id)
            alert.active = False

    async def activate_alert(self, alert_id):
        async with self.lock:
            alert = self.alerts.get(alert_id)
            alert.active = True

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

    async def start_checking(self, interval=1):
        """
        Start the asynchronous loop that checks alerts.
        """
        while True:
            await self.check_alerts()
            await asyncio.sleep(interval)
