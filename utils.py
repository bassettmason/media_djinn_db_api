from google.cloud import firestore
from google.cloud.firestore import SERVER_TIMESTAMP
import os
import logging
# Logging setup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def remove_null_values(d):
    """Recursively remove keys with null values from a dictionary."""
    if not isinstance(d, dict):
        return d
    return {k: remove_null_values(v) for k, v in d.items() if v is not None}

def initialize_firestore():
    """Initialize and return a Firestore client."""
    return firestore.Client()

def add_movie_to_firestore(db, imdb_id, movie_data):
    """Add or merge a movie object to Firestore."""
    movies_ref = db.collection('movies')
    movie_doc_ref = movies_ref.document(imdb_id)
    movie_doc_ref.set(movie_data, merge=True)

def add_movie_list_to_firestore(db, name, media_list):
    """Add a movie list to Firestore."""
    movie_lists_ref = db.collection('movie-lists')
    movie_lists_ref.document(name).set({
        'media_list': media_list,
        'date_modified': SERVER_TIMESTAMP
    })
