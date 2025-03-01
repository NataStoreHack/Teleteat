import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime, timedelta

# Masukkan token BOT Telegram Anda di sini
TELEGRAM_TOKEN = '8155485405:AAEJR88z8Lql92P0FGQ4SHo73WMhRUfpujE'

# URL halaman-halaman yang akan diambil nama token-nya
urls = [
    "https://dexscreener.com/ethereum",
    "https://dexscreener.com/solana",
    "https://dexscreener.com/base",
    "https://dexscreener.com/optimism",
    "https://dexscreener.com/arbitrum",
    "https://dexscreener.com/fantom",
    "https://dexscreener.com/bsc",
    "https://dexscreener.com/Polygon",
    "https://dexscreener.com/blast",
    "https://dexscreener.com/avalanche"
]

def get_tokens_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tokens = soup.find_all("div", class_="token-class-name")  # Sesuaikan dengan class yang sesuai di halaman web

    token_names = set()  # Gunakan set untuk menyimpan nama token unik

    for token in tokens:
        token_name = token.find("span", class_="token-name-class-name").text  # Sesuaikan dengan class yang sesuai di halaman web
        token_names.add(token_name)

    return token_names

def filter_tokens_with_same_name(urls):
    all_tokens = set()
    duplicate_tokens = set()

    for url in urls:
        tokens = get_tokens_from_url(url)
        duplicate_tokens.update(tokens.intersection(all_tokens))
        all_tokens.update(tokens)

    return duplicate_tokens

def get_tokens_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tokens = soup.find_all("div", class_="token-class-name")  # Sesuaikan dengan class yang sesuai di halaman web

    token_info = []

    for token in tokens:
        token_name = token.find("span", class_="token-name-class-name").text  # Sesuaikan dengan class yang sesuai di halaman web
        token_price = token.find("span", class_="token-price-class-name").text  # Sesuaikan dengan class yang sesuai di halaman web
        token_info.append(f"Token: {token_name}, Price: {token_price}")

    return token_info

def get_current_time_utc7():
    utc7_offset = timedelta(hours=7)
    current_time_utc = datetime.utcnow()
    current_time_utc7 = current_time_utc + utc7_offset
    return current_time_utc7.strftime("%Y-%m-%d %H:%M:%S UTC+7")

def get_top_tokens_from_urls(urls):
    all_tokens = []

    for url in urls:
        tokens = get_tokens_from_url(url)
        all_tokens.extend(tokens)

    return all_tokens

def send_top_tokens(bot: Bot, chat_id: str) -> None:
    top_tokens = get_top_tokens_from_urls(urls)
    current_time_utc7 = get_current_time_utc7()

    if top_tokens:
        message = f"Top tokens within the last 24 hours as of {current_time_utc7}:\n"
        message += "\n".join(top_tokens)
        bot.send_message(chat_id=chat_id, text=message)
    else:
        bot.send_message(chat_id=chat_id, text="No top tokens found within the last 24 hours.")

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    def start(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Hello! Use /top_tokens command to get information about top tokens within the last 24 hours.')

    def top_tokens(update: Update, context: CallbackContext) -> None:
        send_top_tokens(context.bot, update.message.chat_id)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("top_tokens", top_tokens))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
