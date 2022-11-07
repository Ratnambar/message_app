from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.


class MessageModel(models.Model):
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')