from Menu import Menu
import logging
from Option import Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Select existing instance", "select()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Departments", "add_department()"),
    Option("Courses", "add_course()"),
    Option("Sections", "add_section()"),
    Option("Majors", "add_major()"),
    Option("Students", "add_student()"),
    Option("Declare Student to Major", "add_student_major()"),
    # Option("Enroll Student to Section", "add_enrollment()"),
    Option("Enroll Student to Section (Pass/Fail)", "add_enrollment_passfail()"),
    Option("Enroll Student to Section (Letter Grade)", "add_enrollment_grade()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Department", "delete_department()"),
    Option("Course", "delete_course()"),
    Option("Section", "delete_section()"),
    Option("Major", "delete_major()"),
    Option("Student", "delete_student()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Department courses", "list_department_courses()"),
    Option("Course sections", "list_course_sections()"),
    Option("Enrollment in section", "list_enrollment()"),
    Option("Declared students in major", "list_student_major()"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Department", "print(select_department())"),
    Option("Course", "print(select_course())"),
    Option("Section", "print(select_section())"),
    Option("Major", "print(select_major())"),
    Option("Student", "print(select_student())"),
    Option("Exit", "pass")
])
