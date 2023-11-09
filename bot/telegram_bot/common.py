from telegram.ext import ConversationHandler
from telegram import Update


async def cancel(update: Update, context) -> int:
    await update.message.reply_text('Conversation canceled.')
    return ConversationHandler.END


async def error(update: Update, context):
    print(f'Update {update} caused error {context.error}')


def format_offers_message(offers, context):
    message = "Top 5 offers:\n\n"
    for offer in offers:
        message += f"Price: {offer['price']} {context.user_data['fiat']}, "
        message += f"Min: {offer['min_amount']}, Max: {offer['max_amount']}\n"
    message += f"\nhttps://p2p.binance.com/en/trade/{context.user_data['order_type']}/{context.user_data['asset']}?fiat={context.user_data['fiat']}"
    message += f"\nDon't forget to uncheck 'Only show Merchant Ads'"
    return message
