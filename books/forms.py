from django.forms import ModelForm
from .views import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'publisher', 'isbn', 'tags', 'description', 'copies_available']
        labels = {
            'title': 'Назва',
            'authors': 'Автори',
            'publisher': 'Видавництво',
            'isbn': 'ISBN',
            'tags': 'Ключові слова',
            'description': 'Опис',
            'copies_available': 'Доступно екземплярів',
        }