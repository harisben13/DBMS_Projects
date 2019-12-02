from django.db import models

# Create your models here.
class Destination(models.Model):
    department_id=models.IntegerField()
    department_name=models.CharField(max_length=255)
