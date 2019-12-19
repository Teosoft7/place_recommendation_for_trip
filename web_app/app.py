# my functions
from functions import (get_place,
                       get_shortest,
                       save_confirm)

# import common libraries
import pandas as pd
from flask import Flask, request, render_template, url_for
from pymongo import MongoClient

# Database connection (to local mongo)
connection = MongoClient(port=27017)
db = connection['cp_seoul']

# Flask app initialize
app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    # get random 3 places for display
    places = get_place(db, count=3)

    # return with template
    return render_template('index.html', 
                            count=len(places),
                            places=places)

@app.route('/detail', methods=['GET'])
def detail():
    """Return shortest places page.""" 

    # get contentid
    content_id = request.args.get('contentid')

    # get shortest places
    title, places = get_shortest(content_id)
    print(content_id)

    return render_template('detail.html', 
                            title=title,
                            content_id=content_id,
                            places=places, 
                            count=len(places))

@app.route('/confirm', methods=['GET'])
def confirm():
    origin_contentid = request.args.get('origin_contentid')
    content_id = request.args.get('contentid')
    ip_addr = None
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_addr = request.environ['REMOTE_ADDR']
    else:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    # Save user reaction to db
    save_confirm(db, origin_contentid, content_id, ip_addr)
    return render_template('confirm.html')

@app.route('/answer', methods=['GET'])
def answer():
    origin_contentid = request.args.get('origin_contentid')
    content_id = request.args.get('contentid')
    ip_addr = None
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_addr = request.environ['REMOTE_ADDR']
    else:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

    answer=request.args.get('answer')

    # Save user reaction to db
    save_confirm(db, origin_contentid, content_id, ip_addr, answer)
    return render_template('confirm.html')

@app.route('/about')
def about():
    """Return the about page."""
    return render_template('about.html')

