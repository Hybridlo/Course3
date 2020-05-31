from django.shortcuts import render, redirect
from .models import Book, Reservation, Taking
from haystack.views import SearchView
from haystack.forms import SearchForm
from .forms import BookForm, BookFileForm
from django.conf import settings

def index(request):
    if (request.GET.get("q", None) != None):
        return SearchView(template="books/index.html")(request)

    rand_books = Book.objects.all().order_by("?")[:5]
    return render(request, 'books/index.html', {'books': rand_books, 'form': SearchForm()})

def book_view(request, id):
    book = Book.objects.get(pk=id)
    reserved = False

    if request.user.is_authenticated and request.user.info.is_staff:
        if request.method == 'POST':
            success = False

            reserv_id = request.POST.get('reserv_id', None)
            taken_id = request.POST.get('taken_id', None)
            form = form = BookForm(initial={
                'title': book.title,
                'authors': book.authors,
                'publisher': book.publisher,
                'isbn': book.isbn,
                'tags': book.tags,
                'description': book.description,
            })
            if reserv_id != None:
                reservation = Reservation.objects.get(pk=reserv_id)
                taking = Taking()
                taking.taken_by = reservation.reserved_by
                taking.book = reservation.book
                taking.save()
                reservation.delete()
                success = True
            
            elif taken_id != None:
                taking = Taking.objects.get(pk=taken_id)
                taking.book.copies_available += 1
                taking.book.save()
                taking.delete()
                success = True

            else:
                form = BookForm(request.POST)
                if form.is_valid():
                    book.title = form.cleaned_data['title']
                    book.authors = form.cleaned_data['authors']
                    book.publisher = form.cleaned_data['publisher']
                    book.isbn = form.cleaned_data['isbn']
                    book.tags = form.cleaned_data['tags']
                    book.description = form.cleaned_data['description']
                    book.save()
                    success = True
            return render(request, 'books/bookedit.html', {'form': form, 'book': book, 'success': success})
        else:
            form = BookForm(initial={
                'title': book.title,
                'authors': book.authors,
                'publisher': book.publisher,
                'isbn': book.isbn,
                'tags': book.tags,
                'description': book.description,
            })
            return render(request, 'books/bookedit.html', {'form': form, 'book': book})

    elif request.user.is_authenticated:
        reserved = (book in request.user.info.books_reserved.all() or book in request.user.info.books_taken.all())
        if request.method == 'POST':
            success = False
            if (not reserved and 
                    book.copies_available > 0 and
                    request.user.info.books_reserved.count() < settings.MAX_ALLOWED_RESERVTIONS and
                    request.user.info.books_reserved.count() + request.user.info.books_taken.count() < settings.MAX_ALLOWED_TAKEN):
                reservation = Reservation()
                reservation.reserved_by = request.user.info
                reservation.book = book
                reservation.save()
                book.copies_available -= 1
                book.save()
                success = True
            return render(request, 'books/book.html', {'book': book, 'success': success, 'is_auth': request.user.is_authenticated})

    return render(request, 'books/book.html', {'book': book, 'is_auth': request.user.is_authenticated})

def book_digital(request, id):
    if not request.user.is_authenticated or not request.user.info.is_staff:
        return redirect('index')

    book = Book.objects.get(pk=id)

    success = None

    if request.method == 'POST':
        success = False
        form = BookFileForm(request.POST, request.FILES)
        if form.is_valid():
            success = True
            book.digital = form.cleaned_data['digital']
            print(request.FILES)
            book.save()
    else:
        form = BookFileForm()

    return render(request, 'books/upload_book.html', {'form': form, 'success': success})

def reservations(request):
    if not request.user.is_authenticated:
        return render(request, 'books/loginToSee.html', {})

    success = None

    if not request.user.info.is_staff:
        if request.method == 'POST':
            reserv_id = int(request.POST.get('reserv_id'))
            reservation = Reservation.objects.get(pk=reserv_id)
            reservation.book.copies_available += 1
            reservation.book.save()
            reservation.delete()
            success = True

        reservations = request.user.info.books_reserved.all()

        return render(request, 'books/reservations.html', {'reservations' : reservations, 'success': success})
    
    if request.user.info.is_staff:
        if request.method == 'POST':
            reserv_id = int(request.POST.get('reserv_id'))
            reservation = Reservation.objects.get(pk=reserv_id)
            taking = Taking()
            taking.taken_by = reservation.reserved_by
            taking.book = reservation.book
            taking.save()
            reservation.delete()
            success = True

        reservations = Reservation.objects.all()
        
        return render(request, 'books/allReservations.html', {'reservations' : reservations, 'success': success})

def takings(request):
    if not request.user.is_authenticated:
        return render(request, 'books/loginToSee.html', {})

    if not request.user.info.is_staff:
        takings = request.user.info.books_taken.all()

        return render(request, 'books/takings.html', {'takings': takings})

    success = None
    
    if request.user.info.is_staff:
        if request.method == 'POST':
            taken_id = int(request.POST.get('taken_id'))
            taking = Taking.objects.get(pk=taken_id)
            taking.book.copies_available += 1
            taking.book.save()
            taking.delete()
            success = True

        takings = Taking.objects.all()
        
        return render(request, 'books/allTakings.html', {'takings' : takings, 'success': success})

def new_book(request):
    if not request.user.is_authenticated or not request.user.info.is_staff:
        return redirect('index')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()

            return redirect('book', id=book.pk)

    else:
        form = BookForm()
        
    return render(request, 'books/new_book.html', {'form': form})