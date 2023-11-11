from secret import TELEGRAM_TOKEN
from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.ext import Application
from bot.telegram_bot import add_alert, prices
from .common import *
from .show_alerts import *
from .remove_alert import *
from .inactivate_alert import *
from .activate_alert import *

# Define conversation states
(CRYPTO, FIAT, ORDER_TYPE, PRICE, REMOVE_ALERT) = range(5)


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_error_handler(error)

    # Define and add conversation handler for the /prices command
    prices_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prices', prices.start_prices)],
        states={
            prices.GET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_crypto)],
            prices.GET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_fiat)],
            prices.GET_ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_order_type)],
            prices.GET_PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, prices.get_payment_method)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(prices_conv_handler)

    # Define and add conversation handler for the /add_alert command
    add_alert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_alert', add_alert.start_add_alert)],
        states={
            add_alert.GET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_crypto)],
            add_alert.GET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_fiat)],
            add_alert.GET_ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_order_type)],
            add_alert.GET_PAYMENT_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_payment_method)],
            add_alert.GET_THRESHOLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_alert.get_threshold)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(add_alert_conv_handler)

    # Define and add command handler for the /show_alerts command
    show_alerts_handler = CommandHandler('show_alerts', show_alerts)
    application.add_handler(show_alerts_handler)

    # Define and add command handler for the /remove_alert command
    remove_alert_handler = CommandHandler('remove_alert', remove_alert)
    application.add_handler(remove_alert_handler)

    # Define and add command handler for the /inactivate_alert command
    inactivate_alert_handler = CommandHandler('inactivate_alert', inactivate_alert)
    application.add_handler(inactivate_alert_handler)

    # Define and add command handler for the /inactivate_alert command
    inactivate_alert_handler = CommandHandler('inactivate_alert', inactivate_alert)
    application.add_handler(inactivate_alert_handler)

    # Define and add command handler for the /activate_alert command
    activate_alert_handler = CommandHandler('activate_alert', activate_alert)
    application.add_handler(activate_alert_handler)

    # Run the bot indefinitely
    print('Running bot...')
    application.run_polling()
