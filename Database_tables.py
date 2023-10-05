
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for




app = Flask(__name__)
app.secret_key = 'your_secret_key'







def tables():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()


    


    c.execute('''CREATE TABLE IF NOT EXISTS admin
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL);''')

    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                profile_pic_url TEXT);''')

                


    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT NOT NULL,
                username TEXT NOT NULL,
                resto_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                review TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                helpful_count INTEGER DEFAULT 0,
                FOREIGN KEY (username) REFERENCES users (username),
                FOREIGN KEY (resto_id) REFERENCES restaurants (resto_id)
            )''')


    c.execute('''CREATE TABLE IF NOT EXISTS helpful_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY (comment_id) REFERENCES ratings (comment_id),
                FOREIGN KEY (username) REFERENCES users (username)
            )''')




    
    # Create the "overall_average" table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS overall_average (
                resto_id TEXT PRIMARY KEY,
                overall_rating FLOAT DEFAULT 0,
                total_ratings INTEGER DEFAULT 0
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS usernames_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resto_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resto_id) REFERENCES restaurants (resto_id),
                FOREIGN KEY (username) REFERENCES users (username)
                )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resto_id INTEGER NOT NULL,      
                resto_likes INTEGER DEFAULT 0,
                FOREIGN KEY (resto_id) REFERENCES restaurants (resto_id)   
                )''')


    c.execute('''CREATE TABLE IF NOT EXISTS location 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,                                
                    location TEXT NOT NULL);''')



    c.execute('''CREATE TABLE IF NOT EXISTS bookmarks
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                resto_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                image_url TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users (username),
                FOREIGN KEY (resto_id) REFERENCES restaurants (resto_id));''')
    
    
    
    # For Admin dashboard
    
    c.execute('''
                    CREATE TABLE IF NOT EXISTS monthly_visits (
                        month TEXT PRIMARY KEY,
                        visits INTEGER
                    )
                    ''')
    
    
    #user report 
    c.execute('''CREATE TABLE IF NOT EXISTS issues
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (email) REFERENCES users(email));''')

    
    
    
    

    c.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", ('Admin', 'Admin'))
    conn.commit()

    conn.commit()
    conn.close()





