from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TimeRecord(models.Model):
    clock_in_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id + ", " + self.date)
