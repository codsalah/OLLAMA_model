import subprocess
import sqlite3
import time
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

# Define categories
categories = [
    "Technology", "Health & Wellness", "Environment", "Social Issues", "Personal Development",
    "Travel", "Lifestyle", "Business", "Education", "Entertainment", "Food & Drink", "Sports",
    "Finance", "Politics", "Science", "Art & Culture", "Parenting", "History", "Music", "Gaming", "Lifestyle"
]

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

# Function to run OLLAMA
def run_ollama(input_text):
    try:
        # print("Running OLLAMA with input:", input_text)  # Add logging
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=input_text.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("OLLAMA response:", result.stdout.decode())  # Add logging
        return result.stdout.decode().strip()  # Return the response
    except Exception as e:
        print(f"Error running OLLAMA: {e}")
        return None

# Function to classify unclassified posts
def classify_unclassified_posts(conn, cursor):
    cursor.execute("SELECT id, post FROM posts WHERE category IS NULL")
    rows = cursor.fetchall()

    classified_posts = []

    for row in rows:
        post_id, post = row
        prompt = f"Always Classify the following post into one or more of the categories below. The categories are: {', '.join(categories)}. Only return the categories that apply, separated by commas. Do not include any other text. \n\nPost: {post}\n\nCategories:"
        response = run_ollama(prompt)
        
        # Extract category from the response
        category = response.split(":")[-1].strip() if response else "Unknown"
        
        # Update the database
        cursor.execute(
            "UPDATE posts SET category = ?, response = ? WHERE id = ?",
            (category, response, post_id)
        )
        conn.commit()
        
        classified_posts.append({
            "post_id": post_id,
            "category": category,
            "response": response
        })
    
    return classified_posts

@app.route('/get_classified_posts', methods=['GET'])
def get_classified_posts():
    # Connect to DB
    conn, cursor = connect_to_db()

    # Get classified posts
    cursor.execute("SELECT id, post, category, response FROM posts WHERE category IS NOT NULL")
    rows = cursor.fetchall()

    classified_posts = [
        {"id": row[0], "post": row[1], "category": row[2], "response": row[3]} for row in rows
    ]

    conn.close()

    return jsonify(classified_posts)

@app.route('/')
def home():
    return """
    <h1>Welcome to the Post Classification Service!</h1>
    <p>Welcome to our Post Classification API. Here you can classify your posts into various categories.</p>
    <h3>Available Endpoints:</h3>
    <ul>
        <li><b>http://127.0.0.1:5000/classify_posts</b> (POST): Classify a given post by sending its text.</li>
        <li><b>http://127.0.0.1:5000/get_unclassified_posts</b> (GET): Retrieve all posts that have not been classified yet.</li>
        <li><b>http://127.0.0.1:5000/get_classified_posts</b> (GET): Retrieve all posts that have been classified Y.</li>

    </ul>
    <h3>Usage:</h3>
    <p>To classify a post, send a POST request to <code>/classify_posts</code> with a JSON body containing the post text.</p>
    """


@app.route('/classify_posts', methods=['POST'])
def classify_posts():
    # Get request JSON
    data = request.get_json()

    # Connect to DB
    conn, cursor = connect_to_db()

    # Post text from request
    post_text = data.get("post")
    
    if not post_text:
        return jsonify({"error": "No post text provided"}), 400

    # Classify the post
    prompt = f"Classify the following post into one or more of the categories below. The categories are: {', '.join(categories)}. Only return the categories that apply, separated by commas. Do not include any other text. \n\nPost: {post_text}\n\nCategories:"
    response = run_ollama(prompt)
    
    category = response.split(":")[-1].strip() if response else "Unknown"

    # Insert the post into the database
    cursor.execute("INSERT INTO posts (post, category, response) VALUES (?, ?, ?)", (post_text, category, response))
    conn.commit()

    # Return the result as JSON
    result = {
        "post": post_text,
        "category": category,
        "response": response
    }

    conn.close()
    
    return jsonify(result)

@app.route('/get_unclassified_posts', methods=['GET'])
def get_unclassified_posts():
    # Connect to DB
    conn, cursor = connect_to_db()

    # Get unclassified posts
    cursor.execute("SELECT id, post FROM posts WHERE category IS NULL")
    rows = cursor.fetchall()

    unclassified_posts = [{"id": row[0], "post": row[1]} for row in rows]

    conn.close()

    return jsonify(unclassified_posts)

# Background thread to periodically check for unclassified posts
def start_scheduler():
    conn, cursor = connect_to_db()
    try:
        while True:
            print("\nChecking for unclassified posts...")
            classified_posts = classify_unclassified_posts(conn, cursor)
            print(f"Classified {len(classified_posts)} posts.")
            time.sleep(10)  # Run every 10 sec
    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Start Flask app in a background thread
    thread = Thread(target=start_scheduler)
    thread.daemon = True
    thread.start()

    # Start Flask API
    app.run(debug=True, host='0.0.0.0', port=5000)



###############################


