# cs361microservices
To send a request to the microservice_A program to create a new workout, the create_communication function must be used to first update the communication.db. The microservice is constantly looking for a change to the ‘action’ column in the communication table in communication.db. If ‘action’ is set to the integer 1, the microservice will add the workout specified in main.py to the workout_tracker.db.

Example code:
In main.py:
print("Enter details of new exercise")
name = input("Enter exercise name: ")
sets = int(input("Enter the number of sets: "))
reps = int(input("Enter the number of reps: "))
create_communication(1, name, sets, reps)
This will update the communications table with the ‘action’ of 1 and workout details.

The microservice will then read an ‘action’ of 1 which creates a workout with ‘name’, ‘sets’, and ‘reps’, and updated the workout to the workout_tracker database.

After sending a request to microservice_A, the workout data will be automatically sent to the workout_tacker database and can be accessed by your main.py program or other microservices with access to the workout_tacker database.

![image](https://github.com/user-attachments/assets/433bb457-7911-48dc-b17d-2951dfb2d3b5)
