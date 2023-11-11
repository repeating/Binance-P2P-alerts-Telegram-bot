from telegram.ext import ConversationHandler
from telegram import Update


async def cancel(update: Update, context) -> int:
    await update.message.reply_text('Conversation canceled.')
    return ConversationHandler.END


async def error(update: Update, context):
    print(f'Update {update} caused error {context.error}')
