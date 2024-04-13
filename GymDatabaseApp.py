import datetime
import psycopg # PostgreSQL adapter for Python


# Create new user.
def createNewUser(firstName, lastName, phoneNumber, email, street, homeNumber, postalCode, password):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO member (password, first_name, last_name, phone_number, email, street, home_number, postal_code) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s) RETURNING member_id;", (password, firstName, lastName, phoneNumber, email, street, homeNumber, postalCode))
        memberId = cursor.fetchone()[0]

    conn.commit()

    print(f"Your member ID ({memberId}) has been created.\n")


#############################
## Existing User Functions ##
#############################

# Show member's personal information
def showPersonalInformation(memberId):
    # Print the headers (with the under line "------")
    columnNames = ["Member ID", "First Name", "Last Name", "Phone Number", "Email", "Street", "Home Number", "Postal Code", "Height (cm)", "Weight (kg)"]
    columnsizes = [12, 20, 20, 15, 30, 30, 14, 14, 14, 14]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT member_id, first_name, last_name, phone_number, email, street, home_number, postal_code, height, weight FROM member WHERE member_id=%s;", (memberId,))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Show the member's dashboard
def showDashboard(memberId):
    print("Dashboard")
    print("---------")

    with conn.cursor() as cursor:
        cursor.execute("SELECT height, weight FROM member WHERE member_id=%s;", (memberId,))
        (height, weight) = cursor.fetchone()[0:2]
        print(f"Height: {height}\tWeight: {weight}\n")

        print("Goals:")
        cursor.execute("SELECT goal_id, weight_goal, start_date, end_date FROM fitness_goal WHERE member_id=%s;", (memberId,))
        for record in cursor:
            print(f"ID: {record[0]}\tWeight Goal: {record[1]}\tStart Date: {record[2]}\tEnd Date: {record[3]}")

        print()

        print("Routines:")
        cursor.execute("SELECT routine_id, name, description FROM routine WHERE member_id=%s;", (memberId,))
        for record in cursor:
            print(f"ID: {record[0]}\tName: {record[1]}\tDescription: {record[2]}")
    
        print()

        print("Achievements:")
        cursor.execute("SELECT achievement FROM achievement WHERE member_id=%s;", (memberId,))
        for record in cursor:
            print(f"{record[0]}")

    print()


# Show list of bookings (both private sessions and classes)
def showBooking(memberId):
    print("Private Sessions:")
    # Print the headers (with the under line "------")
    columnNames = ["Trainer ID", "Trainer's First Name", "Trainer's Last Name", "Date", "Start Time", "End Time"]
    columnsizes = [12, 22, 22, 12, 12, 12]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT t.trainer_id, t.first_name, t.last_name, ps.date, ps.starting_time, ps.ending_time FROM private_session as ps NATURAL JOIN trainer as t WHERE member_id=%s;", (memberId,))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("\nClasses:")
    # Print the headers (with the under line "------")
    columnNames = ["Class ID", "Name", "Date", "Start Time", "End Time", "Room Number", "Trainer ID", "Trainer's Fist Name", "Trainer's Last Name"]
    columnsizes = [10, 20, 12, 12, 12, 14, 12, 22, 22]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT c.class_id, c.name, c.date, c.starting_time, c.ending_time, c.room_number, t.trainer_id, t.first_name, t.last_name FROM (class as c NATURAL JOIN member_class as mc) NATURAL JOIN trainer as t WHERE mc.member_id=%s", (memberId,))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)

    print()


# List trainers' availabilities
def listTrainerAvailabilities():
    # Print the headers (with the under line "------")
    columnNames = ["Availability", "Trainer ID", "First Name", "Last Name"]
    columnsizes = [26, 12, 20, 20]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT A.date_time, T.trainer_id, T.first_name, T.last_name FROM trainer as T NATURAL JOIN availability as A;")
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Schedule a private training session
def scheduleTrainingSession(dateTime, trainerId, memberId):
    date = dateTime.date()
    startTime = dateTime.time()
    endTime = (dateTime + datetime.timedelta(hours=1)).time()

    with conn.cursor() as cursor:
        cursor.execute("SELECT Count(trainer_id) FROM availability WHERE trainer_id=%s AND date_time=%s;", (trainerId, dateTime))
        countResult = cursor.fetchone()[0]
        if (countResult == 1):
            cursor.execute("INSERT INTO private_session (trainer_id, member_id, date, starting_time, ending_time) VALUES (%s, %s, %s, %s, %s);", (trainerId, memberId, date, startTime, endTime))
            cursor.execute("DELETE FROM availability WHERE trainer_id=%s AND date_time=%s;", (trainerId, dateTime))
            conn.commit()
            print(f"Your have schedule a session on {date} at {startTime} successfully.\n")
        else:
            print("This availability doesn't exist.\n")


# Cancel a private training session
def cancelTrainingSession(trainerId, memberId, date):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM private_session WHERE trainer_id=%s AND member_id=%s AND date=%s;", (trainerId, memberId, date))

    conn.commit()

    print(f"Your have cancelled a session on {date} with {trainerId} successfully.\n")


# List the available classes
def memberListClasses():
    # Print the headers (with the under line "------")
    columnNames = ["Class ID", "Name", "Date", "Start Time", "End Time", "Room Number"]
    columnsizes = [12, 30, 15, 10, 10, 14]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT class_id, name, date, starting_time, ending_time, room_number FROM class;")
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Record a member joining a class
def joinClass(classId, memberId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO member_class (member_id, class_id) VALUES (%s, %s);", (memberId, classId))

    conn.commit()

    print(f"Your have join class ID ({classId}) successfully.\n")


# Record a member leaving a class
def leaveClass(classId, memberId):
    with conn.cursor() as cursor:
            cursor.execute("DELETE FROM member_class WHERE member_id=%s AND class_id=%s;", (memberId, classId))

    conn.commit()

    print(f"Your have left class ID ({classId}) successfully.\n")


# Update a member's specified information
def changeInformation(memberId, field, newValue):
    print(field)
    with conn.cursor() as cursor:
        cursor.execute("UPDATE member SET %s = %%s WHERE member_id = %%s" % field, (newValue, memberId))

    conn.commit()

    print(f"The {field} for member {memberId} has been updated to {newValue} successfully.\n")


# Create a goal
def createGoal(weightGoal, startDateTime, endDateTime, memberId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO fitness_goal (weight_goal, start_date, end_date, member_id) VALUES (%s, %s, %s, %s) RETURNING goal_id;", (weightGoal, startDateTime, endDateTime, memberId))
        goalId = cursor.fetchone()[0]

    conn.commit()

    print(f"Your goal ID ({goalId}) has been created.\n")


# Delete a goal
def deleteGoal(goal_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM fitness_goal WHERE goal_id=%s;", (goal_id,))

    conn.commit()

    print(f"Your goal ID ({goal_id}) has been deleted.\n")


# Create an achievement
def createAchievement(achievement, memberId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO achievement (member_id, achievement) VALUES (%s, %s);", (memberId, achievement))

    conn.commit()

    print(f"Your achievement has been created.\n")


# Lookup a routine
def lookupRoutine(routineId):
    # Print the headers (with the under line "------")
    columnNames = ["Exercise"]
    columnsizes = [30]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT exercise_name FROM routine_exercise WHERE routine_id=%s;", (routineId,))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Create a routine
def createRoutine(name, description, memberId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO routine (name, description, member_id) VALUES (%s, %s, %s) RETURNING routine_id;", (name, description, memberId))
        routineId = cursor.fetchone()[0]

    conn.commit()

    print(f"Your routine ID ({routineId}) has been created.\n")


# Add an exercise to a routine
def addExerciseToRoutine(routineId, exercise):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO routine_exercise (routine_id, exercise_name) VALUES (%s, %s);", (routineId, exercise))

    conn.commit()

    print(f"The exercise ({exercise}) has been added to routine {routineId}.\n")


# Remove an exercise from a routine
def removeExerciseToRoutine(routineId, exercise):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM routine_exercise WHERE routine_id=%s AND exercise_name=%s;", (routineId, exercise))

    conn.commit()

    print(f"The exercise ({exercise}) has been removed from routine {routineId}.\n")


# Delete a routine
def deleteRoutine(routineId):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM routine_exercise WHERE routine_id=%s;", (routineId,)) # Delete dependencies first
        cursor.execute("DELETE FROM routine WHERE routine_id=%s;", (routineId,))

    conn.commit()

    print(f"Your routine ID ({routineId}) has been deleted.\n")


# Show the list of exercises
def showExerciseList():
    # Print the headers (with the under line "------")
    columnNames = ["Exercise", "Type"]
    columnsizes = [30, 20]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM exercise;")
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensure that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


#######################
## Trainer Functions ##
#######################

# Retrieve the information of a specified user (searched by name)
def trainerSearchUserByName(firstName, lastName):
    # Print the headers (with the under line "------")
    columnNames = ["Member ID", "First Name", "Last Name", "Phone Number", "Email"]
    columnsizes = [12, 20, 20, 15, 30]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT member_id, first_name, last_name, phone_number, email FROM member WHERE first_name=%s AND last_name=%s;", (firstName, lastName))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Show the availabilities of a trainer
def showAvailabilities(trainerId):
    # Print the headers (with the under line "------")
    columnNames = ["Availabilities"]
    columnsizes = [20]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT date_time FROM availability WHERE trainer_id=%s;", (trainerId,))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Add an availability
def addAvailability(trainerId, dateTime):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO availability (trainer_id, date_time) VALUES (%s, %s);", (trainerId, dateTime))

    conn.commit()

    print(f"Your availability ({dateTime}) has been added successfully.\n")


# Delete an availability
def deleteAvailability(trainerId, dateTime):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM availability WHERE trainer_id=%s AND date_time=%s;", (trainerId, dateTime))

    conn.commit()

    print(f"Your availability ({dateTime}) has been deleted successfully.\n")


#####################
## Staff Functions ##
#####################

# Retrieve the information of a specified user (searched by name)
def staffSearchUserByName(firstName, lastName):
    # Print the headers (with the under line "------")
    columnNames = ["Member ID", "First Name", "Last Name", "Phone Number", "Email", "Street", "Home Number", "Postal Code"]
    columnsizes = [12, 20, 20, 15, 30, 30, 14, 14]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT member_id, first_name, last_name, phone_number, email, street, home_number, postal_code FROM member WHERE first_name=%s AND last_name=%s;", (firstName, lastName))
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Retrieve and displays all records from the equipment table.
def getAllEquipment():
    # Print the headers (with the under line "------")
    columnNames = ["Bar Code", "Model", "Last Maintenance", "Room Number"]
    columnsizes = [12, 30, 15, 6]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM equipment;")
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Update the last_maintenance date of an equipment
def updateEquipmentLastMaintenance(barCode, date):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE equipment SET last_maintenance = %s WHERE bar_code = %s;", (date, barCode))

    conn.commit()

    print(f"The last_maintenance date for equipment: {barCode} has been updated to {date} successfully.\n")


# Create an invoice
def createInvoice(invoiceDate, amount, dueDate, memberId, staffId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO invoice (invoice_date, amount, due_date, member_id, staff_id) VALUES (%s, %s, %s, %s, %s) RETURNING invoice_number;", (invoiceDate, amount, dueDate, memberId, staffId))
        invoiceNumber = cursor.fetchone()[0]

    conn.commit()

    print(f"The invoice {invoiceNumber} has been created successfully.\n")


# Receive a payment
def receivePayment(date, amount, method, memberId, staffId):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO payment (date, amount, method, member_id, staff_id) VALUES (%s, %s, %s, %s, %s) RETURNING transaction_id;", (date, amount, method, memberId, staffId))
        transactionId = cursor.fetchone()[0]

    conn.commit()

    print(f"The payment {transactionId} has been created successfully.\n")


# List classes
def staffListClasses():
    # Print the headers (with the under line "------")
    columnNames = ["Class ID", "Name", "Date", "Start Time", "End Time", "Room Number", "Trainer ID", "Trainer's First Name", "Trainer's Last Name"]
    columnsizes = [12, 30, 15, 10, 10, 14, 12, 22, 22]
    header = "|"
    headerLine = "|"

    for i in range(len(columnNames)):
        header = header + columnNames[i].center(columnsizes[i]) + "|"
        for j in range(columnsizes[i]):
            headerLine = headerLine + "-"
        headerLine = headerLine + "|"
    
    print(header)
    print(headerLine)

    # Print the data
    with conn.cursor() as cursor:
        cursor.execute("SELECT c.class_id, c.name, c.date, c.starting_time, c.ending_time, c.room_number, t.trainer_id, t.first_name, t.last_name FROM class as c NATURAL JOIN trainer as t;")
        for record in cursor:
            recordString = "|"
            columnNumber = -1
            for entry in record:
                entry = str(entry) # Ensures that entry is a string
                columnNumber = columnNumber + 1
                entry = entry.center(columnsizes[columnNumber])
                recordString = recordString + entry + "|"
            print(recordString)
    
    print("")


# Create a class
def createClass(name, date, starting_time, ending_time, roomNumber, trainerId, staff_id):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO class (name, date, starting_time, ending_time, room_number, trainer_id, staff_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING class_id;", (name, date, starting_time, ending_time, roomNumber, trainerId, staff_id))
        classId = cursor.fetchone()[0]

    conn.commit()

    print(f"The class {classId} has been created successfully.\n")


# Delete a class
def deleteClass(classId):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM member_class WHERE class_id=%s;", (classId,)) # Delete dependencies first
        cursor.execute("DELETE FROM class WHERE class_id=%s;", (classId,))

    conn.commit()

    print(f"Your availability ({classId}) has been deleted successfully.\n")


####################
## Menu Functions ##
####################

# Print the Existing User menu prompt.
def printExistingUserPrompt():
    print("Please select an option:")
    print("1- Show personal information")
    print("2- Show dashboard")
    print("3- Show bookings")
    print("4- Schedule personal training session")
    print("5- Cancel a training session")
    print("6- Join a class")
    print("7- Leave a class")
    print("8- Update personal information and health metrics")
    print("9- Create a goal")
    print("10- delete a goal")
    print("11- Add achievement")
    print("12- Lookup a routine")
    print("13- Create a routine")
    print("14- modify a routine")
    print("15- delete a routine")
    print("16- Show list of exercises")
    print("0- Logout")


# Print the Trainer menu prompt.
def printTrainerPrompt():
    print("Please select an option:")
    print("1- Search member by name")
    print("2- Show availabilities")
    print("3- Add availability")
    print("4- Delete availability")
    print("0- Logout")


# Print the Staff menu prompt.
def printStaffPrompt():
    print("Please select an option:")
    print("1- Search member by name")
    print("2- Create an invoice")
    print("3- Receive a payment")
    print("4- Show list of equipment")
    print("5- Update last_maintenance date of an equipment")
    print("6- List classes")
    print("7- Create a class")
    print("8- Delete a class")
    print("0- Logout")


# Print the main menu prompt.
def printMainPrompt():
    print("Please select an option:")
    print("1- New User")
    print("2- Existing User")
    print("3- Trainer")
    print("4- Administration Staff")
    print("0- Quit")


# This is the Existing User prompt loop.
def existingUserPromptLoop(memberId):
    while (True):
        print(f"Hello Member {memberId}!")

        printExistingUserPrompt()

        userInput = input("Please enter the number corresponding to your choice: ")
        print("")

        if (userInput == "0"):
            return
        
        elif (userInput == "1"):
            showPersonalInformation(memberId)

        elif (userInput == "2"):
            showDashboard(memberId)

        elif (userInput == "3"):
            showBooking(memberId)

        elif (userInput == "4"):
            listTrainerAvailabilities()
            print("Please complete the information required to schedule a trainer session with a trainer:")
            print("(Please note that all training sessions are for a period of 1 hour.)")
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            hour = int(input("Hour: "))
            dateTime = datetime.datetime(year, month, day, hour)
            trainerId = input("Trainer ID: ")
            scheduleTrainingSession(dateTime, trainerId, memberId)

        elif (userInput == "5"):
            print("Please complete the information required to cancel a session with a trainer:")
            trainerId = input("Trainer ID: ")
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            date = datetime.datetime(year, month, day)
            cancelTrainingSession(trainerId, memberId, date)

        elif (userInput == "6"):
            memberListClasses()
            classId = input("Please enter the class ID that you wish to join: ")
            joinClass(classId, memberId)

        elif (userInput == "7"):
            classId = input("Please enter the class ID that you wish to leave: ")
            leaveClass(classId, memberId)

        elif (userInput == "8"):
            field = input("Which field to update? ('password', 'phone_number', 'email', 'street', 'home_number', 'postal_code', 'height', 'weight'): ")
            newValue = input("New value: ")
            if (field == "home_number" or field == "height" or field == "weight"):
                newValue = int(newValue)
            changeInformation(memberId, field, newValue)

        elif (userInput == "9"):
            print("Please complete the information required to create a goal:")
            weightGoal = int(input("Weight goal (kg): "))
            startYear = int(input("Starting year: "))
            startMonth = int(input("Starting month: "))
            startDay = int(input("Starting day: "))
            startDateTime = datetime.datetime(startYear, startMonth, startDay)
            endYear = int(input("Ending year: "))
            endMonth = int(input("Ending month: "))
            endDay = int(input("Ending day: "))
            endDateTime = datetime.datetime(endYear, endMonth, endDay)
            createGoal(weightGoal, startDateTime, endDateTime, memberId)

        elif (userInput == "10"):
            goalId = input("Please enter the goal id that you wish to delete: ")
            deleteGoal(goalId)

        elif (userInput == "11"):
            achievement = input("Please enter the achievement that you wish to create: ")
            createAchievement(achievement, memberId)

        elif (userInput == "12"):
            routineId = input("Please enter the routine ID that you wish to lookup: ")
            lookupRoutine(routineId)

        elif (userInput == "13"):
            print("Please complete the information required to create a routine:")
            name = input("Routine name: ")
            description = input("Routine description: ")
            createRoutine(name, description, memberId)

        elif (userInput == "14"):
            routineId = input("Please enter the routine id that you wish to modify: ")
            action = input("Which action do you which to perform? ('add' or 'delete' an exercise to the routine) ")
            if (action == "add"):
                exercise = input("Please enter the exercise that you wish to add to the routine: ")
                addExerciseToRoutine(routineId, exercise)
            elif (action == "delete"):
                exercise = input("Please enter the exercise that you wish to remove from the routine: ")
                removeExerciseToRoutine(routineId, exercise)

        elif (userInput == "15"):
            routineId = input("Please enter the routine id that you wish to delete: ")
            deleteRoutine(routineId)

        elif (userInput == "16"):
            showExerciseList()

        else:
            print("Not a valid option!\n")


# This is the Trainer prompt loop.
def trainerPromptLoop(trainerId):
    while (True):
        print(f"Hello Trainer {trainerId}!")

        printTrainerPrompt()

        userInput = input("Please enter the number corresponding to your choice: ")
        print("")

        if (userInput == "0"):
            return
        
        elif (userInput == "1"):
            print("Please enter the name of the member:")
            firstName = input("First Name: ")
            lastName = input("Last Name: ")
            trainerSearchUserByName(firstName, lastName)

        elif (userInput == "2"):
            showAvailabilities(trainerId)
        
        elif (userInput == "3"):
            print("Please complete the information required to create an availability block (1 hour per block):")
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            hour = int(input("Hour: "))
            dateTime = datetime.datetime(year, month, day, hour)
            addAvailability(trainerId, dateTime)

        elif (userInput == "4"):
            print("Please complete the information required to delete an availability block:")
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            hour = int(input("Hour: "))
            dateTime = datetime.datetime(year, month, day, hour)
            deleteAvailability(trainerId, dateTime)

        else:
            print("Not a valid option!\n")


# This is the Staff prompt loop.
def staffPromptLoop(staffId):
    while (True):
        print(f"Hello Staff {staffId}!")

        printStaffPrompt()

        userInput = input("Please enter the number corresponding to your choice: ")
        print("")

        if (userInput == "0"):
            return
        
        elif (userInput == "1"):
            print("Please enter the name of the member:")
            firstName = input("First Name: ")
            lastName = input("Last Name: ")
            staffSearchUserByName(firstName, lastName)


        elif (userInput == "2"):
            print("Please enter the invoice's details:")
            invoiceYear = int(input("Invoice's year: "))
            invoiceMonth = int(input("Invoice's month: "))
            invoiceDay = int(input("Invoice's day: "))
            invoiceDate = datetime.datetime(invoiceYear, invoiceMonth, invoiceDay)
            amount = input("Invoice amount: ")
            dueYear = int(input("Invoice due date's year: "))
            dueMonth = int(input("Invoice due date's month: "))
            dueDay = int(input("Invoice due date's day: "))
            dueDate = datetime.datetime(dueYear, dueMonth, dueDay)
            memberId = input("Invoiced Member ID: ")
            createInvoice(invoiceDate, amount, dueDate, memberId, staffId)

        elif (userInput == "3"):
            print("Please enter the payment's details:")
            paymentYear = int(input("payment's year: "))
            paymentMonth = int(input("payment's month: "))
            paymentDay = int(input("payment's day: "))
            paymentDate = datetime.datetime(paymentYear, paymentMonth, paymentDay)
            amount = input("payment amount: ")
            method = input("payment method: ")
            memberId = input("payment's Member ID: ")
            receivePayment(paymentDate, amount, method, memberId, staffId)

        elif (userInput == "4"):
            getAllEquipment()

        elif (userInput == "5"):
            barCode = input("Please enter the bar code number of the equipment you wish to update: ")
            year = int(input("Please enter the maintenance's year: "))
            month = int(input("Please enter the maintenance's month: "))
            day = int(input("Please enter the maintenance's day: "))
            date = datetime.datetime(year, month, day)
            updateEquipmentLastMaintenance(barCode, date)

        elif (userInput == "6"):
            staffListClasses()

        elif (userInput == "7"):
            print("Please enter the class's details:")
            name = input("Class name: ")
            year = int(input("Class's year: "))
            month = int(input("Class's month: "))
            day = int(input("Class's day: "))
            date = datetime.datetime(year, month, day)
            hour = int(input("Class's starting hour: "))
            starting_time = datetime.time(hour)
            length = int(input("Class length (in hours): "))
            ending_time = datetime.time(hour + length)
            roomNumber = input("Class's room number: ")
            trainerId = input("Class's trainer (ID): ")
            createClass(name, date, starting_time, ending_time, roomNumber, trainerId, staffId)

        elif (userInput == "8"):
            classId = input("Please enter the class id you wish to delete: ")
            deleteClass(classId)
                
        else:
            print("Not a valid option!\n")


# This is the main prompt loop.
def mainPromptLoop():
    while (True):
        print("\nMain Menu")

        printMainPrompt()

        userInput = input("Please enter the number corresponding to your choice: ")
        print("")

        if (userInput == "0"):
            exit(0)

        elif (userInput == "1"):
            print("Please answer the following questions:")
            firstName = input("First Name: ")
            lastName = input("Last Name: ")
            phoneNumber = input("Phone Number (10 digits, no spaces, no special characters): ")
            email = input("Email: ")
            street = input("Address Street: ")
            homeNumber = input("Home Number: ")
            postalCode = input("Postal Code: ")
            password = input("Password: ")
            createNewUser(firstName, lastName, phoneNumber, email, street, homeNumber, postalCode, password)

        elif (userInput == "2"):
            print("Please enter your credentials:")
            memberId = input("Member ID: ")
            password = input("Password: ")
            print("")
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(member_id) FROM member WHERE member_id=%s AND password=%s;", (memberId, password))
                countResult = cursor.fetchone()[0]
            if (countResult == 1):
                existingUserPromptLoop(memberId)
            else:
                print("Login failed. Please ensure that you have entered the correct credentials.")

        elif (userInput == "3"):
            print("Please enter your credentials:")
            trainerId = input("Trainer ID: ")
            password = input("Password: ")
            print("")
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(trainer_id) FROM trainer WHERE trainer_id=%s AND password=%s;", (trainerId, password))
                countResult = cursor.fetchone()[0]
            if (countResult == 1):
                trainerPromptLoop(trainerId)
            else:
                print("Login failed. Please ensure that you have entered the correct credentials.")

        elif (userInput == "4"):
            print("Please enter your credentials:")
            staffId = input("Staff ID: ")
            password = input("Password: ")
            print("")
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(staff_id) FROM administration_staff WHERE staff_id=%s AND password=%s;", (staffId, password))
                countResult = cursor.fetchone()[0]
            if (countResult == 1):
                staffPromptLoop(staffId)
            else:
                print("Login failed. Please ensure that you have entered the correct credentials.")

        else:
            print("Not a valid option!\n")


# The main function where the connection to the database is established. It then calls the promptLoop() function.
# The conn variable is made global so it can be used by the other functions.
def main():
    try:
        global conn
        conn = psycopg.connect("dbname=Project_V2 user=postgres password=postgres host=localhost port=5432")
        mainPromptLoop()

    except psycopg.OperationalError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()