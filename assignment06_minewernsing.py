# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   Mine Wernsing,5/17/2024,Created Script
# ------------------------------------------------------------------------------------------ #

import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''

FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list[dict[str, str]] = []  # a table of student data
menu_choice: str  # Holds the choice made by the user


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with json files

    Change Log: (Who, When, What)
    Mine Wernsing,5/17/2024,Created Class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: list
        """

        file = None

        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except Exception as error_details:
            IO.output_error_message(message="Error: There was a problem with reading the file.", error=error_details)

        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file and with data from a list of dictionary rows

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: None
        """
        file = None

        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as error_details:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_message(message=message, error=error_details)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    Mine Wernsing,5/17/2024,Created Class
    Mine Wernsing,5/17/2024,Added menu output and input functions
    Mine Wernsing,5/17/2024,Added a function to display the data
    Mine Wernsing,5/17/2024,Added a function to display custom error messages

    """

    @staticmethod
    def output_error_message(message: str, error: Exception = None):
        """ This function displays a custom error message to the user

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message--")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: None
        """
        print()  # Adding extra space to make it look nicer
        print(menu)
        print()  # Adding extra space to make it look nicer

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user
        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please choose only 1, 2, 3, or 4")
        except Exception as error_details:
            IO.output_error_message(error_details.__str__())  # Not passing error details to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the students and course names to the user

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        Change Log: (Who, When, What)
        Mine Wernsing,5/17/2024,Created Function

        :return: list with the new student data
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("Student first name must be alphabetic. ")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("Student last name must be alphabetic. ")

            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as error_details:
            IO.output_error_message(message="One of the values was not the correct type of data", error=error_details)

        except Exception as error_details:
            IO.output_error_message(message="Error: There was a problem with your entered data.", error=error_details)

        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present choices and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, 3 or 4")

print("Program Ended")
