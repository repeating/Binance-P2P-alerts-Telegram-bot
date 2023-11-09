from telegram.ext import Application
from secret import TELEGRAM_TOKEN
from .common import *
from .prices import *
from .set_alert import *

# Define conversation states
(CRYPTO, FIAT, ORDER_TYPE, PRICE, REMOVE_ALERT) = range(5)

# Implement set_alert handlers...
# Implement remove_alert handlers...


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_error_handler(error)

    # Define the conversation handler for the /prices command
    prices_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prices', start_prices)],
        states={
            CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_crypto)],
            FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fiat)],
            ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_order_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers to the application
    application.add_handler(prices_conv_handler)

    # Create the conversation handler for the /set_alert command
    set_alert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('set_alert', start_set_alert)],
        states={
            SET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_crypto)],
            SET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_fiat)],
            SET_ORDER_TYPE: [MessageHandler(filters.Regex('^(BUY|SELL)$'), set_order_type)],
            SET_THRESHOLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_threshold)],
            SET_PAY_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_pay_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add handlers to the application
    application.add_handler(set_alert_conv_handler)

    # ... Add handlers for /set_alert and /remove_alert ...

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

