from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self):
        print('started')
        from schedules import cleanReservations
        cleanReservations.start()