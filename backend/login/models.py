from django.db import models
from django.utils import timezone
# models.py

class UserStatus(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    status = models.CharField(max_length=3, choices=[('in', 'In'), ('out', 'Out')])
    
    def __str__(self):
        return f"{self.username} | {self.status}"
    class Meta:
        db_table = 'user_status'


class UserLoginLog(models.Model):
    username = models.CharField(max_length=150)
    status = models.CharField(max_length=3, choices=[('in', 'In'), ('out', 'Out')])
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_login_log'


    def __str__(self):
        return f"{self.username} | {self.status} | {self.ip_address} | {self.timestamp}"


from django.db import models

class UserIPLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
