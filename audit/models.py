from django.db import models
from django.contrib.auth.models import User

# Model for a System or Application we are auditing (e.g., "Payroll System", "HR Database")
class System(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # ← ADDED THIS FIELD

    def __str__(self):
        return self.name

# Model to represent a User Profile with additional audit info
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Links to Django's built-in User
    role = models.CharField(max_length=50)  # e.g., Admin, User, Read-Only
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Model to log ALL user access events (Login, Logout, Access Attempt)
class AccessLog(models.Model):
    EVENT_TYPES = (
        ('LOGIN_SUCCESS', 'Successful Login'),
        ('LOGIN_FAIL', 'Failed Login'),
        ('LOGOUT', 'User Logout'),
        ('ACCESS_GRANTED', 'Access Granted to Resource'),
        ('ACCESS_DENIED', 'Access Denied to Resource'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # null=True for failed logins where we don't know the user
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True) # We'll capture this later
    details = models.TextField(blank=True) # e.g., which resource was accessed?

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.event_type}"

# Model to log ALL changes (simulating Change Management)
class ChangeLog(models.Model):
    CHANGE_TYPES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    model_name = models.CharField(max_length=50)  # Which database table was changed?
    record_id = models.IntegerField()  # Which specific record was changed?
    timestamp = models.DateTimeField(auto_now_add=True)
    changeset = models.TextField()  # A description of what changed

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.model_name} - {self.change_type}"