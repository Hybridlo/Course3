from django.shortcuts import render
from .models import Book
from haystack.views import SearchView
from haystack.forms import SearchForm

def index(request):
    if (request.GET.get("q", None) != None):
        return SearchView(template="books/index.html")(request)

    rand_books = Book.objects.all().order_by("?")[:5]
    return render(request, 'books/index.html', {'books': rand_books, 'query': None, 'form': SearchForm()})