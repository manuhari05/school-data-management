from django.db import models


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

class Schools(models.Model):
    scid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)

    # Attech the custom manager to the model
    objects=models.Manager() # default manager
    active= ActiveManager()  # Custom manager for active products

    # Many to many relationship with Departments
    dept=models.ManyToManyField('Department.Departments', related_name='schools', blank=True)

    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.scid)+" " +self.name