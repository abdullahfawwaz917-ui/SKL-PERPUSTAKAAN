from django.contrib import admin

from .models import Buku, Siswa, Peminjaman


@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('judul', 'pengarang', 'kategori', 'penerbit', 'tahun_terbit', 'rak_lokasi', 'stok')
    search_fields = ('judul', 'pengarang', 'isbn')
    list_filter = ('kategori',)


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kelas', 'nis', 'status')
    search_fields = ('nama', 'nis')
    list_filter = ('status', 'kelas')


@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('peminjam', 'buku', 'tanggal_pinjam', 'tanggal_jatuh_tempo', 'status', 'petugas')
    list_filter = ('status', 'keperluan')
    search_fields = ('peminjam__nama', 'buku__judul')
