import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Buku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=255, verbose_name='Judul Buku')),
                ('pengarang', models.CharField(max_length=255, verbose_name='Pengarang')),
                ('kategori', models.CharField(choices=[
                    ('Novel', 'Novel'),
                    ('Pendidikan', 'Pendidikan'),
                    ('Sains', 'Sains'),
                    ('Sejarah', 'Sejarah'),
                    ('Biografi', 'Biografi'),
                    ('Fiksi', 'Fiksi'),
                    ('Non-Fiksi', 'Non-Fiksi'),
                    ('Lainnya', 'Lainnya'),
                ], default='Novel', max_length=50, verbose_name='Kategori')),
                ('penerbit', models.CharField(max_length=255, verbose_name='Penerbit')),
                ('tahun_terbit', models.PositiveIntegerField(verbose_name='Tahun Terbit')),
                ('isbn', models.CharField(max_length=50, unique=True, verbose_name='ISBN')),
                ('rak_lokasi', models.CharField(max_length=50, verbose_name='Rak / Lokasi')),
                ('stok', models.PositiveIntegerField(default=0, verbose_name='Stok')),
                ('deskripsi', models.TextField(blank=True, verbose_name='Deskripsi')),
            ],
            options={
                'verbose_name': 'Buku',
                'verbose_name_plural': 'Buku',
                'ordering': ['judul'],
            },
        ),
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, verbose_name='Nama')),
                ('kelas', models.CharField(max_length=50, verbose_name='Kelas')),
                ('nis', models.CharField(max_length=20, unique=True, verbose_name='NIS')),
                ('status', models.CharField(choices=[
                    ('Aktif', 'Aktif'),
                    ('Nonaktif', 'Nonaktif'),
                ], default='Aktif', max_length=20, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'ordering': ['nama'],
            },
        ),
        migrations.CreateModel(
            name='Peminjaman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_pinjam', models.DateField(verbose_name='Tanggal Pinjam')),
                ('tanggal_jatuh_tempo', models.DateField(verbose_name='Tanggal Jatuh Tempo')),
                ('keperluan', models.CharField(choices=[
                    ('Tugas sekolah', 'Tugas sekolah'),
                    ('Bacaan pribadi', 'Bacaan pribadi'),
                    ('Referensi', 'Referensi'),
                    ('Lainnya', 'Lainnya'),
                ], default='Bacaan pribadi', max_length=50, verbose_name='Keperluan')),
                ('catatan', models.TextField(blank=True, verbose_name='Catatan')),
                ('petugas', models.CharField(default='Budi Siregar', max_length=255, verbose_name='Petugas')),
                ('status', models.CharField(choices=[
                    ('Dipinjam', 'Dipinjam'),
                    ('Dikembalikan', 'Dikembalikan'),
                ], default='Dipinjam', max_length=20, verbose_name='Status')),
                ('tanggal_kembali', models.DateField(blank=True, null=True, verbose_name='Tanggal Kembali')),
                ('buku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peminjaman_set', to='perpustakaan.buku', verbose_name='Buku')),
                ('peminjam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peminjaman_set', to='perpustakaan.siswa', verbose_name='Nama Peminjam')),
            ],
            options={
                'verbose_name': 'Peminjaman',
                'verbose_name_plural': 'Peminjaman',
                'ordering': ['-tanggal_pinjam', '-id'],
            },
        ),
    ]
