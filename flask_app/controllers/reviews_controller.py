from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.review_model import Review # Import Review Class from models file
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
from functools import wraps
import flask_app.constants

# ==== Spotify API ====
CLIENT_ID = flask_app.constants.CLIENT_ID
CLIENT_SECRET = flask_app.constants.CLIENT_SECRET
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# ==== Reviews CRUD ====
@app.route('/reviews/new/<album_id>') # ROUTE: new review form w/ album data 
def new_review(album_id):
    album_results = sp.album(album_id) # Get album title and populate 
    album_data = {
        "album_id": album_results['id'],
        "album_name": album_results['name']
    }
    return render_template('review_new.html', album_data=album_data)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/reviews/create/<album_id>', methods=['POST']) # ROUTE: create new reviews
@login_required
def create_review(album_id):
    # print(request.form)
    print(session['user_id'])
    review_data = {
        **request.form,
        "album_id": album_id,
        "user_id": session['user_id']
    }
    Review.create(review_data) # Instantiate Review 
    return redirect('/dashboard')

# TODO ROUTE: search reviews
# TODO ROUTE: view review
# TODO ROUTE: edit review
# TODO ROUTE: delete review
# @app.route('/reviews/delete/<int:id>') 
# def delete_review(id):
    # this_review = Review.