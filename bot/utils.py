import requests
from secret import TELEGRAM_TOKEN


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
        'text': message,
        'parse_mode': 'HTML'
    }

    # Making the request to the Telegram API
    response = requests.post(send_message_url, params=params)

    # Returning the response as a Python dictionary
    return response.json()


def to_float(s):
    if s is None:
        return None
    else:
        return float(s)


def format_table(data, columns, html=False):
    """
    Formats a 2D list into a string representation of a table with fixed column widths.
    Optionally formats the output as HTML with bold column names.

    :param data: A 2D list of data.
    :param columns: A list of column names.
    :param html: A boolean indicating whether to format output as HTML.
    :return: A string representing the data in table format.
    """
    # Determine the maximum width for each column
    col_widths = [max(len(str(item)) for item in column_data) for column_data in zip(*data)]

    formatted_rows = []
    for row in data:
        formatted_row = []
        for i, col in enumerate(columns):
            # Wrap column names in <b></b> if html is True
            col_name = f"<b>{col}</b>" if html else col
            # Format each item to have a fixed width, left aligned
            formatted_item = f"{col_name}: {str(row[i]).ljust(col_widths[i])}"
            formatted_row.append(formatted_item)
        formatted_rows.append(",   ".join(formatted_row))
    return "\n".join(formatted_rows)
