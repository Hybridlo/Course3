from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:id>/', views.book_view, name='book'),
    path('book/<int:id>/add_digital/', views.book_digital, name='book_digital'),
    path('reservations/', views.reservations, name='reservations'),
    path('takings/', views.takings, name='takings'),
    path('new_book/', views.new_book, name='new_book'),
]