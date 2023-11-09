from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.ext import Application
from secret import TELEGRAM_TOKEN
from .common import *
from .prices import *
from .set_alert import *
from .show_alerts import *
from .remove_alert import *
from .inactivate_alert import *
from .activate_alert import *

# Define conversation states
(CRYPTO, FIAT, ORDER_TYPE, PRICE, REMOVE_ALERT) = range(5)

# Implement remove_alert handlers...


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_error_handler(error)

    # Define and add conversation handler for the /prices command
    prices_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('prices', start_prices)],
        states={
            CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_crypto)],
            FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fiat)],
            ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_order_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(prices_conv_handler)

    # Define and add conversation handler for the /set_alert command
    set_alert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('set_alert', start_set_alert)],
        states={
            SET_CRYPTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_crypto)],
            SET_FIAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_fiat)],
            SET_ORDER_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_order_type)],
            SET_THRESHOLD: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_threshold)],
            SET_PAY_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_pay_type)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(set_alert_conv_handler)

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

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

