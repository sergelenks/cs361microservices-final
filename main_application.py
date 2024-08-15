import requests
import sqlite3

CREATE_SERVICE_URL = "http://localhost:5001/exercise"
READ_SERVICE_URL = "http://localhost:5002/exercises"
UPDATE_SERVICE_URL = "http://localhost:5003/exercise"
DELETE_SERVICE_URL = "http://localhost:5004/exercise"
CREATE_WORKOUT_SERVICE_URL = "http://localhost:5005/process_workouts"

COMM_DB = 'communication.db'

def get_comm_db_connection():
    return sqlite3.connect(COMM_DB)

def create_exercise():
    print("Enter details of new exercise")
    name = input("Enter exercise name: ")
    sets = int(input("Enter the number of sets: "))
    reps = int(input("Enter the number of reps: "))

    exercise_data = {"name": name, "sets": sets, "reps": reps}
    try:
        response = requests.post(CREATE_SERVICE_URL, json=exercise_data)

        if response.status_code == 201:
            print("Exercise created successfully.")
        else:
            print(f"Failed to create exercise. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def read_exercises():
    try:
        response = requests.get(READ_SERVICE_URL)

        if response.status_code == 200:
            exercises = response.json()
            if exercises:
                for exercise in exercises:
                    print(
                        f"ID: {exercise['id']}, Name: {exercise['name']}, Sets: {exercise['sets']}, Reps: {exercise['reps']}")
            else:
                print("No exercises found.")
        else:
            print(f"Failed to retrieve exercises. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def update_exercise():
    exercise_id = int(input("Enter the exercise ID to update: "))
    name = input("Enter the updated exercise name: ")
    sets = int(input("Enter the updated number of sets: "))
    reps = int(input("Enter the updated number of reps: "))

    exercise_data = {"name": name, "sets": sets, "reps": reps}
    response = requests.put(f"{UPDATE_SERVICE_URL}/{exercise_id}", json=exercise_data)

    if response.status_code == 200:
        print("Exercise updated successfully.")
    elif response.status_code == 404:
        print("Exercise not found.")
    else:
        print("Failed to update exercise.")


def delete_exercise():
    exercise_id = int(input("Enter the exercise ID to delete: "))

    response = requests.delete(f"{DELETE_SERVICE_URL}/{exercise_id}")

    if response.status_code == 200:
        print("Exercise deleted successfully.")
    elif response.status_code == 404:
        print("Exercise not found.")
    else:
        print("Failed to delete exercise.")


def create_workout():
    print("Create a new workout")
    workout_exercises = []

    while True:
        name = input("Enter exercise name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        sets = int(input("Enter the number of sets: "))
        reps = int(input("Enter the number of reps: "))
        workout_exercises.append({"name": name, "sets": sets, "reps": reps})

    conn = get_comm_db_connection()
    cursor = conn.cursor()

    try:
        for exercise in workout_exercises:
            cursor.execute('''INSERT INTO communication (action, name, sets, reps)
                              VALUES (?, ?, ?, ?)''', (1, exercise['name'], exercise['sets'], exercise['reps']))
        conn.commit()
        print("Workout created.")

        # Trigger workout processing
        response = requests.post(CREATE_WORKOUT_SERVICE_URL)
        if response.status_code == 200:
            print("Workout processing started.")
        else:
            print("Failed to start workout processing.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def main():
    while True:
        print("\nWorkout Tracker")
        print("1. Create Exercise")
        print("2. View Exercises")
        print("3. Update Exercise")
        print("4. Delete Exercise")
        print("5. Create Workout")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_exercise()
        elif choice == '2':
            read_exercises()
        elif choice == '3':
            update_exercise()
        elif choice == '4':
            delete_exercise()
        elif choice == '5':
            create_workout()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()