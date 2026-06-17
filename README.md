# SIPUSTAKA — Sistem Peminjaman Buku

Aplikasi web untuk mengelola peminjaman buku perpustakaan sekolah, dibangun dengan Django.
Mencakup empat modul: **Dashboard**, **Buku**, **Peminjaman**, dan **User** (data siswa peminjam),
sesuai desain yang diberikan.

## Fitur

- **Dashboard** — ringkasan total buku, total judul, jumlah yang sedang dipinjam/sudah dikembalikan,
  grafik distribusi stok per judul, dan ringkasan transaksi.
- **Buku** — CRUD lengkap (tambah, lihat detail, edit, hapus) untuk data buku: judul, pengarang,
  kategori, penerbit, tahun terbit, ISBN, rak/lokasi, stok, dan deskripsi.
- **Peminjaman** — mencatat transaksi peminjaman (memilih peminjam & buku, tanggal pinjam/jatuh
  tempo, keperluan, petugas, catatan) serta tombol "Kembalikan" untuk menutup transaksi. Stok buku
  otomatis berkurang saat dipinjam dan bertambah saat dikembalikan.
- **User** — CRUD data siswa yang berhak meminjam buku (nama, kelas, NIS, status aktif/nonaktif),
  beserta riwayat total peminjaman dan peminjaman yang masih aktif.

Data contoh (3 buku, 4 siswa, 2 transaksi peminjaman) sudah disiapkan lewat migration, sehingga
begitu dijalankan tampilannya langsung terisi seperti pada desain.

## Cara Menjalankan

Pastikan Python 3.10+ sudah terpasang di komputer Anda, lalu jalankan:

```bash
# 1. Masuk ke folder proyek
cd sipustaka

# 2. (Opsional tapi disarankan) buat virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan migration (membuat database + data contoh)
python manage.py migrate

# 5. (Opsional) buat akun admin Django untuk mengakses /admin/
python manage.py createsuperuser

# 6. Jalankan server
python manage.py runserver
```

Lalu buka **http://127.0.0.1:8000/** di browser.

Halaman Django Admin (untuk kelola data lewat antarmuka bawaan Django) tersedia di
**http://127.0.0.1:8000/admin/**.

## Struktur Proyek

```
sipustaka/
├── manage.py
├── requirements.txt
├── sipustaka/              # konfigurasi proyek (settings, urls utama)
└── perpustakaan/           # app utama
    ├── models.py           # Buku, Siswa, Peminjaman
    ├── forms.py            # ModelForm untuk tiap entitas
    ├── views.py            # logic dashboard & CRUD
    ├── urls.py             # routing /buku/, /peminjaman/, /user/, dst.
    ├── admin.py             # registrasi ke Django Admin
    ├── migrations/          # termasuk migration data contoh (0002_seed_data.py)
    ├── templates/perpustakaan/   # semua halaman HTML
    └── static/perpustakaan/css/style.css  # styling sesuai desain
```

## Catatan

- Nama "Admin Aktif" pada sidebar (Budi Siregar) bersifat statis dan diatur lewat
  `ADMIN_AKTIF_NAMA` di `sipustaka/settings.py`, karena desain belum menyertakan halaman login.
  Jika ingin menambahkan sistem login sungguhan, beri tahu saya dan ini bisa ditambahkan
  menggunakan `django.contrib.auth`.
- Field "Kategori" pada Buku dan "Keperluan" pada Peminjaman memakai pilihan (dropdown) yang bisa
  disesuaikan langsung di `perpustakaan/models.py` (cari `KATEGORI_CHOICES` / `KEPERLUAN_CHOICES`).
- `DEBUG = True` dan `SECRET_KEY` di `settings.py` hanya untuk pengembangan lokal — jangan
  dipakai langsung untuk deployment produksi.
# SKL-PERPUSTAKAAN
