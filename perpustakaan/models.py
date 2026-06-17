from django.db import models
from django.urls import reverse


class Buku(models.Model):
    KATEGORI_CHOICES = [
        ('Novel', 'Novel'),
        ('Pendidikan', 'Pendidikan'),
        ('Sains', 'Sains'),
        ('Sejarah', 'Sejarah'),
        ('Biografi', 'Biografi'),
        ('Fiksi', 'Fiksi'),
        ('Non-Fiksi', 'Non-Fiksi'),
        ('Lainnya', 'Lainnya'),
    ]

    judul = models.CharField('Judul Buku', max_length=255)
    pengarang = models.CharField('Pengarang', max_length=255)
    kategori = models.CharField('Kategori', max_length=50, choices=KATEGORI_CHOICES, default='Novel')
    penerbit = models.CharField('Penerbit', max_length=255)
    tahun_terbit = models.PositiveIntegerField('Tahun Terbit')
    isbn = models.CharField('ISBN', max_length=50, unique=True)
    rak_lokasi = models.CharField('Rak / Lokasi', max_length=50)
    stok = models.PositiveIntegerField('Stok', default=0)
    deskripsi = models.TextField('Deskripsi', blank=True)

    class Meta:
        ordering = ['judul']
        verbose_name = 'Buku'
        verbose_name_plural = 'Buku'

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('buku_detail', args=[self.pk])


class Siswa(models.Model):
    STATUS_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif'),
    ]

    nama = models.CharField('Nama', max_length=255)
    kelas = models.CharField('Kelas', max_length=50)
    nis = models.CharField('NIS', max_length=20, unique=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='Aktif')

    class Meta:
        ordering = ['nama']
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.pk])

    @property
    def total_peminjaman(self):
        return self.peminjaman_set.count()

    @property
    def jumlah_peminjaman_aktif(self):
        return self.peminjaman_set.filter(status='Dipinjam').count()


class Peminjaman(models.Model):
    KEPERLUAN_CHOICES = [
        ('Tugas sekolah', 'Tugas sekolah'),
        ('Bacaan pribadi', 'Bacaan pribadi'),
        ('Referensi', 'Referensi'),
        ('Lainnya', 'Lainnya'),
    ]
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    ]

    peminjam = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='peminjaman_set', verbose_name='Nama Peminjam')
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE, related_name='peminjaman_set', verbose_name='Buku')
    tanggal_pinjam = models.DateField('Tanggal Pinjam')
    tanggal_jatuh_tempo = models.DateField('Tanggal Jatuh Tempo')
    keperluan = models.CharField('Keperluan', max_length=50, choices=KEPERLUAN_CHOICES, default='Bacaan pribadi')
    catatan = models.TextField('Catatan', blank=True)
    petugas = models.CharField('Petugas', max_length=255, default='Budi Siregar')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='Dipinjam')
    tanggal_kembali = models.DateField('Tanggal Kembali', null=True, blank=True)

    class Meta:
        ordering = ['-tanggal_pinjam', '-id']
        verbose_name = 'Peminjaman'
        verbose_name_plural = 'Peminjaman'

    def __str__(self):
        return f'{self.peminjam.nama} - {self.buku.judul}'
