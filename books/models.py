from django.db import models
from users.models import UserInfo

class Book(models.Model):
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=1000, default="")
    publisher = models.CharField(max_length=500, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=1000, default="", blank=True)
    description = models.TextField(default="", blank=True)
    copies_available = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Taking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='takings')
    taken_by = models.ForeignKey(UserInfo, related_name='books_taken', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reserved_by = models.ForeignKey(UserInfo, related_name='books_reserved', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)