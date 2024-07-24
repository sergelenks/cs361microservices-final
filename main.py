import sqlite3

conn = sqlite3.connect('workout_tracker.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   sets INTEGER,
                   reps INTEGER)''')

def create_exercise(name, sets, reps):
    if save_or_cancel("save the exercise"):
        cursor.execute("INSERT INTO exercises (name, sets, reps) VALUES (?, ?, ?)", (name, sets, reps))
        conn.commit()
        print("Exercise saved successfully.")
    else:
        print("Exercise creation canceled.")

def read_exercises():
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    for exercise in exercises:
        print(f"ID: {exercise[0]}, Name: {exercise[1]}, Sets: {exercise[2]}, Reps: {exercise[3]}")

def update_exercise(exercise_id, name, sets, reps):
    if save_or_cancel("save the updated exercise"):
        cursor.execute("UPDATE exercises SET name = ?, sets = ?, reps = ? WHERE id = ?",
                       (name, sets, reps, exercise_id))
        conn.commit()
        print("Exercise updated successfully.")
    else:
        print("Exercise update canceled.")

def save_or_cancel(action):
    while True:
        choice = input(f"\nPress Enter to {action} or 2 to cancel: ")
        if choice == '':
            return True
        elif choice.lower() == '2':
            return False
        else:
            print("Invalid choice. Please try again.")

def delete_exercise(exercise_id):
    cursor.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
    conn.commit()
    print("Exercise deleted successfully.")


while True:
    print("\nWorkout Tracker")
    print("This application helps track workouts easily and efficiently")
    print("1. Create Exercise")
    print("2. View Exercises")
    print("3. Update Exercise")
    print("4. Delete Exercise")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("Enter details of new exercise")
        name = input("Enter exercise name: ")
        sets = int(input("Enter the number of sets: "))
        reps = int(input("Enter the number of reps: "))
        create_exercise(name, sets, reps)
    elif choice == '2':
        print("Tip: Return to home to add or update exercises")
        read_exercises()
    elif choice == '3':
        exercise_id = int(input("Enter the exercise ID to update: "))
        name = input("Enter the updated exercise name: ")
        sets = int(input("Enter the updated number of sets: "))
        reps = int(input("Enter the updated number of reps: "))
        update_exercise(exercise_id, name, sets, reps)
    elif choice == '4':
        exercise_id = int(input("Enter the exercise ID to delete: "))
        delete_exercise(exercise_id)
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()