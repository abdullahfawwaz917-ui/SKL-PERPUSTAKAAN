from django.db import migrations


def seed_data(apps, schema_editor):
    Buku = apps.get_model('perpustakaan', 'Buku')
    Siswa = apps.get_model('perpustakaan', 'Siswa')
    Peminjaman = apps.get_model('perpustakaan', 'Peminjaman')

    laskar_pelangi = Buku.objects.create(
        judul='Laskar Pelangi',
        pengarang='Andrea Hirata',
        kategori='Novel',
        penerbit='Bentang Pustaka',
        tahun_terbit=2005,
        isbn='978-979-3062-79-2',
        rak_lokasi='Rak A-01',
        stok=5,
        deskripsi='Novel tentang perjuangan anak-anak Belitung mengejar pendidikan.',
    )
    bumi = Buku.objects.create(
        judul='Bumi',
        pengarang='Tere Liye',
        kategori='Novel',
        penerbit='Gramedia Pustaka Utama',
        tahun_terbit=2014,
        isbn='978-602-03-0998-1',
        rak_lokasi='Rak A-02',
        stok=7,
        deskripsi='Kisah petualangan fantasi Raib, Seli, dan Ali di dunia paralel.',
    )
    Buku.objects.create(
        judul='Negeri 5 Menara',
        pengarang='A. Fuadi',
        kategori='Novel',
        penerbit='Gramedia Pustaka Utama',
        tahun_terbit=2009,
        isbn='978-979-22-4861-6',
        rak_lokasi='Rak A-03',
        stok=2,
        deskripsi='Kisah enam santri yang mengejar mimpi mereka dari Pondok Madani.',
    )

    roni = Siswa.objects.create(nama='Roni', kelas='XI IPA 1', nis='2026001', status='Aktif')
    sinta = Siswa.objects.create(nama='Sinta', kelas='XI IPS 2', nis='2026002', status='Aktif')
    Siswa.objects.create(nama='Dewi Anggraini', kelas='X IPA 3', nis='2026003', status='Aktif')
    Siswa.objects.create(nama='Bima Pratama', kelas='XII IPS 1', nis='2026004', status='Aktif')

    Peminjaman.objects.create(
        peminjam=roni,
        buku=laskar_pelangi,
        tanggal_pinjam='2026-06-01',
        tanggal_jatuh_tempo='2026-06-08',
        keperluan='Tugas sekolah',
        catatan='Referensi tugas Bahasa Indonesia.',
        petugas='Budi Siregar',
        status='Dipinjam',
    )
    Peminjaman.objects.create(
        peminjam=sinta,
        buku=bumi,
        tanggal_pinjam='2026-06-02',
        tanggal_jatuh_tempo='2026-06-09',
        keperluan='Bacaan pribadi',
        catatan='',
        petugas='Budi Siregar',
        status='Dipinjam',
    )


def remove_seed_data(apps, schema_editor):
    Buku = apps.get_model('perpustakaan', 'Buku')
    Siswa = apps.get_model('perpustakaan', 'Siswa')
    Buku.objects.all().delete()
    Siswa.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('perpustakaan', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_seed_data),
    ]
