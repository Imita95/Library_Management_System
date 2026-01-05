from django.urls import path
from . import views

app_name = 'library_app'

urlpatterns = [
    path('', views.home, name='home'),

    # Authors
    path('authors/', views.author_list, name='author_list'),
    path('authors/add/', views.author_add, name='author_add'),
    path('authors/edit/<int:id>/', views.author_edit, name='author_edit'),
    path('authors/delete/<int:id>/', views.author_delete, name='author_delete'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/edit/<int:id>/', views.book_edit, name='book_edit'),
    path('books/delete/<int:id>/', views.book_delete, name='book_delete'),
]
