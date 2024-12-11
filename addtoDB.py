# addtoDB.py

import sqlite3
import argparse

# Connect to SQLite database
def connect_to_db():
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post TEXT NOT NULL,
            category TEXT,
            response TEXT
        )
    """)
    conn.commit()
    return conn, cursor

# Function to add a post to the database
def add_post_to_db(post_text, category=None, response=None):
    conn, cursor = connect_to_db()

    cursor.execute("INSERT INTO posts (post, category, response) VALUES (?, ?, ?)", 
                   (post_text, category, response))
    conn.commit()

    print(f"Post added: {post_text}")
    conn.close()

def main():
    print("Welcome to the Post Adding Service.")
    print("Type 'exit' to stop the service.")
    
    while True:
        # Ask the user to input a post
        post_text = input("Enter post text: ")

        # Exit condition
        if post_text.lower() == 'exit':
            print("Exiting the service.")
            break

        add_post_to_db(post_text)
    
if __name__ == "__main__":
    main()