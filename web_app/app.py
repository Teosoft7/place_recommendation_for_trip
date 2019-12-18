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

    print(get_shortest((places[0]['contentid'])))

    # get total view counts and increments for last 4 hours
    # total_view, increments = get_sum_view_count(db)
    # stats= {
    #     'videos': get_collection_count(db, 'video'),
    #     'increments': get_count_string(increments),
    #     'total_view': get_count_string(total_view)
    # }

    # return with template
    return render_template('index.html', 
                            count=len(places),
                            places=places)

# @app.route('/hottrend')
# def hot_trend():
#     """Return hot trend page."""
#     # Need to add data set for hot trend
#     # Hot : top 10 most increments views for last 4 hours
#     count = 10
#     videos = get_hot_video(db, count=count)
    
#     # apply format for large numbers
#     for video in videos:
#         video['view_count'] = get_count_string(video['view_count'])
#         video['increment'] = get_count_string(video['increment'])

#     return render_template('hot_trend.html', videos=videos, count=count)

# @app.route('/mostwatched')
# def most_watched():
#     """Return most watched page."""
#     # Need to add data set for most_watched
#     # Most watched : top 10 most watched video
#     count = 10
#     videos = get_most_watched_video(db, count=count)
    
#     # apply format for large numbers
#     for video in videos:
#         video['view_count'] = get_count_string(video['view_count'])

#     return render_template('most_watched.html', videos=videos, count=count)

# @app.route('/newreleased')
# def new_released():
#     """Return new released page."""
#     # Need to add data set for new released
#     # new_released : top 6 most recently released video
#     count = 6
#     videos = get_most_recent_video(db, count=count)

#     return render_template('new_released.html', videos=videos, count=count)

@app.route('/about')
def about():
    """Return the about page."""
    return render_template('about.html')

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

    return render_template('confirm.html')