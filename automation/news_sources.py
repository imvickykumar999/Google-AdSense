
# pip install newsapi-python
# https://newsapi.org/docs/client-libraries/python

from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='39e270768fef4cfe848af36d98107e82')

def news_by_topic():
    topic = input('\nEnter News Topic (say, Diwali) : ')
    top_headlines = newsapi.get_everything(q=topic, language='en')
    return top_headlines

def news_by_sources():
    sources = newsapi.get_sources()
    sources = sources['sources']

    dn = {}
    for j, i, in enumerate(sources):
        print(j, i['id'])
        dn.update({j : i['id']})

    x = int(input('\nEnter News number : '))
    top_headlines = newsapi.get_top_headlines(sources=dn[x], language='en')
    return top_headlines

if __name__ == '__main__':
    top_headlines = news_by_topic()
    # top_headlines = news_by_sources()

    x = len(top_headlines['articles'])
    x = int(input(f'\nEnter News number (0-{x-1}) : '))
    nth_news = top_headlines['articles'][x]

    for i in nth_news:
        print()
        print(i, '\t:', nth_news[i])
