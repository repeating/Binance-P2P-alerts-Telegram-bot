from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from bot.alert_manager import AlertManager

# Define the states used for the /set_alert conversation
(SET_CRYPTO, SET_FIAT, SET_ORDER_TYPE, SET_THRESHOLD, SET_PAY_TYPE) = range(5)

alert_manager = AlertManager()


async def start_set_alert(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please enter the crypto asset for the alert (e.g., USDT, BTC):")
    return SET_CRYPTO


async def set_crypto(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_asset'] = update.message.text.upper()
    await update.message.reply_text("Please enter the fiat asset for the alert (e.g., USD, EUR):")
    return SET_FIAT


async def set_fiat(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_fiat'] = update.message.text.upper()
    await update.message.reply_text("Is this alert for a 'BUY' or 'SELL' order?")
    return SET_ORDER_TYPE


async def set_order_type(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_order_type'] = update.message.text.upper()
    await update.message.reply_text("Please enter the threshold price for the alert:")
    return SET_THRESHOLD


async def set_threshold(update: Update, context: CallbackContext) -> int:
    # Validate the threshold price input
    try:
        threshold_price = float(update.message.text)
        context.user_data['alert_threshold'] = threshold_price
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a valid number for the threshold price.")
        return SET_THRESHOLD

    await update.message.reply_text("Please enter the payment type for the alert (e.g., WISE, BANK):")
    return SET_PAY_TYPE


async def set_pay_type(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_pay_type'] = update.message.text.upper()
    # Add the alert to the AlertManager
    user_id = update.effective_user.id
    alert_id = await alert_manager.add_alert(
        user_id,
        context.user_data['alert_asset'],
        context.user_data['alert_fiat'],
        context.user_data['alert_order_type'],
        context.user_data['alert_threshold'],
        context.user_data['alert_pay_type']
    )
    await update.message.reply_text(f"Alert {alert_id} set successfully!")
    return ConversationHandler.END
