import sqlite3
import time
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

WORKOUT_DB = 'workout_tracker.db'
COMM_DB = 'communication.db'


def get_workout_db_connection():
    conn = sqlite3.connect(WORKOUT_DB)
    conn.row_factory = sqlite3.Row
    return conn


def get_comm_db_connection():
    conn = sqlite3.connect(COMM_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    workout_conn = get_workout_db_connection()
    workout_cursor = workout_conn.cursor()
    comm_conn = get_comm_db_connection()
    comm_cursor = comm_conn.cursor()

    try:
        # Create exercises table if not exists
        workout_cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   name TEXT NOT NULL,
                                   sets INTEGER NOT NULL,
                                   reps INTEGER NOT NULL)''')
        workout_conn.commit()

        # Create communication table if not exists
        comm_cursor.execute('''CREATE TABLE IF NOT EXISTS communication
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                action INTEGER NOT NULL,
                                name TEXT,
                                sets INTEGER,
                                reps INTEGER)''')
        comm_conn.commit()

        app.logger.info("Databases initialized successfully")
    except sqlite3.Error as e:
        app.logger.error(f"Failed to initialize databases: {e}")
    finally:
        workout_conn.close()
        comm_conn.close()


def create_exercise(name, sets, reps):
    conn = get_workout_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO exercises (name, sets, reps) VALUES (?, ?, ?)", (name, sets, reps))
        conn.commit()
        app.logger.info(f"Workout created: {name}, {sets} sets, {reps} reps")
    except sqlite3.Error as e:
        app.logger.error(f"Failed to create exercise: {e}")
    finally:
        conn.close()


@app.route('/process_workouts', methods=['POST'])
def process_workouts():
    while True:
        comm_conn = get_comm_db_connection()
        comm_cursor = comm_conn.cursor()
        try:
            comm_cursor.execute("SELECT * FROM communication WHERE action = 1")
            workout = comm_cursor.fetchone()
            if workout:
                create_exercise(workout['name'], workout['sets'], workout['reps'])

                # Reset communication
                comm_cursor.execute("DELETE FROM communication WHERE action = 1")
                comm_conn.commit()
                app.logger.info("Workout processed and communication reset")
            else:
                time.sleep(1)  # Wait for 1 second before checking again
        except sqlite3.Error as e:
            app.logger.error(f"Database error: {e}")
        finally:
            comm_conn.close()

    return jsonify({"message": "Workout processing completed"}), 200


if __name__ == '__main__':
    init_db()
    app.run(port=5005, debug=True)