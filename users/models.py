from django.db import models
from django.contrib.auth.models import User
from datetime import date
import string
import random

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    email2 = models.EmailField(blank=True, null=True, unique=True)
    hide_email2 = models.BooleanField(default=True)
    last_confirm = models.DateField(default=date(1970, 1, 1))
    is_staff = models.BooleanField(default=False)
    misc_info = models.TextField(default="")

    def __str__(self):
        return self.user.get_full_name()

class StaffToken(models.Model):
    token = models.CharField(max_length=30)

    def generate(self):
        lettersAndDigits = string.ascii_letters + string.digits
        self.token = ''.join((random.choice(lettersAndDigits) for i in range(30)))
        self.save()