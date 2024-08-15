import os
import sqlite3
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

DB_NAME = 'workout_tracker.db'


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             sets INTEGER NOT NULL,
             reps INTEGER NOT NULL)
        ''')
        conn.commit()
        app.logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        app.logger.error(f"Failed to initialize database: {e}")
    finally:
        conn.close()


@app.route('/exercise', methods=['POST'])
def create_exercise():
    app.logger.info("Received request to create exercise")
    exercise_data = request.json
    app.logger.debug(f"Exercise data: {exercise_data}")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''INSERT INTO exercises (name, sets, reps)
                          VALUES (?, ?, ?)''',
                       (exercise_data['name'], exercise_data['sets'], exercise_data['reps']))
        conn.commit()
        exercise_id = cursor.lastrowid
        app.logger.info(f"Exercise created with ID: {exercise_id}")
        return jsonify({'id': exercise_id, 'message': 'Exercise created successfully'}), 201
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

    app.run(port=5001, debug=True)