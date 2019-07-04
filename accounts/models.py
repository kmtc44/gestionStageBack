from random import choices

from django.contrib.auth.models import User
from django.db import models

from internship.models import Enterprise

# Create your models here.

DEPARTMENT = (
    ('GIT', 'Genie Informatique et Telecommunication'),
    ('GEM', 'Genie ElectroMecanique '),
    ('GC', 'Genie Civil'),
)

CLASSES = (
    ('TC2', 'Tronc Commun 2'),
    ('DIC1', 'Diplome d\'Ingenieur de Conception 1'),
    ('DIC2', 'Diplome d\'Ingenieur de Conception 2'),
    ('DIC3', 'Diplome d\'Ingenieur de Conception 3')
)


class Promotion(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return "Promotion n-" + str(self.id)


class Department(models.Model):
    name = models.CharField(max_length=50, choices=DEPARTMENT, default="")

    def __str__(self):
        return "departement : " + str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='profiles/', null=True)
    last_name = models.CharField(max_length=50, default="")
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name="students")
    phone = models.IntegerField(default=0)
    department = models.CharField(max_length=50, choices=DEPARTMENT)
    classe = models.CharField(max_length=50, choices=CLASSES)
    status = models.CharField(max_length=50, default="student")
    enterprise = models.ForeignKey(
        Enterprise, related_name="students", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.status + " : =>  " + self.first_name + " " + self.last_name + " " + self.classe


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='profiles/', null=True)
    phone = models.IntegerField(default=0)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, default=1)
    responsible_dept = models.BooleanField(default=False)
    responsible = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="teacher")

    def __str__(self):
        return self.status + " : =>  " + self.first_name + " " + self.last_name


class Framer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='profiles/', null=True)
    last_name = models.CharField(max_length=50, default="")
    phone = models.IntegerField()
    enterprise = models.ForeignKey(
        Enterprise, related_name="framers", on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=50, default="framer")

    def __str__(self):
        return self.status + " : =>  " + self.first_name + " " + self.last_name
