from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('buku/', views.buku_list, name='buku_list'),
    path('buku/tambah/', views.buku_create, name='buku_create'),
    path('buku/<int:pk>/', views.buku_detail, name='buku_detail'),
    path('buku/<int:pk>/edit/', views.buku_update, name='buku_update'),
    path('buku/<int:pk>/hapus/', views.buku_delete, name='buku_delete'),

    path('peminjaman/', views.peminjaman_list, name='peminjaman_list'),
    path('peminjaman/pinjam/', views.peminjaman_create, name='peminjaman_create'),
    path('peminjaman/<int:pk>/kembalikan/', views.peminjaman_kembalikan, name='peminjaman_kembalikan'),

    path('user/', views.user_list, name='user_list'),
    path('user/tambah/', views.user_create, name='user_create'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('user/<int:pk>/edit/', views.user_update, name='user_update'),
    path('user/<int:pk>/hapus/', views.user_delete, name='user_delete'),
]
