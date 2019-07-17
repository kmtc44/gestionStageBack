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
TASK_STATE = (
    ('Created', 'Created'),
    ('Doing', 'Doing'),
    ('Done', 'Done'),
    ('Reviewing', 'Reviewing'),
    ('Finish', 'Finish')
)

SocialStatus = (
        ('CSE', 'Célibataire sans enfants'),
        ('CAE', 'Célibataire avec enfants'),
        ('MSE', 'Marié(e) sans enfants'),
        ('MAE', 'Marié(e) avec enfants'),
    )

Genre=(
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

class Promotion(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return "Promotion n-" + str(self.id)


class Department(models.Model):
    name = models.CharField(max_length=50, choices=DEPARTMENT, default="")

    def __str__(self):
        return "departement : " + str(self.name)


class Classroom(models.Model):
    name = models.CharField(
        max_length=50, choices=CLASSES, unique=True, default="")

    def __str__(self):
        return "classe de  : " + str(self.name)

class Skill(models.Model):
    name = models.CharField(max_length=50, default="")
    
    def __str__(self):
        return self.name 

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='profiles/', null=True)
    last_name = models.CharField(max_length=50, default="")
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name="students")
    phone = models.IntegerField(default=0)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name='students', null=True)
    status = models.CharField(max_length=50, default="student")
    enterprise = models.ForeignKey(
        Enterprise, related_name="students", on_delete=models.CASCADE, null=True)

    socialStatus = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50, default="")

    skills = models.ManyToManyField(Skill, related_name="students")

    birthday = models.DateField(null=True)


    def __str__(self):
        return self.status + " : =>  " + self.first_name + " " + self.last_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='profiles/', null=True)
    phone = models.IntegerField(default=0)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE)
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


class Project(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=200, default="")
    aim = models.CharField(max_length=300, default="")
    framer = models.ForeignKey(
        Framer, related_name="my_project", on_delete=models.CASCADE, null=False)
    enterprise = models.ForeignKey(
        Enterprise, related_name="projects", on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="projects")
    starting_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.TextField()
    framer = models.ForeignKey(
        Framer, related_name="my_tasks", on_delete=models.CASCADE, null=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, related_name="tasks")
    students = models.ManyToManyField(Student, related_name="my_tasks")
    starting_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    state = models.CharField(max_length=30, choices=TASK_STATE, default="Created")

    def __str__(self):
        return self.title + ":  " + self.description

