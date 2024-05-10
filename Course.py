import mongoengine
from mongoengine import *
from Department import Department

class Course(Document):
    """A structured unit in a department that specializes in teaching a specific subject."""
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    courseName = StringField(db_field='course_name', max_length=50, required=True)
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    units = IntField(db_field='units', min_value=1, max_value=5, required=True)
    sections = ListField(ReferenceField('Section'), db_field='sections')
    
    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department', 'courseName'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['department', 'courseNumber'], 'name': 'courses_uk_02'}
            ]}
    
    def __init__(self, department: Department, courseName: str, courseNumber: int, description: str, units: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.courseName = courseName
        self.courseNumber = courseNumber
        self.description = description
        self.units = units
        if self.sections is None:
            self.sections = []
        
    def __str__(self):
        results = f"Department: {self.department.abbreviation} {self.courseNumber} {self.courseName}\n\t{self.description}\n\tUnits: {self.units}"
        for section in self.sections:
            results = results + '\n\t' + f'Section: {self.courseNumber}-{section.sectionNumber}, {section.semester} {section.sectionYear}'
        return results
    
    def add_item(self, item):
        self.sections.append(item)

    def remove_section(self, item):
        self.sections.remove(item)