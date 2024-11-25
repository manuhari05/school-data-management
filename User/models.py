from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import models
from .utils import generate_random_password 

class UsersManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Users(AbstractBaseUser):
    # id = models.AutoField(primary_key=True)
    empid = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    # original_password=models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=True)
    performance = models.IntegerField(null=True, blank=True)
    deptid = models.IntegerField(null=True, blank=True)
    schoolid = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True)
    last_password_update = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UsersManager()

    def save(self, *args, **kwargs):
        """Ensure the password meets required criteria before saving."""
        
        if not self.password:
            self.password = generate_random_password()
            print(self.username,self.password)  # Generate a random password if not set
            self.validate_password(self.password)
            self.password=make_password(self.password)  # Store the hashed password

        super().save(*args, **kwargs)  # Save the model instance

    def validate_password(self, password):
        """Ensure the password meets required criteria."""
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not self.contains_uppercase(password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not self.contains_lowercase(password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not self.contains_digit(password):
            raise ValidationError('Password must contain at least one number.')
        if not self.contains_special_character(password):
            raise ValidationError('Password must contain at least one special character.')

    def contains_uppercase(self, password):
        return any(char.isupper() for char in password)

    def contains_lowercase(self, password):
        return any(char.islower() for char in password)

    def contains_digit(self, password):
        return any(char.isdigit() for char in password)

    def contains_special_character(self, password):
        special_characters = '!@#$%^&*(),.?":{}|<>'
        return any(char in special_characters for char in password)
