from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=30,null=True)
    type = models.CharField(max_length=15,null=True)

    def _str_(self):
        return self.user.Username



class RecruiterUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=30,null=True)
    company = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=30,null=True)

    def _str_(self):
        return self.user.Username



class Job(models.Model):
    recruiter = models.ForeignKey(RecruiterUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.FloatField(max_length=40)
    image = models.FileField()
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    skills = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    creationdate = models.DateField()

    def _str_(self):
        return self.title





class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    applydate= models.DateField()
    
    

    def _str_(self):
        return self.id

