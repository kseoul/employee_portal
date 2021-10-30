from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# Overriding the Default Django Auth User and adding One More Field (user_type)

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Supervisor"), (3, "Employee"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Teams(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return f'{self.team_name}'

class Supervisors(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    team_id = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True) #need to give default team
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    team_id = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True) #need to give default team
    profile_pic = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportEmployees(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    start_date = models.DateField(max_length=255)
    end_date = models.DateField(max_length=255)
    hours_calc = models.IntegerField(default=0)
    leave_date = models.DateField(max_length=255, blank=True, null=True)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    supervisor_id = models.ForeignKey(Supervisors,on_delete=models.CASCADE, blank=True, null=True)
    kronos_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveApprovalEmployees(models.Model):
    approval_id = models.OneToOneField(LeaveReportEmployees, primary_key=True, on_delete=models.CASCADE)
    supervisor_id = models.ForeignKey(Supervisors, on_delete=models.CASCADE,blank=True,null=True)
    approval_date = models.DateTimeField(null=True,blank=True)
    objects = models.Manager()

class FeedBackEmployees(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class FeedBackSupervisors(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_id = models.ForeignKey(Supervisors, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationEmployees(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationSupervisors(models.Model):
    id = models.AutoField(primary_key=True)
    supervisor_id = models.ForeignKey(Supervisors, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Supervisors.objects.create(admin=instance, team_id=Teams.objects.get(id=1))
        if instance.user_type == 3:
            Employees.objects.create(admin=instance, profile_pic="", team_id=Teams.objects.get(id=1))
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.supervisors.save()
    if instance.user_type == 3:
        instance.employees.save()

@receiver(post_save,sender=LeaveReportEmployees)
def post_vacation_created_signal(sender, instance, created, **kwargs):
    print(instance.employee_id.id)
    if created:
        LeaveApprovalEmployees.objects.create(supervisor_id=instance.supervisor_id,approval_date=None)
