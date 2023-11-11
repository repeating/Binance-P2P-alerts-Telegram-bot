from telegram import Update
from telegram.ext import CallbackContext
from bot.alerts.alert_manager import AlertManager

alert_manager = AlertManager()


async def inactivate_alert(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    alert_id = int(context.args[0]) if context.args else None

    if alert_id is None:
        await update.message.reply_text('Please provide the ID of the alert you wish to inactivate.\nUsage: /inactivate_alert <alert_id>')
        return

    alert = alert_manager.alerts.get(alert_id)
    if alert:
        if alert.user_id == user_id:
            await alert_manager.inactivate_alert(alert_id)
            message = f"Alert {alert_id} has been inactivated."
        else:
            message = f"Alert {alert_id} does not belong to user {user_id}."
    else:
        message = "Alert does not exist!"

    await update.message.reply_text(message)
