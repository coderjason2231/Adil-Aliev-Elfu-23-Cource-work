import json

# Singleton Pattern for Authentication Manager


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AuthenticationManager(metaclass=SingletonMeta):
    def __init__(self):
        self.users = {"admin": "password"}  # Simplified example

    def authenticate(self, username, password):
        return username in self.users and self.users[username] == password

# Factory Pattern for Storage Handler


class StorageHandler:
    def save(self, data):
        pass

    def load(self):
        pass


class FileStorageHandler(StorageHandler):
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def load(self):
        with open(self.filename, 'r') as file:
            return json.load(file)


class Factory:
    @staticmethod
    def get_storage_handler():
        return FileStorageHandler('students.json')

# Base Person class and Inheritance for Student


class Person:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone


class Student(Person):
    def __init__(self, roll_no=None, name=None, phone_number=None, address=None, grade=None, student_class=None):
        if roll_no is None:
            self.roll_no = input("Enter student Roll number: ")
            self.name = input("Enter student Name: ")
            self.phone_number = input("Enter student phone number: ")
            self.address = input("Enter student address: ")
            self.grade = input("Enter student grades: ")
            self.student_class = input("Enter student class [Example: 1-9]: ")
            super().__init__(self.name, self.address, self.phone_number)
            print("\nStudent added successfully")
        else:
            self.roll_no = roll_no
            self.name = name
            self.phone_number = phone_number
            self.address = address
            self.grade = grade
            self.student_class = student_class
            super().__init__(name, address, phone_number)

    def get_details(self):
        print("\nStudent details\n")
        print("\tRoll number:", self.roll_no)
        print("\tStudent name:", self.name)
        print("\tStudent phone number:", self.phone_number)
        print("\tStudent address:", self.address)
        print("\tClass:", self.student_class)
        print("\tGrade:", self.grade)

    def update_student(self):
        print("\nSelect option to update details\n")
        print("\t1) To Change Student Name")
        print("\t2) To Change Student Phone Number")
        print("\t3) To Change Student Address")
        print("\t4) To Change Student Class")
        option = input("\tEnter any above given option: ")

        if option == "1":
            self.name = input("\tEnter new student name: ")
            print("\n\tStudent name changed successfully\n")
        elif option == "2":
            self.phone_number = input("\tEnter new phone number: ")
            print("\n\tStudent phone number changed successfully\n")
        elif option == "3":
            self.address = input("\tEnter new student address: ")
            print("\n\tStudent address changed successfully\n")
        elif option == "4":
            self.student_class = input("\tEnter student's new class name: ")
            print("\n\tStudent class changed successfully\n")
        else:
            print("\n\tYou have chosen an invalid option")

        self.get_details()

# Main Application


class SchoolSystem:
    def __init__(self):
        self.storage = Factory.get_storage_handler()
        self.auth_manager = AuthenticationManager()
        self.students = self.load_students()
        self.school_name = "Evergreen Academy"

    def load_students(self):
        try:
            students_data = self.storage.load()
            return {
                stu['roll_no']: Student(
                    roll_no=stu.get('roll_no'),
                    name=stu.get('name'),
                    phone_number=stu.get('phone_number'),
                    address=stu.get('address'),
                    grade=stu.get('grade'),
                    student_class=stu.get('student_class')
                ) for stu in students_data
            }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Failed to load student data: {str(e)}")
            return {}

    def add_student(self):
        student = Student()
        self.students[student.roll_no] = student
        self.save_students()
        print("Student added successfully.")

    def save_students(self):
        students_data = [vars(stu) for stu in self.students.values()]
        self.storage.save(students_data)

    def get_student_details(self, roll_no):
        if roll_no in self.students:
            self.students[roll_no].get_details()
        else:
            print("Student not found.")

    def update_student_details(self, roll_no):
        if roll_no in self.students:
            self.students[roll_no].update_student()
        else:
            print("Student not found.")

    def remove_student(self, roll_no):
        if roll_no in self.students:
            del self.students[roll_no]
            self.save_students()
            print(f"Student {roll_no} deleted successfully.")
        else:
            print("No student with that roll number.")

    def update_school_name(self, new_name):
        self.school_name = new_name
        print("School name changed successfully to", self.school_name)

    def get_total_students(self):
        print("Total number of students in school:", len(self.students))

    def get_all_students_details(self):
        if self.students:
            print("All student details:")
            for sNo, student in enumerate(self.students.values(), 1):
                print(f"\nStudent {sNo}")
                student.get_details()
        else:
            print("\tNo students there")

    def run(self):
        if not self.auth_manager.authenticate(input("Username: "), input("Password: ")):
            print("Authentication Failed")
            return
        option = 'y'
        while option.lower() == 'y':
            print(f"Welcome to {self.school_name} management system\n")
            print("\t1) To get student details")
            print("\t2) To add new student")
            print("\t3) To remove student")
            print("\t4) To update student details")
            print("\t5) To update school name")
            print("\t6) To get number of students in school")
            print("\t7) To get all student details")
            option = input("Enter the number of one of the given options: ")
            print()

            if option == "1":
                roll_no = input("\tEnter the roll number of a student: ")
                self.get_student_details(roll_no)
            elif option == "2":
                self.add_student()
            elif option == "3":
                roll_no = input("\tEnter the roll number of a student: ")
                self.remove_student(roll_no)
            elif option == "4":
                roll_no = input("\tEnter the roll number of a student: ")
                self.update_student_details(roll_no)
            elif option == "5":
                new_school_name = input("\tEnter the new school name: ")
                self.update_school_name(new_school_name)
            elif option == "6":
                self.get_total_students()
            elif option == "7":
                self.get_all_students_details()
            else:
                print("\n\tInvalid option selected")

            option = input("\nDo you want to continue? [y/n]: ")


if __name__ == "__main__":
    system = SchoolSystem()
    system.run()
