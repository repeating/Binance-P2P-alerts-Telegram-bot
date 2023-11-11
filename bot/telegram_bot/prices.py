from telegram import Update
from telegram.ext import ConversationHandler
from bot.binance_api import get_offers, get_link
from bot.utils import format_table

# Define the states used for the /prices conversation
(GET_CRYPTO, GET_FIAT, GET_ORDER_TYPE, GET_PAYMENT_METHOD) = range(4)


def format_offers_message(offers, context):
    message = "<b>Top 5 offers:</b>:\n\n"

    data = []
    for offer in offers:
        data.append([f"{offer['price']} {context.user_data['fiat']}", offer['min_amount'], offer['max_amount']])
    message += format_table(data, columns=['Price', 'Min', 'Max'], html=True) + '\n'

    link = get_link(context.user_data['fiat'], context.user_data['asset'],
                    context.user_data['payment_method'], context.user_data['order_type'])
    message += (f"\n{link}\n"
                f"Don't forget to uncheck 'Only show Merchant Ads'")

    return message


async def start_prices(update: Update, context) -> int:
    await update.message.reply_text("Please enter the crypto asset (e.g., USDT, BTC):")
    return GET_CRYPTO


async def get_crypto(update: Update, context) -> int:
    context.user_data['asset'] = update.message.text.upper()
    await update.message.reply_text("Please enter the fiat asset (e.g., USD, EUR):")
    return GET_FIAT


async def get_fiat(update: Update, context) -> int:
    context.user_data['fiat'] = update.message.text.upper()
    await update.message.reply_text("Please enter the order type 'Buy' or 'Sell':")
    return GET_ORDER_TYPE


async def get_order_type(update: Update, context) -> int:
    order_type = update.message.text.capitalize()

    if order_type not in ['Buy', 'Sell']:
        await update.message.reply_text("Invalid order type. Please type 'Buy' or 'Sell':")
        return GET_ORDER_TYPE  # This will ask for the order type again

    context.user_data['order_type'] = order_type

    await update.message.reply_text("Please enter the payment type for the alert (e.g., Wise, Bank):")
    return GET_PAYMENT_METHOD


async def get_payment_method(update: Update, context) -> int:
    context.user_data['payment_method'] = update.message.text.capitalize()

    offers = await get_offers(
        context.user_data['asset'],
        context.user_data['fiat'],
        context.user_data['order_type'],
        context.user_data['payment_method']
    )
    offers_message = format_offers_message(offers, context)

    await update.message.reply_text(offers_message, parse_mode='HTML')
    return ConversationHandler.END
