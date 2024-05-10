import mongoengine
from mongoengine import *
from Course import Course
from Building import Building
from enum import Enum

class Schedule(Enum):
    MW = 'MW'
    TUTH = 'TuTh'
    MWF = 'MWF'
    F = 'F'
    S = 'S'
    
class Semester(Enum):
    FALL = 'Fall'
    WINTER = 'Winter'
    SPRING = 'Spring'
    SUMMERI = 'Summer I'
    SUMMERII = 'Summer II'

class Section(Document):
    """A subdivision within a course that determines the instructor, session location, date, and time."""
    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)
    sectionNumber = IntField(db_field='section_number', required=True)
    semester = EnumField(Semester, required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = EnumField(Building, required=True)
    room = IntField(db_field='room', min_value=1, max_value=1000, required=True)
    schedule = EnumField(Schedule, required=True)
    # startTime = IntField(db_field='start_time', min_value=800, max_value=1930, required=True)
    startTime = StringField(db_field='start_time', required=True)
    instructor = StringField(db_field='instructor', max_length=50, required=True)
    enrollment = ListField(ReferenceField('Enrollment'), db_field='enrollment')
    
    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course', 'sectionNumber', 'sectionYear', 'semester'], 'name': 'sections_uk_01'},
                {'unique': True, 'fields': ['sectionYear', 'semester', 'startTime', 'building', 'room'], 'name': 'sections_uk_02'},
                {'unique': True, 'fields': ['sectionYear', 'semester', 'schedule', 'startTime', 'instructor'], 'name': 'sections_uk_03'}                
            ]}
    
    def __init__(self, course: Course, sectionNumber: int, sectionYear: int, semester: str, building: Building, room: int, schedule: Schedule, startTime: int, instructor: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course
        self.sectionNumber = sectionNumber
        self.sectionYear = sectionYear
        self.semester = semester
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor
        if self.enrollment is None:
            self.enrollment = []
        
    def __str__(self):
        return f"Section: {self.course.courseNumber}-{self.sectionNumber}\n\tSemester: {self.semester} {self.sectionYear}\n\tBuilding and room: {self.building} {self.room}\n\tSchedule: {self.schedule}, Time: {self.startTime}\n\tInstructor: {self.instructor}"
    
    def enroll_student(self, student):
        for already_enrolled_student in self.enrollment:
            if student.equals(already_enrolled_student):
                return # student is already enrolled, ignore add
        self.enrollment.append(student)

    def remove_student(self, student):
        self.enrollment.remove(student)
