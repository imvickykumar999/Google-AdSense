
import requests, random
from flask_sqlalchemy import SQLAlchemy

from flask import (Flask, 
    render_template, 
    redirect, 
    url_for, 
    request
)

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

def get_news(source, bot_token='982e523813b347c6a6404fd1f9b6e41c'):
    try:
        bot_token = '982e523813b347c6a6404fd1f9b6e41c'
        gets = f'https://newsapi.org/v1/articles?source={source}&sortBy=top&apiKey={bot_token}'
        
        req = requests.get(gets) 
        box = req.json()['articles']

    except Exception as e:
        print(e)

    ha,ia,ba,la = [],[],[],[]

    for i in range(len(box)):
        h = box[i]['title']
        m = box[i]['urlToImage']
        b = box[i]['description']

        try: l = box[i]['url']
        except: l = 'link not found'

        ha.append(h)
        ia.append(m)
        ba.append(b)
        la.append(l)

    return ha, ia, ba, la

@app.route('/news/<source>')
def one_news(source):
    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html', 
                                ha=ha, 
                                ia=ia, 
                                ba=ba, 
                                la=la,
                                len = len(ha))
    except:
        return render_template('home.html', api_key=False)

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        if request.method == 'POST':
            api_key = request.form['api_key']
            source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
            source = random.choice(source)

            ha, ia, ba, la = get_news(source, api_key)
            return render_template('news.html', 
                                    ha=ha, 
                                    ia=ia, 
                                    ba=ba, 
                                    la=la,
                                    len = len(ha))
        else:
            return render_template('home.html', api_key=True)
    except: return render_template('404.html')

@app.route('/')
def news():
    source = ['bbc-news', 'cnn', 'the-verge', 'time', 'the-wall-street-journal']
    source = random.choice(source)

    try:
        ha, ia, ba, la = get_news(source)
        return render_template('news.html', 
                                ha=ha, 
                                ia=ia, 
                                ba=ba, 
                                la=la,
                                len = len(ha))
    except:
        return render_template('home.html', api_key=False)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/welcome/<uname>")
def welcome(uname):
    return render_template("welcome.html", uname=uname)

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("welcome", uname=uname))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == '__main__':
    db.create_all()
    app.run(
        # host="0.0.0.0", 
        debug=True
    )
