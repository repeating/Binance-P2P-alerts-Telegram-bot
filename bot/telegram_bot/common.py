import requests
from secret import TELEGRAM_TOKEN
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
    message += f"\nhttps://p2p.binance.com/en/trade/{context.user_data['pay_type']}/{context.user_data['asset']}?fiat={context.user_data['fiat']}"
    message += f"\nDon't forget to uncheck 'Only show Merchant Ads'"
    return message


def send_telegram_message(user_id, message):
    """
    Send a message to a user from a Telegram bot.

    Parameters:
    user_id (str): Unique identifier for the target user or username of the target channel.
    message (str): Text of the message to be sent.

    Returns:
    dict: Response from the Telegram API.
    """
    # Telegram API endpoint for sending messages
    send_message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    # Parameters for the API request
    params = {
        'chat_id': user_id,
        'text': message
    }

    # Making the request to the Telegram API
    response = requests.post(send_message_url, params=params)

    # Returning the response as a Python dictionary
    return response.json()
