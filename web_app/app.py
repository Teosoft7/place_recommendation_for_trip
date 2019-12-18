# my functions
from functions import (get_place,
                       get_shortest,)

# import common libraries
import pandas as pd
from flask import Flask, request, render_template, url_for
from pymongo import MongoClient

connection = MongoClient(port=27017)
db = connection['cp_seoul']
app = Flask(__name__, static_url_path="")

if __name__ == '__main__':
    app.run(debug=True)

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
                            places=places, 
                            count=len(places))


@app.route('/confirm', methods=['GET'])
def confirm():
    content_id = request.args.get('contentid')
    print(content_id)

    print(request.remote_addr)

    # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    #     print(request.environ['REMOTE_ADDR'])
    # else:
    #     print(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy

    return render_template('confirm.html')


@app.route('/about')
def about():
    """Return the about page."""
    return render_template('about.html')

