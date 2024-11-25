from Teacher.models import Teachers
from Department.models import Departments


def run():
    departments=list(Departments.objects.values_list('name',flat=True).distinct())

    #depts=Departments.objects.all()
    
    print(departments)
    print('\n')
    teacher=Teachers.objects.all()
    for i in teacher:
        print(i.dept)

        
        dept = i.dept.name.strip()
        if dept in departments:
            Departments.objects.filter(name=dept).update(hod=i)
            departments.remove(dept)
            print(departments)
            print(f"Updated HOD for {dept} to {i}")

    print("Remaining Departments:", departments)
            

             
    