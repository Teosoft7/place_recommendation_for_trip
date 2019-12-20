# Place Recommendation
#### with visitkorea.or.kr data for SEOUL, KOREA

## Business Understanding

When you're planning a trip, you need to search a lot of places for your interest.   
In terms of visiting SEOUL, there a bunch of places to go.   
I made a recommendation model for places based on your interest.   

## Data Understanding

I used API from visitkorea.or.kr, operated by the Korea Tourism Organization,   
to collect points of interest data of SEOUL.   
You can refer to http://api.visitkorea.or.kr page about API and data itself.

## Data Preparation

I just collect the places in SEOUL from KTO API by filtering the area.
I mostly used the title, content_type, and overview text to analyze the characteristic of the place.

## Modeling

My model is simply using vectorized values from overview text about the place with TF-IDF method, based on the values, I calculate the distances between vectors of each place, and find the nearest place. I assume the nearest distance of vectors means they have some similarities.

## Evaluation

There are no target values from the user, it means no way to evaluate the model with predicted value vs. real value. I'm trying to evaluate the model with deployment to the web and collect answers from the users.

## Deployment

http://trip.proba.in
I deployed the model with a simple web app with Flask.
When opening the web page,  you can see the random selected 3 places in SEOUL. If you choose your preferred place, you can see 3 similar places with your choice. You can answer if you like the recommended place or not.

## Exploration

I have some plans to build tour recommendation apps based on this approach. 
