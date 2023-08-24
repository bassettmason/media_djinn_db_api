from utils import remove_null_values, initialize_firestore, add_movie_to_firestore, add_movie_list_to_firestore

# Initializing Firestore client
db = initialize_firestore()

def movie_db(request):
    """Adds a movie object or a movie list to the Firestore database."""
    if request.method != 'POST':
        return 'Only POST requests are allowed', 405

    request_json = request.get_json(silent=True)
    
    # Check for movie list POST request
    if 'name' in request_json and 'media_list' in request_json:
        return process_movie_list(request_json)
    # Otherwise, assume it's a movie POST request
    elif 'title' in request_json and 'ids' in request_json:
        return process_movie(request_json)
    else:
        return 'Invalid POST request format', 400

def process_movie(movie_data):
    """Process a single movie object."""
    if not all(key in movie_data for key in ['title', 'year', 'ids']):
        return 'Invalid movie object provided', 400

    imdb_id = movie_data['ids'].get('imdb')
    if not imdb_id:
        return 'No IMDb ID provided in movie object', 400

    cleaned_data = remove_null_values(movie_data)
    # Add movie to Firestore
    add_movie_to_firestore(db, imdb_id, cleaned_data)
    
    return f'Movie {imdb_id} added successfully!', 200

def process_movie_list(movie_list_data):
    """Process a movie list object."""
    name = movie_list_data.get('name')
    media_list = movie_list_data.get('media_list')

    if not name or not media_list:
        return 'Invalid movie list provided', 400
    
    # Add movie list to Firestore
    add_movie_list_to_firestore(db, name, media_list)
    return f"Movie list '{name}' added successfully!", 200
