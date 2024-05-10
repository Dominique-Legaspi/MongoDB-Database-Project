from ConstraintUtilities import select_general, unique_general, prompt_for_date, prompt_for_date_no_future
from Utilities import Utilities
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select
from Department import Department
from Course import Course
from Section import Section
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from datetime import time
from PassFail import PassFail
from LetterGrade import LetterGrade

def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add():
    menu_loop(add_select)


def list_members():
    menu_loop(list_select)

# --------------------------- SELECT FUNCTIONS
def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)

def select_department():
    return select_general(Department)

def select_course():
    return select_general(Course)

def select_section():
    return select_general(Section)

def select_student():
    return select_general(Student)

def select_major():
    return select_general(Major)

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')
    
def validate_time(input_str):
    try:
        hour_str, minute_str = input_str.split(':')

        hour = int(hour_str)
        minute = int(minute_str)
        
        start_time = time(8,0)
        end_time = time(19, 30)

        time_str = time(hour, minute)
        
        if start_time <= time_str < end_time:
            return input_str
        else:
            print('Time must be between 8:00 and 19:30 (8:00AM to 7:30PM)')
            add_section()
        
    except Exception as e:
        print('Time must be of format HH:MM in 24-hour clock', e)
        add_section()
    
    
    
# --------------------------- ADD FUNCTIONS 
def add_department():
    success: bool = False
    new_department = None
    while not success:
        new_department = Department(input('Name --> '),
                                    input('Abbreviation --> '),
                                    input('Chair name --> '),
                                    prompt_for_enum('Building --> ', Department, 'building'),
                                    int(input('Office --> ')),
                                    input('Description --> '))
        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_department.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new department:')
                print(Utilities.print_exception(e))
                
def add_course():
    success: bool = False
    new_course: Course
    department: Department
    while not success:
        department = select_department()
        new_course = Course(department,
                            input('Course name --> '),
                            int(input('Course number --> ')),
                            input('Description --> '),
                            int(input('Units --> ')))
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_course.save()
                department.add_course_to_department(new_course)
                department.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new course:')
                print(Utilities.print_exception(e))
                
def add_section():
    success: bool = False
    new_section: Section
    course: Course
    while not success:
        course = select_course()        
        new_section = Section(course,
                              int(input('Section number --> ')),
                              int(input('Section year --> ')),
                              prompt_for_enum('Semester --> ', Section, 'semester'),
                              prompt_for_enum('Building --> ', Section, 'building'),
                              int(input('Room number --> ')),
                              prompt_for_enum('Schedule', Section, 'schedule'),
                            #   int(time(int(input('Start hour (HH) (24-hour format) --> ')), int(input('Start minute (MM) --> '))).strftime('%H%M')), # mongoengine does not support Time only
                              str(validate_time(time(int(input('Start hour (24-hour clock) --> ')), int(input('Start minute --> '))).strftime('%H:%M'))),
                              input('Instructor --> '))
        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_section.save()
                course.add_item(new_section)
                course.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new section:')
                print(Utilities.print_exception(e))
                
def add_student():
    success: bool = False
    new_student: Student
    while not success:
        new_student = Student(input('Enter last name --> '),
                              input('Enter first name --> '),
                              input('Enter email --> '))
        violated_constraints = unique_general(new_student)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_student.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new student:')
                print(Utilities.print_exception(e))

def add_major():
    success: bool = False
    new_major: Major
    department: Department
    while not success:
        department = select_department()
        new_major = Major(department,
                          input('Enter name of major --> '),
                          input('Enter description --> '))
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:
            try:
                new_major.save()
                department.add_major_to_department(new_major)
                department.save()
                success = True
            except Exception as e:
                print('Exception trying to add the new major:')
                print(Utilities.print_exception(e))
      
def add_enrollment_passfail():
    success: bool = False
    student: Student
    section: Section
    new_enrollment: PassFail
    while not success:
        student = select_student()
        section = select_section()
        
        new_enrollment = PassFail(student, section,
                                    prompt_for_enum('Enter pass/fail status --> ', PassFail, 'status'),
                                    prompt_for_date_no_future('Enter application date (cannot be in the future):')) # new function to validate dates
        
        violated_constraints = unique_general(new_enrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:   
            try:
                new_enrollment.save()
                student.enroll_student(new_enrollment)
                section.enroll_student(new_enrollment)
                student.save()
                section.save()
                success = True
            except Exception as e:
                    print('Exception trying to enroll student to section:')
                    print(Utilities.print_exception(e))
                    
def add_enrollment_grade():
    success: bool = False
    student: Student
    section: Section
    new_enrollment: LetterGrade
    while not success:
        student = select_student()
        section = select_section()
        
        new_enrollment = LetterGrade(student, section,
                                    prompt_for_enum('Enter minimum satisfactory grade: ', LetterGrade, 'minSatisfactory'))
        
        violated_constraints = unique_general(new_enrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:   
            try:
                new_enrollment.save()
                student.enroll_student(new_enrollment)
                section.enroll_student(new_enrollment)
                student.save()
                section.save()
                success = True
            except Exception as e:
                    print('Exception trying to enroll student to section:')
                    print(Utilities.print_exception(e))

def add_student_major():
    success: bool = False
    student: Student
    major: Major
    new_declaration: StudentMajor
    while not success:
        student = select_student()
        major = select_major()
        new_declaration = StudentMajor(student, major,
                                       prompt_for_date_no_future('Enter declaration date (cannot be in the future):')) # new function to validate dates
        
        violated_constraints = unique_general(new_declaration)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('Try again')
        else:   
            try:
                new_declaration.save()
                student.declare_student(new_declaration)
                major.declare_student(new_declaration)
                student.save()
                major.save()
                success = True
            except Exception as e:
                    print('Exception trying to declare student to major:')
                    print(Utilities.print_exception(e))
         
         
# --------------------------- LIST FUNCTIONS 
def list_department_courses():
    department = select_department()
    courses = department.courses
    print('Number of courses in department:', len(courses))
    
    for course in courses:
        print(course)
        
def list_course_sections():
    course = select_course()
    sections = course.sections
    print('Number of sections in course:', len(sections))
    
    for section in sections:
        print(section)
        
def list_enrollment():
    section = select_section()
    enrollment = section.enrollment
    print('Number of students in section:', len(enrollment))
    
    for enrolled_student in enrollment:
        print(enrolled_student)

def list_student_major():
    major = select_major()
    students = major.students
    print('Number of students in major:', len(students))
    
    for student in students:
        print(student)


# --------------------------- DELETE FUNCTIONS
def delete_department(): 
    department = select_department()

    try:
        department.delete()
        print(f"Successfully deleted the {department.name} department.\n")
    except Exception as error:
        print(error)

def delete_course(): 
    course = select_course()

    try:
        # Remove course from department
        department = course.department
        department.remove_course_from_department(course)
        department.save()

        course.delete()
        print(f"Successfully deleted the course.\n")
    except Exception as error:
        print(error) 

def delete_section(): 
    section = select_section()

    try:
        # Remove all enrollments in the section
        for enr in section.enrollment:
            student = enr.student
            student.remove_student(enr) 
            student.save()
            enr.delete()

        # Remove section from course
        course = section.course
        course.remove_section(section)
        course.save()

        section.delete()
        print(f"Successfully deleted the section.\n")
    except Exception as error:
        print(error)

def delete_student():
    student = select_student()

    try:
        # Remove student from majors
        for sm in student.majors:
            major = sm.major
            major.remove_student(sm)
            major.save()
            sm.delete()

        # Remove student from enrollments
        for enr in student.enrollment:
            section = enr.section
            section.remove_student(enr)
            section.save()
            enr.delete()
    
        student.delete()
        print(f"Successfully deleted the student.\n")
    except Exception as error:
        print(error) 

def delete_major(): 
    major = select_major()

    try:
        # Remove major from students
        for sm in major.students:
            student = sm.student
            student.remove_major(sm)
            student.save()
            sm.delete()
        
        # Remove major from department
        department = major.department
        department.remove_major_from_department(major)
        department.save()

        major.delete()
        print(f"Successfully deleted the major.\n")
    except Exception as error:
        print(error) 
    
    


if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
