from functions import get_restaurants_df, get_profile_pic, get_overall_ratings


import sqlite3
from flask import session, Flask, render_template
import random




# Function to randomly select n unique restaurants from a DataFrame for a given category
def get_random_restaurants(df, category, n=5):
    category_restaurants = df[df['category'] == category]
    unique_restaurants = category_restaurants['Resto_name'].nunique()
    
    if unique_restaurants < n:
   
        n = unique_restaurants
    
    if n <= 0:
        return None

    category_restaurants = category_restaurants.drop_duplicates(subset='Resto_name')
    
    if unique_restaurants > 0:
        category_restaurants = category_restaurants.sample(n=n, replace=False)
    else:
        return None 
    
    return category_restaurants



restaurants_df  = get_restaurants_df()





# Function for feed to generate random categorial Resto
def feed():
    has_location = None
    if 'username' in session:

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM location WHERE username = ?', (session['username'],))
            
            if c.fetchone():
                has_location = True

            else:
                has_location = False



    if 'username' in session:

        if has_location:
            
                c.execute('SELECT location FROM location WHERE username = ?', (session['username'],))
                location = c.fetchone()

                location = location[0]

                # Filter restaurants based on the user's location
                location_restaurants = restaurants_df[restaurants_df['location'] == location]


                if location_restaurants.empty:
                    return "No restaurants found for the given location."

                # Filter out category with 1 or 2 restaurants in the user's location
                filtered_category = []
                for category in location_restaurants['category'].unique():
                    category_restaurants = location_restaurants[location_restaurants['category'] == category]
                    unique_restaurants = category_restaurants['Resto_name'].nunique()
                    if unique_restaurants > 2:
                        filtered_category.append(category)

                if len(filtered_category) < 3:
                    return "Not enough category with sufficient restaurants in the given location."

                # Randomly select three category from the updated filtered list
                if len(filtered_category) < 20:
                    category = random.sample(filtered_category, len(filtered_category))
                else:
                    category = random.sample(filtered_category, 20)

                feed_data = {}

                for category in category:
                    # Get randomly selected restaurants for the category
                    category_restaurants = get_random_restaurants(location_restaurants, category, n=10)

                    # Create a list of restaurant details for the category
                    restaurant_details = []
                    for _, row in category_restaurants.iterrows():
                        restaurant_detail = {
                            'name': row['Resto_name'],
                            'location': row['location'],
                            'address': row['address'],
                            'large_image_url': row['large_image_url'],
                            'image_url': row['image_url'],
                            'category': row['category'],
                            'resto_id': row['resto_id'],
                            'latitude': row['latitude'],
                            'longitude': row['longitude'],
                            'overall_rating': get_overall_ratings(row['resto_id'])
                        }
                        restaurant_details.append(restaurant_detail)

                    # Store the category's restaurants in the feed_data dictionary
                    feed_data[category] = restaurant_details

                # Extract unique values from the "category" column
                category_select = location_restaurants['category'].unique()

                # Extract unique values from the "location" column
                location_select = restaurants_df['location'].unique()


        else:   
            # Filter out category with 1 or 2 restaurants
            filtered_category = []
            for category in restaurants_df['category'].unique():
                category_restaurants = restaurants_df[restaurants_df['category'] == category]
                unique_restaurants = category_restaurants['Resto_name'].nunique()
                if unique_restaurants > 2:
                    filtered_category.append(category)

            
            # Randomly select three category from the updated filtered list
            category = random.sample(filtered_category, 20)
            feed_data = {}

            for category in category:
                # Get randomly selected restaurants for the category
                category_restaurants = get_random_restaurants(restaurants_df, category, n=10)

                # Create a list of restaurant details for the category
                restaurant_details = []
                for _, row in category_restaurants.iterrows():
                    restaurant_detail = {
                        'name': row['Resto_name'],
                        'location': row['location'],
                        'address': row['address'],
                        'large_image_url': row['large_image_url'],
                        'image_url': row['image_url'],
                        'category': row['category'],
                        'resto_id': row['resto_id'],
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                        'overall_rating': get_overall_ratings(row['resto_id'])
                    }
                    restaurant_details.append(restaurant_detail)

                # Store the category's restaurants in the feed_data dictionary
                feed_data[category] = restaurant_details


            # Extract unique values from the "category" column
            location_select = restaurants_df['location'].unique()


    else:
        # Filter out category with 1 or 2 restaurants
            filtered_category = []
            for category in restaurants_df['category'].unique():
                category_restaurants = restaurants_df[restaurants_df['category'] == category]
                unique_restaurants = category_restaurants['Resto_name'].nunique()
                if unique_restaurants > 2:
                    filtered_category.append(category)

        
        # Randomly select three category from the updated filtered list
            category = random.sample(filtered_category, 20)
            feed_data = {}

            for category in category:
                # Get randomly selected restaurants for the category
                category_restaurants = get_random_restaurants(restaurants_df, category, n=10)

                # Create a list of restaurant details for the category
                restaurant_details = []
                for _, row in category_restaurants.iterrows():
                    restaurant_detail = {
                        'name': row['Resto_name'],
                        'location': row['location'],
                        'address': row['address'],
                        'large_image_url': row['large_image_url'],
                        'image_url': row['image_url'],
                        'category': row['category'],
                        'resto_id': row['resto_id'],
                        'latitude': row['latitude'],
                        'overall_rating': get_overall_ratings(row['resto_id'])
                    }
                    restaurant_details.append(restaurant_detail)

                # Store the category's restaurants in the feed_data dictionary
                feed_data[category] = restaurant_details

        

            # Extract unique values from the "category" column
            location_select = restaurants_df['location'].unique()
    
        
    
    profile_pic_url = get_profile_pic()


    # Pass the feed data and updated category list to the template
    return render_template('feed.html', feed_data=feed_data, location_select=location_select, has_location=has_location, profile_pic_url=profile_pic_url)




