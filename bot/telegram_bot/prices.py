from telegram import Update
from telegram.ext import ConversationHandler
from .common import format_offers_message
from bot.binance_api import get_offers

# Define the states used for the /prices conversation
(CRYPTO, FIAT, ORDER_TYPE) = range(3)


async def start_prices(update: Update, context) -> int:
    await update.message.reply_text("Please enter the crypto asset (e.g., USDT, BTC):")
    return CRYPTO


async def get_crypto(update: Update, context) -> int:
    context.user_data['asset'] = update.message.text.upper()
    await update.message.reply_text("Please enter the fiat asset (e.g., USD, EUR):")
    return FIAT


async def get_fiat(update: Update, context) -> int:
    context.user_data['fiat'] = update.message.text.upper()
    await update.message.reply_text("Is this alert for a 'BUY' or 'SELL' order?")
    return ORDER_TYPE


async def get_order_type(update: Update, context) -> int:
    context.user_data['order_type'] = update.message.text.upper()

    offers = await get_offers(
        context.user_data['asset'],
        context.user_data['fiat'],
        context.user_data['order_type']
    )
    offers_message = format_offers_message(offers, context)

    await update.message.reply_text(offers_message)
    return ConversationHandler.END

