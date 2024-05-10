from mongoengine import *
from Student import Student
from Section import Section

class Enrollment(Document):
    """The process of registering a student within a section in order for the student to participate in course activities."""
    student = ReferenceField(Student, required=True)
    section = ReferenceField(Section, required=True)
    enrollment_unique = StringField(unique=True) # ensures student is not enrolled in the same semester, section year
    
    meta = {'allow_inheritance': True,
            'collection': 'enrollment',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollment_uk_01'}
                ]}
    
    def __init__(self, student: Student, section: Section, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.section = section
        
    def save(self, *args, **kwargs):
        # Unique Constraint checker: {semester, sectionYear, departmentAbbreviation, courseNumber, studentID}
        self.enrollment_unique = (f"{self.section.semester} {self.section.sectionYear} {self.section.course.department.abbreviation} {self.section.course.courseNumber} {self.student.lastName} {self.student.firstName}")
        
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.student}\n\tSection: {self.section.course.courseNumber}-{self.section.sectionNumber}, {self.section.semester} {self.section.sectionYear}"

    def get_student(self):
        return self.student
    
    def equals(self, other) -> bool:
        return (self.get_student().lastName == other.get_student().lastName and self.get_student().firstName == other.get_student().firstName) 