from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from bot.alerts import AlertManager

# Define the states used for the /add_alert conversation
(GET_CRYPTO, GET_FIAT, GET_ORDER_TYPE, GET_PAYMENT_METHOD, GET_THRESHOLD) = range(5)

alert_manager = AlertManager()


async def start_add_alert(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Please enter the crypto asset for the alert (e.g., USDT, BTC):")
    return GET_CRYPTO


async def get_crypto(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_asset'] = update.message.text.upper()
    await update.message.reply_text("Please enter the fiat asset for the alert (e.g., USD, EUR):")
    return GET_FIAT


async def get_fiat(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_fiat'] = update.message.text.upper()
    await update.message.reply_text("Is this alert for a 'Buy' or 'Sell' order?")
    return GET_ORDER_TYPE


async def get_order_type(update: Update, context: CallbackContext) -> int:
    order_type = update.message.text.capitalize()
    if order_type not in ['Buy', 'Sell']:
        await update.message.reply_text("Invalid order type. Please type 'Buy' or 'Sell':")
        return GET_ORDER_TYPE  # This will ask for the order type again

    context.user_data['alert_order_type'] = order_type

    await update.message.reply_text("Please enter the payment type for the alert (e.g., Wise, Bank):")
    return GET_PAYMENT_METHOD


async def get_payment_method(update: Update, context: CallbackContext) -> int:
    context.user_data['alert_payment_method'] = update.message.text.capitalize()

    await update.message.reply_text("Please enter the threshold price for the alert:")
    return GET_THRESHOLD


async def get_threshold(update: Update, context: CallbackContext) -> int:
    # Validate the threshold price input
    try:
        threshold_price = float(update.message.text)
        context.user_data['alert_threshold'] = threshold_price
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a valid number for the threshold price.")
        return GET_THRESHOLD

    # Add the alert to the AlertManager
    user_id = update.effective_user.id
    alert_id, link = await alert_manager.add_alert(
        user_id,
        context.user_data['alert_asset'],
        context.user_data['alert_fiat'],
        context.user_data['alert_order_type'],
        context.user_data['alert_threshold'],
        context.user_data['alert_payment_method']
    )
    message = f"Alert {alert_id} set successfully!\n" \
              f"Watching offers at {link}"

    await update.message.reply_text(message)
    return ConversationHandler.END
