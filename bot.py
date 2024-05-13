import asyncio
import logging
import os

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable is not set")

bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()

file_ids = []


async def send_exchange_rate_to_user(message: types.Message) -> None:
    """
    Sends the exchange rate data to the user in the form of an Excel file.
    """
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    file_name = f"exchange_rates_{today}.xlsx"
    excel_file = FSInputFile(file_name)
    result = await message.answer_document(excel_file, caption="Exchange rates excel")
    file_ids.append(result.document.file_id)


@dp.message(Command("get_exchange_rate"))
async def send_exchange_rate(message: types.Message) -> None:
    try:
        await send_exchange_rate_to_user(message)
    except Exception as e:
        logging.error(f"Error sending exchange rate: {e}")
        await message.answer("An error occurred while fetching the exchange rates.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
