from django.db import models

# Create your models here.

class Enterprise(models.Model):
    name = models.CharField(max_length=50, default="")
    field = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=50, default="")
    website = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, default="")
    phone = models.IntegerField()
    leader_name = models.CharField(max_length=50, default="")
    is_partner = models.BooleanField(default=False)

    def __str__(self):
        return self.name
