from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# from Department.models import Departments

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

class Teachers(models.Model):
    empid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    perfomance=models.FloatField(default=0.0)
    
    is_active=models.BooleanField(default=True)

    # Attech the custom manager to the model
    objects=models.Manager() # default manager
    active= ActiveManager()  # Custom manager for active products

    dept=models.ForeignKey('Department.departments',on_delete=models.DO_NOTHING,null=True,blank=True)
    school=models.ForeignKey('School.schools', on_delete=models.DO_NOTHING, null=True, blank=True)
    hod=models.BooleanField(default=False)

    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.name

