from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from bot.alert_manager import AlertManager

alert_manager = AlertManager()


async def remove_alert(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    alert_id = int(context.args[0]) if context.args else None

    if alert_id is None:
        await update.message.reply_text('Please provide the ID of the alert you wish to remove. Usage: /remove_alert <alert_id>')
        return

    success, message = await alert_manager.remove_alert(user_id, alert_id)
    await update.message.reply_text(message)