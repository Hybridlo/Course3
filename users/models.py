from django.db import models
from django.contrib.auth.models import User
from datetime import date
from books.models import Book

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    email2 = models.EmailField(blank=True)
    last_confirm = models.DateField(default=date(1970, 1, 1))
    misc_info = models.TextField(default="")

    def __str__(self):
        return self.user.get_full_name()

class Taking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    taken_by = models.ForeignKey(UserInfo, related_name='books_taken', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_by = models.ForeignKey(UserInfo, related_name='books_reserved', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)