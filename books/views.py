from django.shortcuts import render
from .models import Book

def index(request):
    rand_books = Book.objects.all().order_by("?")[:5]
    print(rand_books[0].authors.all())
    return render(request, 'books/index.html', {'books': rand_books})