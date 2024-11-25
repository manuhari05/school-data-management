from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from Teacher.models import Teachers
# from Department.models import Departments

from .utils import passing_marks ,update_teacher_performance

class ActiveManager(models.Manager):
    # def  get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)
    
    def  get_queryset(self):
        return super().get_queryset()
    
    def get_active(self):
        return self.get_queryset().filter(is_active=True)
    
    def get_inactive(self):
        return self.get_queryset().filter(is_active=False)
    
    def active_count(self):
        return self.get_active().count()
    

    

# Create your models here.


class Students(models.Model):
    rollno=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    dept=models.ForeignKey('Department.Departments',on_delete=models.DO_NOTHING,null=True,blank=True,related_name="dept_students")
    teacher_id=models.ForeignKey('Teacher.Teachers', on_delete=models.DO_NOTHING, null=True, blank=True,related_name="teacher_students")
    school=models.ForeignKey('School.Schools', on_delete=models.DO_NOTHING, null=True, blank=True, related_name="school_students")
    # phy_marks=models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(50)])
    # che_marks=models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(50)])
    # maths_marks=models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(50)])
    is_active=models.BooleanField(default=True)

    # Attech the custom manager to the model
    objects=models.Manager() # default manager
    active= ActiveManager()  # Custom manager for active products

    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    total_marks=models.FloatField(default=0.0)
    # percentage=models.FloatField(editable=False)
    # phy_pass=models.BooleanField(default=False)
    # che_pass=models.BooleanField(default=False)
    # maths_pass=models.BooleanField(default=False)
    result=models.BooleanField(default=False)

    def save(self,*args,**kwargs):

        if self.teacher_id and self.dept and self.school:
            if self.teacher_id.dept != self.dept or self.teacher_id.school != self.school:
                raise ValidationError("The teacher's department and school must match the student's department and school.")    
                # raise ValidationError("The teacher's department must match the student's department.")



        # self.total_marks=self.phy_marks+self.che_marks+self.maths_marks
        self.percentage=round((self.total_marks/150)*100,2)
        # self.phy_pass=self.phy_marks>=passing_marks
        # self.che_pass=self.che_marks>=passing_marks
        # self.maths_pass=self.maths_marks>=passing_marks
        self.result=self.total_marks >= passing_marks*3

        super(Students, self).save(*args, **kwargs)

        if self.teacher_id:
            update_teacher_performance(self.teacher_id.empid)

    def delete(self,*args,**kwargs):
        teacher=self.teacher_id
        super(Students, self).delete(*args, **kwargs)
        if teacher:
            update_teacher_performance(teacher)


    def __str__(self):
        return self.name


