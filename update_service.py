from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('workout_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/exercise/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    exercise_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''UPDATE exercises 
                      SET name = ?, sets = ?, reps = ?
                      WHERE id = ?''',
                   (exercise_data['name'], exercise_data['sets'],
                    exercise_data['reps'], exercise_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Exercise not found'}), 404

    conn.close()
    return jsonify({'message': 'Exercise updated successfully'})


if __name__ == '__main__':
    app.run(port=5003)