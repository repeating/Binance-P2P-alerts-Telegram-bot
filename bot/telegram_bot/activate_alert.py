from telegram import Update
from telegram.ext import CallbackContext
from bot.alerts.alert_manager import AlertManager

alert_manager = AlertManager()


async def activate_alert(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    alert_id = int(context.args[0]) if context.args else None

    if alert_id is None:
        await update.message.reply_text('Please provide the ID of the alert you wish to activate. Usage: /activate_alert <alert_id>')
        return

    alert = alert_manager.alerts.get(alert_id)
    if alert:
        print(alert.user_id, user_id, alert.user_id == user_id, type(alert.user_id), type(user_id))
        if alert.user_id == user_id:
            await alert_manager.activate_alert(alert_id)
            message = f"Alert {alert_id} has been activated."
        else:
            message = f"Alert {alert_id} does not belong to user {user_id}."
    else:
        message = "Alert does not exist!"

    await update.message.reply_text(message)
