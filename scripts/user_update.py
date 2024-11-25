from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from Teacher.models import Teachers
from Department.models import Departments
from School.models import Schools
from User.models import Users
from User.utils import generate_random_password

def run():
    teachers=Teachers.objects.all()

    count=0
    no_created=0

    for teacher in teachers:
        # if count>=1 or no_created>=1:
        #     break

        empid=teacher.empid
        first_name=teacher.name.split(' ')[0]
        
        last_name=teacher.name.split(' ')[1:]
        last_name=' '.join(last_name)

        role='teacher'

        if teacher.hod:
            role='hod'
        
        deptid=teacher.dept.deptid
        schoolid=teacher.school.scid

        is_active=False
        if teacher.is_active==True:
            is_active=True

        performance=teacher.perfomance


        username=teacher.name.lower().replace(' ','_')
        username=username+'_'+str(teacher.empid)
        email=username+'@gmail.com'

        if Users.objects.filter(username=username).exists():
            print(f"Teacher {teacher.name} with username {username} already exists")

            continue


        password=generate_random_password()

        try:
            user=Users(username=username, 
                       email=email, 
                       password=password,
                       empid=empid, 
                       first_name=first_name, 
                       last_name=last_name, 
                       role=role, 
                       deptid=deptid, 
                       schoolid=schoolid, 
                       is_active=is_active,
                       performance=performance )
            user.save()
            count+=1
            print(f"Teacher {teacher.name} with username {username} created with password {password}")

        except IntegrityError as e:
            failed_count += 1
            print(f"Failed to create user for teacher {teacher.name} due to IntegrityError: {e}")
        except ValidationError as e:
            failed_count += 1
            print(f"Validation error for teacher {teacher.name}: {e}")

    print(f"\nProcess completed: {count} users created, {no_created} failed.")

            