from telegram import Update
from telegram.ext import CallbackContext
from bot.alert_manager import AlertManager

alert_manager = AlertManager()


async def show_alerts(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_alerts = [alert for alert in alert_manager.alerts.values() if alert.user_id == user_id]

    if not user_alerts:
        await update.message.reply_text('You have no alerts set.')
        return

    message = 'Your alerts:\n\n'
    for i, alert in enumerate(user_alerts):
        status = 'Active' if alert.active else 'Inactive'
        message += (f"ID: {alert.alert_id}\n"
                    f"Asset: {alert.asset}\n"
                    f"Fiat: {alert.fiat}\n"
                    f"Type: {alert.trade_type}\n"
                    f"Threshold: {alert.threshold_price}\n"
                    f"Payment Type: {alert.pay_type}\n"
                    f"Status: {status}\n")
        if i < len(user_alerts) - 1:
            message += '-------\n'

    await update.message.reply_text(message)
