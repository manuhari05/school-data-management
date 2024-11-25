from Department.models import Departments
from Teacher.models import Teachers
from Student.models import Students

def run():
    for dept in Departments.objects.all():

        # Update student's school where their dept matches
        Students.objects.filter(dept=dept.deptid).update(school=dept.school) 