from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta, date, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate
import cryptocalculate, scrapenews, nflscrape


app = Flask(__name__)
app.secret_key = 'mykey'  # key that allows sessions to operate (i think)
app.permanent_session_lifetime = timedelta(minutes = 5)  # (allows the session to last for such amount of time)


@app.route('/')
def test():
    return render_template('base.html', page='test')

@app.route('/crypto', methods=['POST', 'GET'])
def crypto():
    yourcrypto = None 
    message = None
    if request.method == 'POST':
        cryptoname = request.form['name']
        yourcrypto = int(request.form['yourcrypto'])
        futurecrypto = int(request.form['futurecrypto'])
        session['cryptoname'] = cryptoname
        session['yourcrypto'] = yourcrypto
        session['futurecrypto'] = futurecrypto

        upside = futurecrypto/yourcrypto
        message = f"{cryptoname}'s upside will be a {upside}x"
        return render_template('crypto.html', page='crypto', crypto = yourcrypto, upside = upside, message=message, cryptoname=cryptoname)
    
    return render_template('crypto.html', page='crypto')

@app.route('/news')
def news():
    newsframe = scrapenews.findtitles()
    return render_template('news.html', page='news', data = newsframe, frame = newsframe.to_html(classes=["table", "table-bordered", "table-striped", "table-hover", "table table-striped table-hover"]))

@app.route('/youtube')
def youtube():
    return render_template('youtube.html', page= 'youtube')

@app.route('/nflscrape')
def espnscrape():
    statframe = nflscrape.findstats()
    return render_template('nflscrape.html' , page ='espnscrape', data=statframe.to_html(classes=["table", "table-bordered", "table-striped", "table-hover", "table table-striped table-hover"]))

if __name__ == '__main__':
    app.run(debug=True)