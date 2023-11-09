from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from bot.alert_manager import AlertManager

alert_manager = AlertManager()


async def inactivate_alert(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    alert_id = int(context.args[0]) if context.args else None

    if alert_id is None:
        await update.message.reply_text('Please provide the ID of the alert you wish to inactivate. Usage: /inactivate_alert <alert_id>')
        return

    # Get the alert from the alert manager
    alert = alert_manager.alerts.get(alert_id)

    # Check if the alert exists and belongs to the user
    if alert and alert.user_id == user_id:
        alert.active = False
        await update.message.reply_text(f'Alert {alert_id} has been inactivated.')
    else:
        await update.message.reply_text(f'No alert found with ID {alert_id}.')
