from mongoengine import *
from Enrollment import Enrollment
from Student import Student
from Section import Section
from enum import Enum

class MinSatisfactory(Enum):
    A = 'A'
    B = 'B'
    C = 'C'

class LetterGrade(Enrollment):
    minSatisfactory = EnumField(MinSatisfactory, required=True)
    
    def __init__(self, student: Student, section: Section, minSatisfactory: MinSatisfactory, *args, **kwargs):
        super().__init__(student, section, *args, **kwargs)
        self.minSatisfactory = minSatisfactory
        
    def save(self, *args, **kwargs):
        # Unique Constraint checker: {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
        self.enrollment_unique = (f"{self.student} {self.section.course.department} {self.section.course.courseNumber} {self.section.semester} {self.section.sectionYear}")
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return super().__str__() + "\n\t" + f"Minimum satisfactory grade: {self.minSatisfactory}"