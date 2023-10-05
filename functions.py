import sqlite3
from flask import session, request, Flask, redirect, url_for, render_template, jsonify
import uuid
from datetime import datetime
import pandas as pd







# Function to get the restaurant_df path 
def get_restaurants_df():
    
    restaurants_df = pd.read_csv(r'C:\Users\Gerald\Desktop\system\datasets\DATASETS.csv')
    
    return restaurants_df




# Function to get profile pic url of the users
def get_profile_pic():
     
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()

        if 'username' in session:
            # Get user's current profile picture URL
            c.execute("SELECT profile_pic_url FROM users WHERE username = ?", (session['username'],))
            result = c.fetchone()
            if result is not None:
                profile_pic_url = result[0]
            else:
                profile_pic_url = 'https://cdn-icons-png.flaticon.com/512/1144/1144709.png'
        elif 'is_admin' in session:
            profile_pic_url = 'https://cdn-icons-png.flaticon.com/512/1144/1144709.png'
        else:
            profile_pic_url = 'https://cdn-icons-png.flaticon.com/512/1144/1144709.png'
            
        if profile_pic_url is None:
            profile_pic_url = 'https://cdn-icons-png.flaticon.com/512/1144/1144709.png'

        return profile_pic_url
    
    

# Function to save default location
def save_location():
    location = request.form['location']
    username = session['username']


    has_location = None
    if 'username' in session:

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM location WHERE username = ?', (session['username'],))
            
            if c.fetchone():
                has_location = True

            else:
                has_location = False
        
            if has_location:
                c.execute('UPDATE location SET location = ? WHERE username = ?', (location, username))   
            else:
                c.execute('INSERT INTO location (username, location) VALUES (?, ?)', (username, location))
                conn.commit()   

        return redirect(url_for('index'))








# Function to add ratings and comments
def submit_rating():
    if 'username' not in session:
        session['resto_id'] = request.form.get('resto_id')
        return redirect(url_for('login'))

    resto_id = request.form.get('resto_id')
    rating = request.form.get('rating')
    review = request.form.get('review')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generate a unique comment ID using a UUID
    comment_id = str(uuid.uuid4())

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO ratings (comment_id, username, resto_id, rating, review, timestamp)
                     VALUES (?, ?, ?, ?, ?, ?)''', (comment_id, session['username'], resto_id, rating, review, timestamp))
        conn.commit()


    # Retrieve all ratings for the restaurant from the database
    c.execute("SELECT rating FROM ratings WHERE resto_id = ?", (resto_id,))
    ratings = c.fetchall()

    # Calculate the overall average rating
    total_ratings = len(ratings)
    if total_ratings == 0:
        overall_rating = 0  # If there are no ratings, set the overall rating to 0
    else:
        sum_ratings = sum(rating[0] for rating in ratings)
        overall_rating = sum_ratings / total_ratings

    
    # Round off the overall rating to 2 decimal places
    overall_rating = round(overall_rating, 2)

    

    # Update the 'restaurants' table with the overall rating and total ratings
    c.execute("SELECT COUNT(*) FROM overall_average WHERE resto_id = ?", (resto_id,))
    restaurant_exists = c.fetchone()[0] > 0


    if restaurant_exists:
        # Update the existing row with the new overall rating and total ratings
        c.execute("UPDATE overall_average SET total_ratings = ?, overall_rating = ? WHERE resto_id = ?", (total_ratings, overall_rating, resto_id))
    else:
        # Insert a new row with the resto_id, overall rating, and total ratings
        c.execute("INSERT INTO overall_average (resto_id, overall_rating, total_ratings) VALUES (?, ?, ?)", (resto_id, overall_rating, total_ratings))

    conn.commit()
    

    return redirect(url_for('details', name=resto_id))




# Function to delete ratings
def delete_rating(comment_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()

  
        c.execute("SELECT resto_id, rating FROM ratings WHERE comment_id = ?", (comment_id,))
        rating_data = c.fetchone()

     

        resto_id = rating_data[0]
        old_rating = rating_data[1]


        c.execute("DELETE FROM ratings WHERE comment_id = ?", (comment_id,))
        conn.commit()

        # Retrieve all ratings for the restaurant from the database
        c.execute("SELECT rating FROM ratings WHERE resto_id = ?", (resto_id,))
        ratings = c.fetchall()

   
        total_ratings = len(ratings)
        if total_ratings == 0:
            overall_rating = 0  # If there are no ratings, set the overall rating to 0
        else:
            sum_ratings = sum(rating[0] for rating in ratings)
            overall_rating = sum_ratings / total_ratings

     
     
        overall_rating = round(overall_rating, 2)

        c.execute("UPDATE overall_average SET total_ratings = ?, overall_rating = ? WHERE resto_id = ?", (total_ratings, overall_rating, resto_id))
        conn.commit()

       
        return redirect(url_for('details', name=resto_id))



# Function to fetch overall ratings from the user
def get_overall_ratings(resto_id):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT overall_rating, total_ratings FROM overall_average WHERE resto_id = ?", (resto_id,))
        fetched_data = c.fetchone()

    if fetched_data:
        overall_rating = fetched_data[0]
    else:
        overall_rating = 0.0
      
    return overall_rating




# function to like the clicked resto
def submit_like():
    if 'username' not in session:
        session['resto_id'] = request.form.get('resto_id')
        return redirect(url_for('login'))
    
    resto_id = request.form.get('resto_id')

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()

        c.execute("INSERT INTO likes (resto_id) VALUES (?)", (resto_id,))


        c.execute("SELECT resto_likes FROM likes WHERE resto_id = ?", (resto_id,))
        current_count = c.fetchone()[0]

        new_count = current_count + 1

     
        c.execute("UPDATE likes SET resto_likes = ? WHERE resto_id = ?", (new_count, resto_id))

      
        c.execute("INSERT INTO usernames_likes (username, resto_id) VALUES (?, ?)", (session['username'], resto_id))

        conn.commit()

    return redirect(url_for('details', name=resto_id))


# function to undo like
def undo_like():
    resto_id = request.form.get('resto_id')



    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()

     
        c.execute("SELECT resto_likes FROM likes WHERE resto_id = ?", (resto_id,))
        current_count = c.fetchone()[0]

       
        new_count = current_count - 1

      
        c.execute("UPDATE likes SET resto_likes = ? WHERE resto_id = ?", (new_count, resto_id))

        c.execute("DELETE FROM usernames_likes WHERE username = ? AND resto_id = ?", (session['username'], resto_id))

        conn.commit()


        conn.commit()

    return redirect(url_for('details', name=resto_id))



# function to define ratings likes
def has_clicked_helpful(username, comment_id):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM helpful_ratings WHERE username = ? AND comment_id = ?", (username, comment_id))
        return c.fetchone() is not None



# Function to add like to a ratings or mark them as helpful

def mark_helpful():
    if 'username' not in session:
        session['resto_id'] = request.form.get('resto_id')
        return redirect(url_for('login'))

    
    comment_id = request.form.get('comment_id')
    resto_id = request.form.get('resto_id')
    
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        


        c.execute("SELECT helpful_count FROM ratings WHERE comment_id = ?", (comment_id,))
        current_count = c.fetchone()[0]

    
        new_count = current_count + 1

       
        c.execute("UPDATE ratings SET helpful_count = ? WHERE comment_id = ?", (new_count, comment_id))

       
        c.execute("INSERT INTO helpful_ratings (username, comment_id) VALUES (?, ?)", (session['username'], comment_id))

        conn.commit()
        

    return redirect(url_for('details', name=resto_id))




# Function to undo the like in ratings
def undo_mark_helpful():
    comment_id = request.form.get('comment_id')
    resto_id = request.form.get('resto_id')



    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()


        c.execute("SELECT helpful_count FROM ratings WHERE comment_id = ?", (comment_id,))
        current_count = c.fetchone()[0]


        new_count = current_count - 1


        c.execute("UPDATE ratings SET helpful_count = ? WHERE comment_id = ?", (new_count, comment_id))


        c.execute("DELETE FROM helpful_ratings WHERE username = ? AND comment_id = ?", (session['username'], comment_id))

        conn.commit()

    return redirect(url_for('details', name=resto_id))








# Function to add bookmarks
def bookmark():
    if 'username' not in session:
        session['resto_id'] = request.form.get('resto_id')
        return redirect(url_for('login'))
        
    
    resto_id = request.form['resto_id']
    name = request.form['name']
    location = request.form['location']
    category = request.form['category']
    image_url = request.form['image_url']

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO bookmarks (username, resto_id, name, location, category, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                  (session['username'], resto_id, name, location, category, image_url))
        conn.commit()

    return 'success'





# Functions to fetch all bookmarks  
def bookmarks():
    if 'username' not in session:
        return redirect(url_for('login'))

    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''SELECT resto_id, name, location, category, image_url, timestamp
                     FROM bookmarks
                     WHERE username = ?
                     ORDER BY timestamp DESC''', (session['username'],))
        bookmarks = c.fetchall()

    import datetime
    


    bookmarks = sorted(bookmarks, key=lambda x: datetime.datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S'), reverse=True)
    
    
    # Load the restaurants data into a DataFrame
    restaurants_df = get_restaurants_df()
    
    location_select = restaurants_df['location'].unique()
    
    profile_pic_url = get_profile_pic()


    return render_template('bookmarks.html', bookmarks=bookmarks, location_select=location_select, profile_pic_url=profile_pic_url)


def delete_bookmark(bookmark_id):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('''DELETE FROM bookmarks
                         WHERE username = ? AND resto_id = ?''', (session['username'], bookmark_id))
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})