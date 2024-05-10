# import mongoengine
from mongoengine import *
from Major import Major
from Student import Student
import datetime

class StudentMajor(Document):
    # student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    # major = ReferenceField(Major, required=True, reverse_delete_rule=mongoengine.DENY)
    student = ReferenceField(Student, required=True)
    major = ReferenceField(Major, required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)
    
    meta = {'collection': 'student_major',
            'indexes': [
                {'unique': True, 'fields': ['student', 'major'], 'name': 'student_major_pk'}
            ]}
    
    def __init__(self, student: Student, major: Major, declarationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.major = major
        self.declarationDate = declarationDate
        
    def __str__(self):
        return f"{self.student}, major: {self.major.name}"
