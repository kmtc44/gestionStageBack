from django.contrib import admin
from .models import Student, Framer, Teacher, Task

# Register your models here.
admin.site.register(Student)
admin.site.register(Framer)
admin.site.register(Teacher)
admin.site.register(Task)
