from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    email2 = models.EmailField(blank=True)
    last_confirm = models.DateField(default=date(1970, 1, 1))
    is_staff = models.BooleanField(default=False)
    misc_info = models.TextField(default="")

    def __str__(self):
        return self.user.get_full_name()