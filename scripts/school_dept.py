from Department.models import Departments
from Teacher.models import Teachers

def run():
    for teacher in Teachers.objects.all():
        dept=teacher.dept
        if dept:
            if teacher.empid==dept.hod.empid:
                teacher.hod= True
            
            teacher.school=dept.school
            teacher.save()

        