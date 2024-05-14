# Exchange Rate Telegram Bot

_This Telegram bot fetches the current exchange rate from a website, saves it to a database and an Excel file, and sends it to users upon request._

## Files

1. **bot.py**: Contains the Telegram bot implementation using the aiogram library. Handles user requests and sends exchange rate data.
2. **database.py**: Defines the database model using SQLAlchemy for storing exchange rate information.
3. **parser.py**: Fetches exchange rates from a website, saves them to a database and an Excel file periodically.

## Setup

1. Install required libraries:

`pip install aiogram pandas sqlalchemy requests lxml python-dotenv`

2. Create a .env file in the project directory with the following content:

`BOT_TOKEN=your_telegram_bot_token`

3. Run database.py to initialize the SQLite database:

`python database.py`

4. Run parser.py in the background to fetch and save exchange rates periodically:

`python parser.py &`

5. Run bot.py to start the Telegram bot:

`python bot.py`

## Bot Commands

* /get_exchange_rate: Fetches and sends the latest exchange rate data in Excel format.

## Notes

The bot fetches exchange rates every hour and saves them to both the database and an Excel file named **exchange_rates_{date}.xlsx.**
Make sure to replace **your_telegram_bot_token** in the '**.env**' file with your actual Telegram bot token.