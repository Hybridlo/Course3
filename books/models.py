from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author, related_name="Books")
    publisher = models.CharField(max_length=500)
    isbn = models.CharField(max_length=20)

    def __str__(self):
        return self.title