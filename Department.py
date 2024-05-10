from mongoengine import *
from Building import Building

class Department(Document):
    """An organizational unit within an academic institution that consists of several courses, and is managed by a chair person."""
    name = StringField(db_field='name', max_length=50, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, required=True)
    building = EnumField(Building, required=True)
    office = IntField(db_field='office', required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    courses = ListField(ReferenceField('Course'), db_field='courses')
    majors = ListField(ReferenceField('Major'), db_field='majors')
    
    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_03'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_04'},
            ]}
    
    def __init__(self, name: str, abbreviation: str, chairName: str, building: Building, office: int, description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description
        if self.courses is None:
            self.courses = []
        if self.majors is None:
            self.majors = []
        
    def __str__(self):
        results = f"Department: {self.abbreviation} - {self.name}\n\tChair name: {self.chairName}, building and office: {self.building} {self.office}\n\t{self.description}"
        for course in self.courses:
            results = results + '\n\t' + f'Course: {course.courseNumber} {course.courseName}'
        return results
            
    def add_course_to_department(self, item):
        self.courses.append(item)
        
    def add_major_to_department(self, item):
        self.majors.append(item)
    
    def remove_course_from_department(self, item):
        self.courses.remove(item)

    def remove_major_from_department(self, item):
        self.majors.remove(item)