
import requests, random
from flask import Flask, render_template, send_from_directory
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route('/<filename>')
def ads(filename):
    if '.' in filename:
        filename = 'ads.txt'
    return send_from_directory("", filename)

def get_news(source):
    if source == 'inshorts':

        link = 'https://inshorts.com/en/read'
        req = requests.get(link)

        soup = bs(req.content, 'html5lib')
        box = soup.findAll('div', attrs = {'class':'news-card z-depth-1'})

        ha,ia,ba,la = [],[],[],[]
        for i in range(len(box)):
            h = box[i].find('span', attrs = {'itemprop':'headline'}).text

            m = box[i].find('div', attrs = {'class':'news-card-image'})
            m = m['style'].split("'")[1]

            b = box[i].find('div', attrs = {'itemprop':'articleBody'}).text
            l = 'link not found'

            try:
                l = box[i].find('a', attrs = {'class':'source'})['href']
            except:
                pass
            
            ha.append(h)
            ia.append(m)
            ba.append(b)
            la.append(l)

    else:
        try:
            bot_token = '87623b8db3254e8698e239abc51a9c10'
            gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
            
            req = requests.get(gets) 
            box = req.json()['articles']

        except:
            try:
                bot_token = 'e1b57251b1b94ed894f3c60d25551eb2'
                gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
                
                req = requests.get(gets) 
                box = req.json()['articles']

            except:
                bot_token = '5f69434d32434ea8bdb16b347f71cca2'
                gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
                
                req = requests.get(gets) 
                box = req.json()['articles']

        ha,ia,ba,la = [],[],[],[]
        for i in range(len(box)):
            h = box[i]['title']
            m = box[i]['urlToImage']
            b = box[i]['description']
            l = 'link not found'

            try:
                l = box[i]['url']
            except:
                pass

            ha.append(h)
            ia.append(m)
            ba.append(b)
            la.append(l)
    return ha, ia, ba, la

@app.route('/news/<source>')
def one_news(source):
    
    ha, ia, ba, la = get_news(source)
    return render_template('news.html', 
                            ha=ha, 
                            ia=ia, 
                            ba=ba, 
                            la=la, 
                            len = len(ha))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def news():
    source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
    
    # https://newsapi.org/account
    source = random.choice(source)
    print(source)

    ha, ia, ba, la = get_news(source)
    # ha, ia, ba, la = get_news('inshorts')

    return render_template('news.html', 
                            ha=ha, 
                            ia=ia, 
                            ba=ba, 
                            la=la, 
                            len = len(ha))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(
        # host="0.0.0.0", 
        debug=False
    )
