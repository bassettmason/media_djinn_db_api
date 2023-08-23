from utils import remove_null_values, initialize_firestore, add_movie_to_firestore

# Initializing Firestore client
db = initialize_firestore()

def add_movie_to_db(request):
    """Adds a movie object to the Firestore database."""
    if request.method != 'POST':
        return 'Only POST requests are allowed', 405

    request_json = request.get_json(silent=True)

    if not request_json or not all(key in request_json for key in ['title', 'year', 'ids']):
        return 'Invalid movie object provided', 400

    imdb_id = request_json['ids'].get('imdb')
    if not imdb_id:
        return 'No IMDb ID provided in movie object', 400

    cleaned_data = remove_null_values(request_json)

    # Add movie to Firestore
    add_movie_to_firestore(db, imdb_id, cleaned_data)
    
    return f'Movie {imdb_id} added successfully!', 200
