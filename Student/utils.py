# from Teacher.models import Teachers
# from Student.models import Students
from . import models
from Teacher.models import Teachers

'''This utils.py file contains the functions of few logics which 
    used in this project'''


'''
this variable is used to store the passing marks
of a student in the examination
'''
passing_marks=18


'''
this function is used to calculate the passing percentage
of a student based on the given criteria
'''
cut_off_percentage = 35
total_subjects = 3
max_marks_per_subject = 50

def calculate_passing_percentage():
    return round((cut_off_percentage/100)*(total_subjects*max_marks_per_subject),2)




'''
this function is used to calculate the passing percentage
'''

def update_teacher_performance(teacher):
    students = models.Students.objects.filter(teacher_id=teacher)
    total_students = students.count()
    passed_students = students.filter(result=True).count()
    passing_percentage = (passed_students / total_students * 100) if total_students > 0 else 0
    print(passing_percentage)
    
    # Update the teacher's passing percentage
    Teachers.objects.filter(empid=teacher).update(perfomance = passing_percentage)
