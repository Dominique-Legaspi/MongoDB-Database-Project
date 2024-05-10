from mongoengine import *
from enum import Enum
from Enrollment import Enrollment
from Student import Student
from Section import Section
import datetime

class Status(Enum):
    PASS = 'Pass'
    FAIL = 'Fail'

class PassFail(Enrollment):
    status = EnumField(Status, required=True)
    applicationDate = DateTimeField(db_field='application_date', required=True)
    
    def __init__(self, student: Student, section: Section, status: Status, applicationDate: datetime, *args, **kwargs):
        super().__init__(student, section, *args, **kwargs)
        self.status = status
        self.applicationDate = applicationDate
        
    def save(self, *args, **kwargs):
        # Unique Constraint checker: {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
        # Generates a string for the enrollment_unique attribute. If the same string appears again, throw a uniqueness constraint violation
        # Student cannot be enrolled in multiple sections within the same year, semester, course, and department
        self.enrollment_unique = (f"{self.student} {self.section.course.department} {self.section.course.courseNumber} {self.section.semester} {self.section.sectionYear}")
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return super().__str__() + "\n\t" + f"Application date: {self.applicationDate}, status: {self.status}"