from telegram import Update
from telegram.ext import CallbackContext
from bot.alerts.alert_manager import AlertManager

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
        message += (f"<b>ID</b>: {alert.alert_id}\n\n"
                    f"{alert.asset}\{alert.fiat}\n"
                    f"<b>Type</b>: {alert.trade_type}\n"
                    f"<b>Threshold</b>: {alert.threshold_price}\n"
                    f"<b>Payment Type</b>: {alert.payment_method}\n"
                    f"<b>Status</b>: {status}\n")
        if i < len(user_alerts) - 1:
            message += '\n-------\n\n'

    await update.message.reply_text(message, parse_mode='HTML')
