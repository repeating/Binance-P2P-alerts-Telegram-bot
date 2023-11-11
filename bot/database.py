import sqlite3
from bot.alerts import Alert


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def init_db(self):
        with sqlite3.connect(self.db_name) as db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    asset TEXT NOT NULL,
                    fiat TEXT NOT NULL,
                    trade_type TEXT NOT NULL,
                    threshold_price REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    active BOOLEAN NOT NULL,
                    last_triggered TIMESTAMP
                )
            ''')
            db.commit()

    def insert_alert(self, alert):
        with sqlite3.connect(self.db_name) as db:
            db.execute('''
                INSERT INTO alerts (alert_id, user_id, asset, fiat, trade_type, threshold_price, payment_method, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (alert.alert_id, alert.user_id, alert.asset, alert.fiat, alert.trade_type, alert.threshold_price, alert.payment_method, 1))
            db.commit()

    def delete_alert(self, alert_id):
        with sqlite3.connect(self.db_name) as db:
            db.execute('DELETE FROM alerts WHERE alert_id = ?', (alert_id,))
            db.commit()

    def update_last_triggered(self, alert_id, last_triggered):
        with sqlite3.connect(self.db_name) as db:
            db.execute('UPDATE alerts SET last_triggered = ? WHERE alert_id = ?', (last_triggered, alert_id))
            db.commit()

    def load_alerts(self):
        alerts = {}
        with sqlite3.connect(self.db_name) as db:
            cursor = db.execute('SELECT * FROM alerts')
            for row in cursor.fetchall():
                alert = Alert(*row[:-2])
                alert.active = row[-2]
                alert.last_triggered = row[-1]
                alerts[alert.alert_id] = alert
        return alerts
