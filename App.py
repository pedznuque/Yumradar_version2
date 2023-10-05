from Database_tables import tables
from Profile_setting import profile, profile_pic
from Admin import user_list, user_profile, delete_user, delete_users_review
from Forms import login, logout, register
from functions import get_profile_pic, submit_rating, delete_rating, save_location, get_restaurants_df, get_overall_ratings, submit_like, undo_like, mark_helpful, has_clicked_helpful, undo_mark_helpful, bookmarks, bookmark, delete_bookmark
from Feed import feed


import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
import datetime







app = Flask(__name__)
app.secret_key = 'YumRadar'




# THIS IS THE STARTER PAGE OF THE SYSTEM
@app.route('/')
def index():
    
    
    
    
    # Log the visit in the database
    current_month = datetime.datetime.now().strftime('%B-%Y')
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO monthly_visits (month, visits) VALUES (?, 0)', (current_month,))
        c.execute('UPDATE monthly_visits SET visits = visits + 1 WHERE month = ?', (current_month,))
        conn.commit()
     


    profile_pic_url = get_profile_pic()
    
    # Extract unique values from the "location" column
    location_select = restaurants_df['location'].unique()
    

    return render_template('index.html', profile_pic_url=profile_pic_url, location_select=location_select)






tables()


# THESE ARE THE ROUTES FOR PROFILE_SETTING"S FUNCTIONS
app.route('/profile', methods=['GET', 'POST'])(profile)
app.route('/account', methods=['GET', 'POST'])(profile_pic)


# THESE ARE THE ROUTES FOR ADMIN'S FUNCTIONS
app.route('/users')(user_list)
app.route('/users/<int:user_id>')(user_profile)
app.route('/delete_user', methods=['POST'])(delete_user)
app.route('/delete_users_review', methods=['POST'])(delete_users_review)


# THESE ARE THE ROUTES FOR LOG IN AND REGISTER FORMS
app.route('/register', methods=['GET', 'POST'])(register)
app.route('/login', methods=['GET', 'POST'])(login)
app.route('/logout')(logout)



# THESE ARE THE ROUTES FOR FUNCTIONS
app.route('/submit_rating', methods=['POST'])(submit_rating)
app.route('/delete_rating/<comment_id>', methods=['POST'])(delete_rating)
app.route('/save_location', methods=['POST'])(save_location)
app.route('/feed', methods=['GET'])(feed)
app.route('/submit_like', methods=['POST'])(submit_like)
app.route('/undo_like', methods=['POST'])(undo_like)
app.route('/mark_helpful', methods=['POST'])(mark_helpful)
app.route('/undo_mark_helpful', methods=['POST'])(undo_mark_helpful)
app.route('/bookmark', methods=['POST'])(bookmark)
app.route('/bookmarks')(bookmarks)
app.route('/delete_bookmark/<bookmark_id>', methods=['DELETE'])(delete_bookmark)



@app.route('/admin_dashboard')
def admin_dashboard():
    
    
    

    # Retrieve monthly visit data from the SQLite database
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('SELECT month, visits FROM monthly_visits')
        data = c.fetchall()
      

    # Prepare data for rendering in the HTML template
    months = [row[0] for row in data]
    visits = [row[1] for row in data]
    
    # Execute the SQL query to get the sum of visits
    c.execute('SELECT SUM(visits) FROM monthly_visits')

    # Fetch the result
    total_visits = c.fetchone()[0]
    
    
    
    
    # Execute the SQL query to get the total number of users
    c.execute('SELECT COUNT(*) FROM users')

    # Fetch the result
    total_users = c.fetchone()[0]
    
    
    # Execute the SQL query to get the total number of reviews
    c.execute('SELECT COUNT(*) FROM ratings')

    # Fetch the result
    total_reviews = c.fetchone()[0]
    
    
    # Load the restaurants data into a DataFrame
    restaurants_df = get_restaurants_df()
    
    
    
    

    
    
    word_to_count_manila = "Manila"  
    filtered_df_manila = restaurants_df[restaurants_df['location'].str.contains(word_to_count_manila, case=False, na=False)]

    Manila_count = len(filtered_df_manila)


    word_to_count_makati = "Makati"
    filtered_df_makati = restaurants_df[restaurants_df['location'].str.contains(word_to_count_makati, case=False, na=False)]

    Makati_count = len(filtered_df_makati)




    word_to_count_paranaque = "Paranaque"
    filtered_df_paranaque = restaurants_df[restaurants_df['location'].str.contains(word_to_count_paranaque, case=False, na=False)]

    Paranaque_count = len(filtered_df_paranaque)



    word_to_count_pasig = "Pasig"
    filtered_df_pasig = restaurants_df[restaurants_df['location'].str.contains(word_to_count_pasig, case=False, na=False)]

    Pasig_count = len(filtered_df_pasig)



    word_to_count_muntilupa = "Muntilupa"
    filtered_df_muntilupa = restaurants_df[restaurants_df['location'].str.contains(word_to_count_muntilupa, case=False, na=False)]

    Muntilupa_count = len(filtered_df_muntilupa)




    word_to_count_mandaluyong = "Mandaluyong"
    filtered_df_muntilupa = restaurants_df[restaurants_df['location'].str.contains(word_to_count_mandaluyong, case=False, na=False)]

    Mandaluyong_count = len(filtered_df_muntilupa)



    word_to_count_pasay = "Pasay"
    filtered_df_pasay = restaurants_df[restaurants_df['location'].str.contains(word_to_count_pasay, case=False, na=False)]

    Pasay_count = len(filtered_df_pasay)



    word_to_count_marikina = "Marikina"
    filtered_df_marikina = restaurants_df[restaurants_df['location'].str.contains(word_to_count_marikina, case=False, na=False)]

    Marikina_count = len(filtered_df_marikina)



    word_to_count_san_juan = "San Juan"
    filtered_df_marikina = restaurants_df[restaurants_df['location'].str.contains(word_to_count_san_juan, case=False, na=False)]

    San_Juan_count = len(word_to_count_san_juan)


    word_to_count_manila = "Manila"
    filtered_df_manila = restaurants_df[restaurants_df['location'].str.contains(word_to_count_manila, case=False, na=False)]

    Manila_count = len(filtered_df_manila)



    word_to_count_caloocan = "Caloocan"
    filtered_df_caloocan = restaurants_df[restaurants_df['location'].str.contains(word_to_count_caloocan, case=False, na=False)]

    Caloocan_count = len(filtered_df_caloocan)



    word_to_count_las_pinas = "Las Pinas"
    filtered_df_las_pinas = restaurants_df[restaurants_df['location'].str.contains(word_to_count_las_pinas, case=False, na=False)]

    las_pinas_count = len(filtered_df_las_pinas)




    word_to_count_valenzuela = "Valenzuela"
    filtered_df_valenzuela = restaurants_df[restaurants_df['location'].str.contains(word_to_count_valenzuela, case=False, na=False)]

    Valenzuela_count = len(filtered_df_valenzuela)



    word_to_count_pateros = "Pateros"
    filtered_df_pateros = restaurants_df[restaurants_df['location'].str.contains(word_to_count_pateros, case=False, na=False)]

    Pateros_count = len(filtered_df_pateros)


    word_to_count_malabon = "Malabon"
    filtered_df_malabon = restaurants_df[restaurants_df['location'].str.contains(word_to_count_malabon, case=False, na=False)]

    Malabon_count = len(filtered_df_malabon)


    word_to_count_quezon = "Quezon"
    filtered_df_quezon = restaurants_df[restaurants_df['location'].str.contains(word_to_count_quezon, case=False, na=False)]

    Quezon_count = len(filtered_df_quezon)



    word_to_count_quezon = "Quezon"
    filtered_df_quezon = restaurants_df[restaurants_df['location'].str.contains(word_to_count_quezon, case=False, na=False)]

    Quezon_count = len(filtered_df_quezon)


    word_to_count_taguig = "Taguig"
    filtered_df_taguig = restaurants_df[restaurants_df['location'].str.contains(word_to_count_taguig, case=False, na=False)]

    Taguig_count = len(filtered_df_taguig)
    
    
    # Get the total count of all locations in the "location" column
    total_locations = restaurants_df['location'].count()


    data = {
        'Manila': Manila_count,
        'Makati': Makati_count,
        'Paranaque': Paranaque_count,
        'Pasig': Pasig_count,
        'Muntilupa': Muntilupa_count,
        'Mandaluyong': Mandaluyong_count,
        'Pasay': Pasay_count,
        'Marikina': Marikina_count,
        'San Juan': San_Juan_count,
        'Caloocan': Caloocan_count,
        'Las Pinas': las_pinas_count,
        'Valenzuela': Valenzuela_count,
        'Pateros': Pateros_count,
        'Malabon': Malabon_count,
        'Quezon': Quezon_count,
        'Taguig': Taguig_count,
        

    }
    
    print(total_locations)
    
    
    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    return render_template('admin_dashboard.html', location_select=location_select, profile_pic_url=profile_pic_url,  months=months, visits=visits, data=data, total_locations=total_locations, total_visits=total_visits, total_users=total_users, total_reviews=total_reviews)

    



@app.route('/help_desk')
def help_desk():
    
    # Load the restaurants data into a DataFrame
    restaurants_df = get_restaurants_df()
    
    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    
    return render_template('help_desk.html', location_select=location_select, profile_pic_url=profile_pic_url)




@app.route('/report_an_issue_form')
def report_an_issue_form():
    
    return render_template('report_an_issue_form.html')


@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    if request.method == 'POST':
        email = request.form['email']
        title = request.form['title']
        description = request.form['description']
        current_date = datetime.datetime.now().strftime('%B-%d-%Y')

        # Insert the issue into the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO issues (email, title, description, date) VALUES (?, ?, ?, ?)",
                  (email, title, description, current_date))
        conn.commit()
        conn.close()

        return render_template('success_report.html')
    
    
@app.route('/report_list')
def report_list():
    
    
 
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('SELECT * FROM issues')
    
    issues = c.fetchall()
    



    restaurants_df = get_restaurants_df()
    

    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    
    return render_template('report_list.html', location_select=location_select, profile_pic_url=profile_pic_url, issues=issues)
    
    
    
  


@app.route('/delete_issue/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            # Delete the issue with the specified issue_id
            c.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
            conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return 'success'
    
    

@app.route('/open_report_issue')
def open_report_issue():
    
    issue_id = request.args.get('issue_id')
    

    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('SELECT * FROM issues WHERE id = ?', (issue_id))
    
    issues = c.fetchall()
    
    
    restaurants_df = get_restaurants_df()
    

    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    
    
    
    
    
    return render_template('open_report_issue.html', issues=issues, location_select=location_select, profile_pic_url=profile_pic_url)   
    
    
    
    
@app.route('/about_us')
def about_us():
    
    restaurants_df = get_restaurants_df()
    

    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    
    return render_template('about_us.html', location_select=location_select, profile_pic_url=profile_pic_url)
    
    



# These are the libraries used for implementing algorithm
import numpy as np
from scipy.sparse.linalg import norm
import jellyfish
import pandas as pd



# Load the restaurants data into a DataFrame
restaurants_df = get_restaurants_df()


# Convert the category and location columns into a single combined column
restaurants_df['keywords'] = restaurants_df['category'] + ' ' + restaurants_df['Resto_name'] + ' ' + restaurants_df['location'] + ' ' + restaurants_df['Dishes_key']


# Convert the combined column into a TF-IDF vector representation
keywords = restaurants_df['keywords'].astype(str).tolist()



# Remove all commas from the keywords list
keywords = [keyword.replace(',', '') for keyword in keywords]




# Tokenize the text and count the term frequencies
Term_Frequencies = {}
for keyword in keywords:
    split_keywords = keyword.split()
    

    for split_keyword in split_keywords:
        Term_Frequencies[split_keyword] = Term_Frequencies.get(split_keyword, 0) + 1
        
 
    

# Create a vocabulary sorted by term frequency
unique_keywords_set = sorted(Term_Frequencies, key=Term_Frequencies.get, reverse=True)



# Assign indices to the vocabulary terms
term_indices = {term: index for index, term in enumerate(unique_keywords_set)}


# Calculate the term frequency-inverse document frequency (TF-IDF) matrix
TFIDF_matrix = np.zeros((len(keywords), len(unique_keywords_set)))
for i, doc in enumerate(keywords):
    tokens = doc.split()
    for token in tokens:
        if token in term_indices:
            term_index = term_indices[token]
            TFIDF_matrix[i, term_index] += 1


# Compute the document frequencies
document_frequencies = np.sum(TFIDF_matrix > 0, axis=0)



# Calculate the inverse document frequencies (IDF)
idf = np.log(len(keywords) / (1 + document_frequencies))

# Multiply the TF and IDF to get the TF-IDF matrix
TFIDF_matrix *= idf


# Normalize the TF-IDF matrix
document_norms = np.linalg.norm(TFIDF_matrix, axis=1)
normalized_TFIDF_matrix = TFIDF_matrix / document_norms[:, np.newaxis]



# Define the route for recommending restaurants
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    
    
    user_location = request.form['location']
    selected_value = request.form['value']

    Keywords_df = pd.read_csv(r'C:\Users\Gerald\Desktop\system\datasets\Keywords.csv')

    columns = ['Resto_name', 'Dishes_one', 'Dishes_two', 'Dishes_three', 'Dishes_four', 'Dishes_five', 'Dishes_six', 'Dishes_seven', 'Dishes_eight', 'Dishes_nine', 'Dishes_ten', 'category']

    # Function to find the nearest value in each column and return the column with the highest similarity score
    def find_nearest_combined_value(value):
        max_similarity = 0
        nearest_value = ""
        for column in columns:
            combined_values = Keywords_df[column].astype(str).tolist()
            match = max(combined_values, key=lambda x: jellyfish.jaro_winkler(value, x))
            similarity = jellyfish.jaro_winkler(value, match)
            if similarity > max_similarity:
                max_similarity = similarity
                nearest_value = match
        return nearest_value



    user_location = user_location
    # Find the nearest value in the combined columns
    nearest_value = find_nearest_combined_value(selected_value)

    possible_dish_or_resto = nearest_value
    
    
    

    # Create a TF-IDF vector for the user's input
    user_input = np.zeros((1, len(unique_keywords_set)))
    tokens = (nearest_value + ' ' + user_location).split()
    for token in tokens:
        if token in term_indices:
            term_index = term_indices[token]
            user_input[0, term_index] += 1

    # Multiply the user input with IDF to get the TF-IDF representation
    user_input *= idf
    
    
    # Normalize the user input vector
    user_input_norm = np.linalg.norm(user_input)
    normalized_user_input = user_input / user_input_norm
    
    
    def cosine_similarity(vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)
        similarity = dot_product / (norm_vector1 * norm_vector2)
        
        return similarity


    # Calculate the cosine similarity between the user input and all restaurants
    similarities = np.array([cosine_similarity(normalized_user_input, Restaurant_df_vector) for Restaurant_df_vector in normalized_TFIDF_matrix])



    # Add the cosine similarity values to the DataFrame
    restaurants_df['similarity'] = similarities

    # Filter restaurants based on the selected location
    filtered_restaurants_df = restaurants_df[restaurants_df['location'] == user_location]

    # Sort the filtered restaurants by cosine similarity, in descending order
    recommended_restaurants = filtered_restaurants_df.sort_values('similarity', ascending=False)

    # Show the top 30 recommended restaurants or the closest value if the number of recommended restaurants is less than 30
    n = min(60, len(recommended_restaurants))
    recommended_restaurants = recommended_restaurants[:n]

    # Get the name, address, and image URL of each restaurant
    Resto_names = recommended_restaurants['Resto_name'].tolist()
    locations = recommended_restaurants['location'].tolist()
    addresses = recommended_restaurants['address'].tolist()
    image_urls = recommended_restaurants['large_image_url'].tolist()
    category = recommended_restaurants['category'].tolist()
    cost_for_twos = recommended_restaurants['average_cost_for_two'].tolist()
    Resto_ids = recommended_restaurants['resto_id'].tolist()
    
    
    # Fetch overall ratings for each restaurant
    overall_ratings = [get_overall_ratings(resto_id) for resto_id in Resto_ids]




    restaurants = []
    for Resto_id, cost_for_two, category, address, Resto_name, location, image_url, ratings in zip(Resto_ids, cost_for_twos, category, addresses, Resto_names, locations, image_urls, overall_ratings):
        restaurant = {
            'Resto_id': Resto_id,
            'cost_for_two': cost_for_two,
            'category': category,
            'address': address,
            'Resto_name': Resto_name,
            'location': location,
            'image_url': image_url,
            'overall_ratings': ratings
        }
        
        restaurants.append(restaurant)

        
    
    location_select = restaurants_df['location'].unique()
    
    
    
    # Pass the list of dictionaries to the template
    return render_template('recommend.html', restaurants=restaurants, location_select=location_select, profile_pic_url=get_profile_pic(), possible_dish_or_resto=possible_dish_or_resto,user_location=user_location)














# function that show more details about the clicked resto and allow the user to comment and bookmark
@app.route('/details', methods=['GET', 'POST'])
def details():
    name = request.args.get('name')
    


    from sklearn.metrics.pairwise import cosine_similarity

    restaurant = restaurants_df[restaurants_df['resto_id'] == name].iloc[0]


    # Get the index of the clicked restaurant
    clicked_restaurant_index = restaurant.name

    # Calculate the TF-IDF similarity between the clicked restaurant and all restaurants
    similarities = cosine_similarity([TFIDF_matrix[clicked_restaurant_index]], TFIDF_matrix)[0]

    # Sort the restaurants based on TF-IDF similarity, in descending order
    similar_restaurants_indices = np.argsort(similarities)[::-1]
    similar_restaurants_indices = similar_restaurants_indices[similar_restaurants_indices != clicked_restaurant_index]

    # Filter out restaurants with the same 'Resto_name'
    similar_restaurants_indices = similar_restaurants_indices[~restaurants_df.iloc[similar_restaurants_indices]['Resto_name'].duplicated()]

    # Filter out restaurants with different category types
    clicked_restaurant_category = restaurant['category']
    similar_restaurants_indices = similar_restaurants_indices[restaurants_df.iloc[similar_restaurants_indices]['category'].apply(lambda x: isinstance(x, str) and any(category in x for category in clicked_restaurant_category.split(',')))]

    # Filter restaurants by location
    if restaurant['location'] == 'Makati':
        similar_restaurants_indices = similar_restaurants_indices[restaurants_df.iloc[similar_restaurants_indices]['location'] == 'Makati']
    else:
        similar_restaurants_indices = similar_restaurants_indices[restaurants_df.iloc[similar_restaurants_indices]['location'] == restaurant['location']]

    # Take exactly 3 most similar restaurants, or fill with other locations if necessary
    if len(similar_restaurants_indices) < 3:
        additional_restaurants_indices = restaurants_df[~restaurants_df['resto_id'].isin(similar_restaurants_indices)]['location'].drop_duplicates().sample(n=3-len(similar_restaurants_indices), random_state=42).index
        similar_restaurants_indices = np.concatenate([similar_restaurants_indices, additional_restaurants_indices])

    similar_restaurants_indices = similar_restaurants_indices[:3]
    similar_restaurants = restaurants_df.iloc[similar_restaurants_indices]


 
    similar_restaurants_list = []
    for _, row in similar_restaurants.iterrows():
        similar_restaurant = {
            'Resto_id': row['resto_id'],
            'cost_for_two': row['average_cost_for_two'],
            'category': row['category'],
            'address': row['address'],
            'Resto_name': row['Resto_name'],
            'location': row['location'],
            'image_url': row['image_url']
        }
        similar_restaurants_list.append(similar_restaurant)



    # Check if the value is True or False
    
    Delivery_true = restaurant['Delivery']
    if str(Delivery_true).lower() == 'true':
        Delivery = 'Available'
    else:
        Delivery = 'N/A'
        
    reservable_true = restaurant['reservable']
    if str(reservable_true).lower() == 'true':
        reservable = 'Available'
    else:
        reservable = 'N/A'
        
    Takeout_true = restaurant['Takeout']
    if str(Takeout_true).lower() == 'true':
        Takeout = 'Available'
    else:
        Takeout = 'N/A'
        
    dine_in_true = restaurant['dine_in']
    if str(dine_in_true).lower() == 'true':
        dine_in = 'Available'
    else:
        dine_in = 'N/A'  
        
    serves_breakfast_true = restaurant['serves_breakfast']
    if str(serves_breakfast_true).lower() == 'true':
        serves_breakfast = 'Available'
    else:
        serves_breakfast = 'N/A'  
        
    serves_lunch_true = restaurant['serves_lunch']
    if str(serves_lunch_true).lower() == 'true':
        serves_lunch = 'Available'
    else:
        serves_lunch = 'N/A' 
        
    serves_brunch_true = restaurant['serves_brunch']
    if str(serves_brunch_true).lower() == 'true':
        serves_brunch = 'Available'
    else:
        serves_brunch = 'N/A' 
    
    serves_dinner_true = restaurant['serves_dinner']
    if str(serves_dinner_true).lower() == 'true':
        serves_dinner = 'Available'
    else:
        serves_dinner = 'N/A' 

    
    serves_beer_true = restaurant['serves_beer']
    if str(serves_beer_true).lower() == 'true':
        serves_beer = 'Available'
    else:
        serves_beer = 'N/A' 
        
    serves_wine_true = restaurant['serves_wine']
    if str(serves_wine_true).lower() == 'true':
        serves_wine = 'Available'
    else:
        serves_wine = 'N/A' 
        
        
    # Used for the location Direction 
    api_key = "AIzaSyCM-Tau4R9IViS7_5svXJHwZUNd191kdTM"
    origin = f"{restaurant['latitude']},{restaurant['longitude']}"
    destination = restaurant['Resto_name']
    url_direction = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&key={api_key}"



    restaurant_details = {
        'name': restaurant['Resto_name'],
        'location': restaurant['location'],
        'address': restaurant['address'],
        'large_image_url': restaurant['large_image_url'],
        'image_url': restaurant['image_url'],
        'category': restaurant['category'],
        'resto_id': restaurant['resto_id'],
        'latitude': restaurant['latitude'],
        'longitude': restaurant['longitude'],
        'local_contacts': restaurant['local_contacts'],
        'international_contacts': restaurant['international_contacts'],
        'Delivery': Delivery,
        'reservable': reservable,
        'Takeout': Takeout,
        'dine_in': dine_in,
        'serves_breakfast': serves_breakfast,
        'serves_lunch': serves_lunch,
        'serves_brunch': serves_brunch,
        'serves_dinner': serves_dinner,
        'serves_beer': serves_beer,
        'serves_wine': serves_wine,
        'url_direction': url_direction
      
    }
    
    

   # Retrieve the ratings and reviews for the restaurant from the database
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT username, rating, review, timestamp, comment_id, helpful_count FROM ratings WHERE resto_id = ?", (name,))
        ratings = c.fetchall()

        

    # Create a list of dictionaries, where each dictionary represents a rating
    ratings_list = []
    for rating in ratings:
        rating_data = {
            'username': rating[0],
            'rating': rating[1],
            'review': rating[2],
            'timestamp': rating[3],
            'comment_id': rating[4],
            'count': rating[5],
            'clicked': has_clicked_helpful(session.get('username'), rating[4]) if session.get('username') else False,
            'profile_pic_url': None  # Initialize with None if the user doesn't have a profile picture
        }
        

        # Fetch the user's profile picture URL from the users table
        c.execute("SELECT profile_pic_url FROM users WHERE username = ?", (rating_data['username'],))
        result = c.fetchone()
        if result and result[0]:
            rating_data['profile_pic_url'] = result[0]
        else:
            # Set a default profile picture URL
            rating_data['profile_pic_url'] = 'https://cdn-icons-png.flaticon.com/512/1144/1144709.png'


        ratings_list.append(rating_data)
        
        # Sort the ratings_list based on timestamp in descending order (latest to oldest)
        ratings_list = sorted(ratings_list, key=lambda x: x['timestamp'], reverse=True)




    # Retrieve the ratings and reviews for the restaurant from the database
    c.execute("SELECT overall_rating, total_ratings FROM overall_average WHERE resto_id = ?", (name,))
    fetched_data = c.fetchall()



    overall_average = []
    for data in fetched_data:
        overall_average_data = {
            'overall_rating': data[0],
            'total_ratings': data[1],
        }
        overall_average.append(overall_average_data)



 
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT resto_likes FROM likes WHERE resto_id = ?", (restaurant['resto_id'],))
        not_none = c.fetchone() is not None

    if not_none:
        c = conn.cursor()
        c.execute("SELECT resto_likes FROM likes WHERE resto_id = ?", (restaurant['resto_id'],))
        likes_count = c.fetchone()[0]
    else:
        likes_count = ''
    


    if 'username' in session:
        
        c.execute("SELECT 1 FROM usernames_likes WHERE username = ? AND resto_id = ?", (session['username'], restaurant['resto_id']))
        liked = c.fetchone() is not None
        
        if liked:
          
            clicked = True
        else:
            clicked = False
    else:
        clicked = False

    session.pop('resto_id', None)  # Clear the stored resto_id from the session
    
    

    
    logged_in = False
    
    if 'username' in session:
        logged_in = True
    else:
        logged_in = False
        
        

    is_bookmarked = False  

    if 'username' in session:
            c.execute('''SELECT 1 FROM bookmarks
                         WHERE username = ? AND resto_id = ?''', (session['username'], restaurant_details['resto_id']))
            
            
            if c.fetchone() is not None:
                is_bookmarked = True
            else:
                is_bookmarked = False
                
   
   
    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()
    
    return render_template('details.html', restaurant=restaurant_details, is_bookmarked=is_bookmarked, similar_restaurants=similar_restaurants_list, ratings=ratings_list, overall_average=overall_average, profile_pic_url=profile_pic_url, location_select=location_select, likes_count=likes_count, clicked=clicked, logged_in=logged_in)





if __name__ == '__main__':
    app.run(debug=True)
