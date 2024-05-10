import mongoengine
from mongoengine import *
from Department import Department

class Major(Document):
    """A primary focus or specialization offered by the department, which grants a degree or diploma upon completion of the necessary course work."""
    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    name = StringField(db_field='name', max_length=50, required=True)
    description = StringField(db_field='description', max_length=80, required=True)
    students = ListField(ReferenceField('StudentMajor'), db_field='students')
    
    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'}
            ]}

    def __init__(self, department: Department, name: str, description: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.name = name
        self.description = description
        if self.students is None:
            self.students = []
        
    def __str__(self):
        return f"Major: {self.department.name} - {self.name}\n\t{self.description}"
    
    def declare_student(self, student):
        self.students.append(student)

    def remove_student(self, student):
        self.students.remove(student)