# Binance P2P alerts Telegram Bot 
![Python 3.9.6](https://img.shields.io/badge/python-3.9.6-blue.svg) ![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

This repository contains a Telegram bot, [@binance_p2p_alertsbot](https://t.me/binance_p2p_alertsbot), that interacts with the Binance P2P platform. It allows users to fetch the latest prices and set price alerts directly through Telegram.

## Features

- `/prices`: Retrieves the top 5 offers for a specified crypto and fiat asset pair on Binance P2P. It prompts the user to enter the details of the crypto asset, fiat currency, and order type (buy/sell), then displays the best available offers.

- `/show_alerts`: Lists all active price alerts set by the user, showing details such as asset type, fiat currency, price threshold, and whether each alert is active or inactive.

- `/add_alert`: Sets up a new price alert for Binance P2P. The bot will ask for the crypto asset, fiat asset, order type, threshold price, and payment type, then monitors the prices and notifies the user when conditions are met.

- `/remove_alert`: Deletes a specified price alert. The user provides the ID of the alert they wish to remove.

- `/inactivate_alert`: Temporarily disables a specified alert without deleting it. This can be used to pause alerts during times of low trading activity.

- `/activate_alert`: Reactivates a specified price alert that was previously inactivated.

- `/cancel`: Cancels the current conversation or command input, allowing the user to start over or choose a different action.

## Setup

With Docker, setting up the bot is straightforward:

1. Clone the repository.
2. Run `docker-compose build` to build the Docker container.
3. Run `docker-compose up` to start the bot.

Ensure you have a `secret.py` file with your Telegram Bot Token `TELEGRAM_TOKEN = <token>` before starting the bot.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for bugs, feature requests, or other concerns.

## License

This project is open-sourced under the [MIT License](LICENSE).
