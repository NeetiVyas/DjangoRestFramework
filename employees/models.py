from django.db import models


class Employee(models.Model):
    emp_id = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=40)
    designation = models.CharField(max_length=40)

    def __str__(self):
        return self.emp_name