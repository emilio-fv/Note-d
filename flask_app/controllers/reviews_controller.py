from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.models.review_model import Review 
import pprint
from flask_app.controllers.helpers import login_required, sp
import flask_app.constants

@app.route('/reviews/new/<album_id>') # New Review Form
def new_review_form(album_id):
    album_results = sp.album(album_id)
    album_data = {
        "album_id": album_results['id'],
        "album_name": album_results['name'],
        "artist_name": album_results['artists'][0]['name'],
        "img_url": album_results['images'][0]['url']
    }
    return render_template('review_new.html', album_data=album_data)

@app.route('/reviews/create', methods=['POST']) # Create New Review
@login_required
def create_review():
    review_data = {
        **request.form,
        "user_id": session['user_id']
    }
    Review.create(review_data) 
    return redirect('/dashboard')

@app.route('/reviews/search') # Search reviews form
@login_required
def search_reviews_form():
    return render_template('review_search.html')


# TODO Search Reviews
@app.route('/reviews/search', methods=['POST'])
@login_required
def search_reviews():
    search_input = request.form['search_input']
    search_category = request.form['search_category']

    if search_category == 'album':
        search_results = Review.get_all_by_album({'album_name': search_input})

    if search_category == 'artist':
        search_results = Review.get_all_by_artist({'artist_name': search_input})

    if search_category == 'username':
        search_results = Review.get_all_by_username({'username': search_input})

    all_reviews = []
    for review in search_results:
        this_review = {
            'id': review.id,
            'album_name': review.album_name,
            'artist_name': review.artist_name,
            'img_url': review.img_url,
            'date': review.date,
            'rating': review.rating,
            'text': review.text,
            'created_at': review.created_at,
            'updated_at': review.updated_at,
            'user_id': review.user_id,
            'username': review.user.username,
            'first_name': review.user.first_name,
            'last_name': review.user.last_name,
        }
        all_reviews.append(this_review)

    return jsonify(all_reviews)


# TODO View Review
# TODO Edit Review

@app.route('/reviews/delete/<review_id>') # Delete Review
@login_required
def delete_review(review_id):
    Review.delete({
        "id": review_id
    })
    return redirect('/dashboard')