import telebot


from news_service import (
    get_news_by_topic, 
    prepare_for_markdown,
)
from settings import BOT_API_KEY

bot = telebot.TeleBot(BOT_API_KEY, parse_mode="Markdown")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing pelotudo?")

@bot.message_handler(commands=['news'])
def get_news(message):
    news = get_news_by_topic('blockchain')  # TODO: add topic 
    news_message = prepare_for_markdown(news)
    msgs = [news_message[i:i + 4096] for i in range(0, len(news_message), 4096)]
    for text in msgs:
        bot.reply_to(message, text)

if __name__ == "__main__":
    bot.infinity_polling()
