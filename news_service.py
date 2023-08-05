import requests
from pprint import pprint as pp 
from settings import NEWS_API_KEY
# Todo: Set logging


def get_news_by_topic(topic='technology'):
    """
    TOPICS_AVAILABLE = blockchain, earnings, ipo, mergers_and_acquisitions, financial_markets,
    economy_fiscal, economy_monetary, economy_macro, energy_transportation, finance, 
    life_sciences, manufacturing, real_estate, retail_wholesale, technology
    
    https://www.alphavantage.co/documentation/#news-sentiment
    
    """
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&'
    url += 'topics={}&'.format(topic)
    url += 'apikey={}'.format(NEWS_API_KEY)
    print(url)
    response = requests.get(url)
    if response.ok:
        response = response.json()
        return _format_news(response.get('feed'))
    print('something wrong happened {}'.format(response))

def get_news_by_ticker(tickers=['AAPL']):
    """
    https://www.alphavantage.co/documentation/#news-sentiment
    """
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&'
    url += 'tickers={}&'.format(','.join(tickers))
    url += 'apikey={}'.format(NEWS_API_KEY)
    response = requests.get(url)
    if response.ok:
        response = response.json()
        feed = response.get('feed')
        if not feed:
            return 'No feed for that ticker {}'.format(response)
        return _format_news(response.get('feed'))
    print('something wrong happened {}'.format(response))

    
def _format_news(news_response):
    news = []
    for i in range(len(news_response)):
        new = dict()
        new['title'] = news_response[i].get('title')
        tickers = []
        for sentiment in news_response[i].get('ticker_sentiment'):
            d = {}
            d['ticker'] = sentiment.get('ticker')
            d['sentiment_label'] = sentiment.get('ticker_sentiment_label')
            d['relevance'] = sentiment.get('relevance_score')
            tickers.append(d)
        new['tickers'] = tickers
        new['url'] = news_response[i].get('url')
        news.append(new)
    return news

def prepare_for_markdown(news_list):
    news = ""
    for new in news_list:
        news += f"[{new.get('title')}]({new.get('url')})"
        news += "\n\n"
    return news

def prepare_for_single_items(news_list):
    news = []
    for new in news_list:
        news.append(f"[{new.get('title')}]({new.get('url')})")
    return news
