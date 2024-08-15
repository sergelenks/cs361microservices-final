from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('workout_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/exercise/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Exercise not found'}), 404

    conn.close()
    return jsonify({'message': 'Exercise deleted successfully'})


if __name__ == '__main__':
    app.run(port=5004)