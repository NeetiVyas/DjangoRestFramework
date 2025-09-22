from django.db import models
from django.utils import timezone


class Customer(models.Model):
    time_raised = models.DateTimeField(default=timezone.now(), editable=False)
    name = models.CharField(max_length=20)
    age = models.IntegerField()

