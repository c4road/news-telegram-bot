import logging
import json

import telebot
from telebot.util import extract_arguments

from news_service import (
    get_news_by_topic, 
    prepare_for_markdown,
    prepare_for_single_items,
)
from settings import BOT_API_KEY, VALID_TOPICS

bot = telebot.TeleBot(BOT_API_KEY, parse_mode="Markdown")


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing pelotudo?")

@bot.message_handler(commands=['news'])
def get_news(message):
    logger.info("This is the message json %s", message.json)
    text = message.json.get('text', '') 
    topic = extract_arguments(text).replace('\'','').replace('\"', '')
    logger.info('Processing this topic %s', topic)
    if topic in  ['topics', 'topic']:
        logger.info("Invalid topic : %s", topic)
        bot.reply_to(message, str(VALID_TOPICS))
        return
    if not topic in VALID_TOPICS:
        logger.info("Invalid topic : %s", topic)
        bot.reply_to(message, f'Huh ({topic})?')
        return
    news = get_news_by_topic(topic)  # TODO: add topic 
    if not len(news):
        bot.reply_to(message, "No results")
        return
    news_message = prepare_for_single_items(news)
    # msgs = [news_message[i:i + 4096] for i in range(0, len(news_message), 4096)]
    for new in news_message:
        bot.reply_to(message, new)
    return

@bot.message_handler(commands=['newst'])
def get_news(message):
    # topic = extract_arguments(message)
    logger.info("Hello chat %s", message.chat)

if __name__ == "__main__":
    bot.infinity_polling()
