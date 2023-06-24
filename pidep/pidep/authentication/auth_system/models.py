from django.db import models
from django.contrib.auth.models import User

class UserRole(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('student', 'Student')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=USER_ROLES, max_length=10)
