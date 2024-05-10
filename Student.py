import mongoengine
from mongoengine import *

class Student(Document):
    """An individual enrolled in an academic institution to acquire skillset, knowledge, and qualifications."""
    lastName = StringField(db_field='last_name', max_length=80, required=True)
    firstName = StringField(db_field='first_name', max_length=80, required=True)
    email = EmailField(db_field='email', max_length=180, required=True)
    majors = ListField(ReferenceField('StudentMajor'), db_field='majors')
    enrollment = ListField(ReferenceField('Enrollment'), db_field='enrollment')
    
    meta = {'collection': 'students',
        'indexes': [
            {'unique': True, 'fields': ['email'], 'name': 'students_uk_01'},
            {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_02'}
        ]}

    def __init__(self, lastName: str, firstName: str, email: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lastName = lastName
        self.firstName = firstName
        self.email = email
        if self.majors is None:
            self.majors = []
        if self.enrollment is None:
            self.enrollment = []
    
    def __str__(self):
        return f"Student: {self.lastName}, {self.firstName} - Email: {self.email}"
    
    def declare_student(self, major):
        self.majors.append(major)
        
    def enroll_student(self, student):
        for already_enrolled_student in self.enrollment:
            if student.equals(already_enrolled_student):
                return  # student is already enrolled, ignore add
        self.enrollment.append(student)

    def remove_major(self, major):
        self.majors.remove(major)
        
    def remove_student(self, student):
        self.enrollment.remove(student)