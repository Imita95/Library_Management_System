from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Author, Category, Book

def home(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    books = Book.objects.select_related('author').prefetch_related('categories').all()

    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))

    if category_id:
        books = books.filter(categories__id=category_id)

    categories = Category.objects.all()
    context = {
        'books': books.distinct(),
        'categories': categories,
        'q': q,
        'selected_category': category_id
    }
    return render(request, 'home.html', context)



def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})

def author_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        biography = request.POST.get('biography')
        Author.objects.create(name=name, email=email, biography=biography)
        return redirect('library_app:author_list')
    return render(request, 'author_form.html', {'author': None})

def author_edit(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        author.name = request.POST.get('name')
        author.email = request.POST.get('email')
        author.biography = request.POST.get('biography')
        author.save()
        return redirect('library_app:author_list')
    return render(request, 'author_form.html', {'author': author})

def author_delete(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        author.delete()
        return redirect('library_app:author_list')
   
    return render(request, 'author_form.html', {'author': author, 'confirm_delete': True})



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('library_app:category_list')

    return render(request, 'category_form.html', {'category': None})

def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('library_app:category_list')

    return render(request, 'category_form.html', {'category': category})

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.delete()
        return redirect('library_app:category_list')

    return render(request, 'category_form.html', {
        'category': category,
        'confirm_delete': True   
    })




def book_list(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    books = Book.objects.select_related('author').prefetch_related('categories').all()

    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
    if category_id:
        books = books.filter(categories__id=category_id)

    categories = Category.objects.all()
    return render(request, 'book_list.html', {
        'books': books.distinct(),
        'categories': categories,
        'q': q,
        'selected_category': category_id
    })


def book_add(request):
    authors = Author.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        author_id = request.POST.get('author')
        category_ids = request.POST.getlist('categories')
        isbn = request.POST.get('isbn')
        published_date = request.POST.get('published_date') or None
        total_pages = request.POST.get('total_pages') or None
        price = request.POST.get('price') or 0

        book = Book.objects.create(
            title=title,
            description=description,
            author_id=author_id,
            isbn=isbn,
            published_date=published_date if published_date else None,
            total_pages=(int(total_pages) if total_pages else None),
            price=price
        )
        if category_ids:
            book.categories.set(category_ids)
        return redirect('library_app:book_list')

    return render(request, 'book_form.html', {'book': None, 'authors': authors, 'categories': categories})


def book_edit(request, id):
    book = get_object_or_404(Book, id=id)
    authors = Author.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.description = request.POST.get('description')
        book.author_id = request.POST.get('author')
        category_ids = request.POST.getlist('categories')
        book.isbn = request.POST.get('isbn')
        published_date = request.POST.get('published_date') or None
        total_pages = request.POST.get('total_pages') or None
        book.published_date = published_date if published_date else None
        book.total_pages = (int(total_pages) if total_pages else None)
        book.price = request.POST.get('price') or 0
        book.save()
        if category_ids:
            book.categories.set(category_ids)
        else:
            book.categories.clear()
        return redirect('library_app:book_list')

    return render(request, 'book_form.html', {
        'book': book,
        'authors': authors,
        'categories': categories
    })


def book_delete(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('library_app:book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})
