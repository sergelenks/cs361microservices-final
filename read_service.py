from flask import Flask, jsonify
import sqlite3
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

DB_NAME = 'workout_tracker.db'


def get_db_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        app.logger.info(f"Successfully connected to database: {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Failed to connect to database: {e}")
        raise


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           sets INTEGER NOT NULL,
                           reps INTEGER NOT NULL)''')
        conn.commit()
        app.logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        app.logger.error(f"Failed to initialize database: {e}")
    finally:
        conn.close()


@app.route('/exercises', methods=['GET'])
def read_exercises():
    app.logger.info("Received request to read exercises")
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM exercises")
        exercises = cursor.fetchall()
        app.logger.info(f"Retrieved {len(exercises)} exercises")
        return jsonify([dict(exercise) for exercise in exercises])
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        app.logger.info(f"Database file not found. Creating new database: {DB_NAME}")
    else:
        app.logger.info(f"Database file found: {DB_NAME}")

    init_db()  # Call init_db() every time the app starts

    app.run(port=5002, debug=True)