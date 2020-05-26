from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:id>/', views.book_view, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    path('takings/', views.takings, name='takings'),
]