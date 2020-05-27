import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
import django
django.setup()

from books.models import Book

def add_book(d):
    book = Book()
    book.title = d.get('title')
    book.authors = d.get('authors')
    book.publisher = d.get('publisher', "")
    book.isbn = d.get('isbn', "")
    book.tags = d.get('tags', "")
    book.description = d.get('description', "")
    book.copies_available = int(d.get('copies_available', 1))
    book.save()