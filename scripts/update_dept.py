
from Department.models import Departments
from School.models import Schools
'''
This function iterates over all schools and retrieves all departments associated with each school.
Then, it sets the departments for each school using the set() method on the school's departments relation.
This ensures that all departments are correctly associated with their respective schools.
'''
def run():
    for school in Schools.objects.all():
        depts = Departments.objects.filter(school=school)
        school.dept.set(depts)
