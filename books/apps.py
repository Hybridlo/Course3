from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self):
        from schedules import cleanReservAndUsers
        cleanReservAndUsers.start()