from django import forms
from .views import Book

class BookForm(forms.ModelForm):
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

class BookFileForm(forms.Form):
    digital = forms.FileField(label="Електроний екземпляр")