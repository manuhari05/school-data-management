from django.db import models


# from Teacher.models import Teachers
# from School.models import Schools


class ActiveManager(models.Manager):
    def  get_queryset(self):
        return super().get_queryset()
    
    def get_active(self):
        return self.get_queryset().filter(is_active=True)
    
    def get_inactive(self):
        return self.get_queryset().filter(is_active=False)
    
    def active_count(self):
        return self.get_active().count()
    
# Create your models here.
class Departments(models.Model):
    deptid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    # hod=models.ForeignKey('Teacher.Teachers',on_delete=models.DO_NOTHING,null=True,blank=True)
    # school=models.ForeignKey('School.Schools', on_delete=models.DO_NOTHING, null=True, blank=True,related_name='departments')
    is_active=models.BooleanField(default=True)

    # Attech the custom manager to the model
    objects=models.Manager() # default manager
    active= ActiveManager()  # Custom manager for active products


    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
