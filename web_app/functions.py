import pandas as pd
import numpy as np
import time
import pickle

from datetime import datetime, timedelta
from pymongo import MongoClient, DESCENDING

def get_place(db, count=3):
    """Return the random selected place from the db"""
    place_coll = db['seoul_poi']

    cursor = place_coll.find({'contenttypeid': '76',
    'overview': {"$regex": "^[\s\S]{0,}$"},
    'firstimage': {"$regex": "^[\s\S]{0,}$"}})
    
    places = [place for place in cursor]

    idx = np.arange(len(places))
    selected = np.random.choice(idx, count, replace=False)
    
    selected_place = []
    for idx in selected:
        place = places[idx]
        note = "..."
        try:
            note = place['overview']
            place.update({'note': note[:200] + '...'})
        except:
            print("Error occured when extracting note")

        selected_place.append(place)
        
    return selected_place

def get_shortest(contentid, count=3):
    """Return shortest n vectors in matrix"""

    # load dataframe and vector matrix from pickled file
    svd_values = None
    df = None
    with open('poi_vectors', 'rb') as f:
        svd_values = pickle.load(f)

    with open('poi_df', 'rb') as f:
        df = pickle.load(f)

    # extract vectors to tuple array    
    vectors = [(i[0], i[1], i[2]) for i in svd_values]

    # find index of contentid
    index = df[df['contentid'] == contentid].index[0]
    title = df[df['contentid'] == contentid].title.values[0]

    # extract value of each dimension for calculating distance
    X = vectors[index][0]
    Y = vectors[index][1]
    Z = vectors[index][2]
 
    distances = []
    for i, value in enumerate(vectors):
        distance = (abs(X - value[0]) + abs(Y - value[1]) + abs(Z - value[2]), i)
        distances.append(distance)

    top5_similars = [i[1] for i in sorted(distances)[1:count + 1]]

    result = []
    i = 0
    for _, row in df.loc[top5_similars].iterrows():
        item = {
            'title': row['title'],
            'contentid': row['contentid'],
            'overview': row['overview'],
            'note': row['overview'][:200] + '...',
            'firstimage': row['firstimage'],
            'modifiedtime': row['modifiedtime'],
            'distance': distances[i][0]
        }
        result.append(item)
        i += 1
    
    return title, result
    

    

