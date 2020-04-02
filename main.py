#!/usr/bin/env python3

import os
import logging
from uuid import uuid4
import requests

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown

TOKEN = os.getenv("TOKEN", None)
if not TOKEN:
    print("Define the TOKEN env variable containing the Telegram's token.")
    exit(1)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Start writing @nincodesbot followed by a valid username to get it\'s Nintendo friend code in any chat!')


def inlinequery(update, context):
    username = update.inline_query.query
    if not username:
        return

    code = fetch_friend_code(username)

    if not code:
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title=f"⚠️ {username} not found",
                input_message_content=InputTextMessageContent(
                    f'⚠️ <i>{username}</i> not found!\nAdd your friend code from https://nin.codes.',
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    ))]
        update.inline_query.answer(results)
        return

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title=f"{username}'s friend code",
            input_message_content=InputTextMessageContent(
                f'Friend code of <b>{username}</b>:\n<code>{code}</code>\n\n<i>Powered by <a href="https://nin.codes/{username}">nin.codes</a>.</i>',
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                ))]

    update.inline_query.answer(results)


def fetch_friend_code(username: str):
    url = f"https://api.nin.codes/v1/{username}"
    res = requests.get(url)
    try:
        code = res.json()["code"]
    except:
        return None
    return format_code(code)

def format_code(code: str) -> str:
    return f"{code[:4]}-{code[4:8]}-{code[8:]}"


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inlinequery))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
