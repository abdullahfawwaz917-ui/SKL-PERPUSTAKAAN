from django.contrib import messages
from django.db import connection
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import BukuForm, SiswaForm, PeminjamanForm


# ---------------------------------------------------------------------------
# Helper raw SQL
# ---------------------------------------------------------------------------

def dictfetchall(cursor):
    """Ubah hasil cursor.fetchall() jadi list of dict supaya tetap bisa
    diakses pakai dot-notation di template Django (mis. {{ buku.judul }})."""
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    for row in rows:
        row['pk'] = row.get('id')
    return rows


def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    data = dict(zip(columns, row))
    data['pk'] = data.get('id')
    return data


def raw_get_or_404(table, pk):
    """Pengganti get_object_or_404 versi raw SQL.
    `table` selalu string konstan yang kita tulis sendiri di kode (bukan
    input user), jadi aman dari SQL injection meski ditempel lewat f-string."""
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM {table} WHERE id = %s', [pk])
        row = dictfetchone(cursor)
    if row is None:
        raise Http404(f'Data dengan id={pk} tidak ditemukan di tabel {table}.')
    return row


def raw_insert(table, data: dict):
    if not data:
        return
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
    with connection.cursor() as cursor:
        cursor.execute(sql, list(data.values()))


def raw_update(table, pk, data: dict):
    if not data:
        return
    assignments = ', '.join([f'{col} = %s' for col in data.keys()])
    sql = f'UPDATE {table} SET {assignments} WHERE id = %s'
    with connection.cursor() as cursor:
        cursor.execute(sql, list(data.values()) + [pk])


def raw_delete(table, pk):
    with connection.cursor() as cursor:
        cursor.execute(f'DELETE FROM {table} WHERE id = %s', [pk])


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT COALESCE(SUM(stok), 0) FROM perpustakaan_buku')
        total_buku = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM perpustakaan_buku')
        total_judul = cursor.fetchone()[0]

        cursor.execute(
            'SELECT COUNT(*) FROM perpustakaan_peminjaman WHERE status = %s',
            ['Dipinjam']
        )
        sedang_dipinjam = cursor.fetchone()[0]

        cursor.execute(
            'SELECT COUNT(*) FROM perpustakaan_peminjaman WHERE status = %s',
            ['Dikembalikan']
        )
        sudah_dikembalikan = cursor.fetchone()[0]

        cursor.execute('SELECT * FROM perpustakaan_buku')
        semua_buku = dictfetchall(cursor)

    stok_max = max([b['stok'] for b in semua_buku], default=0) or 1
    distribusi_stok = [
        {'buku': b, 'persen': round(b['stok'] / stok_max * 100)} for b in semua_buku
    ]

    total_transaksi = sedang_dipinjam + sudah_dikembalikan or 1
    persen_dipinjam = round(sedang_dipinjam / total_transaksi * 100)
    persen_dikembalikan = round(sudah_dikembalikan / total_transaksi * 100)

    context = {
        'nama': 'Abdullah fawwaz',
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'distribusi_stok': distribusi_stok,
        'persen_dipinjam': persen_dipinjam,
        'persen_dikembalikan': persen_dikembalikan,
        'active_nav': 'dashboard',
    }
    return render(request, 'perpustakaan/dashboard.html', context)


# ---------------------------------------------------------------------------
# Buku
# ---------------------------------------------------------------------------

def buku_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM perpustakaan_buku ORDER BY id')
        buku_qs = dictfetchall(cursor)
    return render(request, 'perpustakaan/buku_list.html', {
        'buku_list': buku_qs,
        'active_nav': 'buku',
    })


def buku_detail(request, pk):
    buku = raw_get_or_404('perpustakaan_buku', pk)
    return render(request, 'perpustakaan/buku_detail.html', {
        'buku': buku,
        'active_nav': 'buku',
    })


def buku_create(request):
    if request.method == 'POST':
        form = BukuForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            raw_insert('perpustakaan_buku', data)
            messages.success(request, f'Buku "{data["judul"]}" berhasil ditambahkan.')
            return redirect('buku_list')
    else:
        form = BukuForm()
    return render(request, 'perpustakaan/buku_form.html', {
        'form': form,
        'judul_halaman': 'Tambah Buku',
        'label_tombol': 'Simpan Buku',
        'active_nav': 'buku',
    })


def buku_update(request, pk):
    buku = raw_get_or_404('perpustakaan_buku', pk)
    if request.method == 'POST':
        form = BukuForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            raw_update('perpustakaan_buku', pk, data)
            messages.success(request, f'Buku "{data["judul"]}" berhasil diperbarui.')
            return redirect('buku_list')
    else:
        form = BukuForm(initial=buku)
    return render(request, 'perpustakaan/buku_form.html', {
        'form': form,
        'buku': buku,
        'judul_halaman': 'Edit Buku',
        'label_tombol': 'Perbarui Buku',
        'active_nav': 'buku',
    })


def buku_delete(request, pk):
    buku = raw_get_or_404('perpustakaan_buku', pk)
    if request.method == 'POST':
        judul = buku['judul']
        raw_delete('perpustakaan_buku', pk)
        messages.success(request, f'Buku "{judul}" berhasil dihapus.')
        return redirect('buku_list')
    return render(request, 'perpustakaan/buku_confirm_delete.html', {
        'buku': buku,
        'active_nav': 'buku',
    })


# ---------------------------------------------------------------------------
# Peminjaman
# ---------------------------------------------------------------------------

def peminjaman_list(request):
    sql = '''
        SELECT
            p.id, p.petugas, p.tanggal_pinjam, p.tanggal_kembali, p.status,
            s.id AS peminjam_id, s.nama AS peminjam_nama,
            b.id AS buku_id, b.judul AS buku_judul, b.stok AS buku_stok
        FROM perpustakaan_peminjaman p
        JOIN perpustakaan_siswa s ON p.peminjam_id = s.id
        JOIN perpustakaan_buku b ON p.buku_id = b.id
        ORDER BY p.id DESC
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

    peminjaman_qs = []
    for (pid, petugas, tgl_pinjam, tgl_kembali, status,
         peminjam_id, peminjam_nama, buku_id, buku_judul, buku_stok) in rows:
        peminjaman_qs.append({
            'id': pid,
            'pk': pid,
            'petugas': petugas,
            'tanggal_pinjam': tgl_pinjam,
            'tanggal_kembali': tgl_kembali,
            'status': status,
            'peminjam': {'id': peminjam_id, 'pk': peminjam_id, 'nama': peminjam_nama},
            'buku': {'id': buku_id, 'pk': buku_id, 'judul': buku_judul, 'stok': buku_stok},
        })

    return render(request, 'perpustakaan/peminjaman_list.html', {
        'peminjaman_list': peminjaman_qs,
        'active_nav': 'peminjaman',
    })


def peminjaman_create(request):
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            # cleaned_data['buku'] / ['peminjam'] kemungkinan masih berupa
            # instance model (kalau field-nya ModelChoiceField di forms.py),
            # jadi kita ambil .pk-nya saja untuk dipakai di raw SQL.
            buku_obj = form.cleaned_data['buku']
            siswa_obj = form.cleaned_data['peminjam']
            petugas = form.cleaned_data['petugas']
            tanggal_pinjam = form.cleaned_data['tanggal_pinjam']

            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT stok, judul FROM perpustakaan_buku WHERE id = %s',
                    [buku_obj.pk]
                )
                row = cursor.fetchone()

            if row is None:
                raise Http404('Buku tidak ditemukan.')
            stok_sekarang, judul_buku = row

            if stok_sekarang < 1:
                messages.error(request, f'Stok buku "{judul_buku}" tidak tersedia.')
            else:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'UPDATE perpustakaan_buku SET stok = stok - 1 WHERE id = %s',
                        [buku_obj.pk]
                    )
                    cursor.execute(
                        '''
                        INSERT INTO perpustakaan_peminjaman
                            (peminjam_id, buku_id, petugas, tanggal_pinjam, tanggal_kembali, status)
                        VALUES (%s, %s, %s, %s, NULL, %s)
                        ''',
                        [siswa_obj.pk, buku_obj.pk, petugas, tanggal_pinjam, 'Dipinjam']
                    )

                messages.success(
                    request,
                    f'Peminjaman buku "{judul_buku}" oleh {siswa_obj.nama} berhasil dicatat.'
                )
                return redirect('peminjaman_list')
    else:
        initial = {
            'petugas': request.session.get('admin_aktif_nama', None) or 'Budi Siregar',
            'tanggal_pinjam': timezone.localdate(),
        }
        form = PeminjamanForm(initial=initial)
    return render(request, 'perpustakaan/peminjaman_form.html', {
        'form': form,
        'active_nav': 'peminjaman',
    })


def peminjaman_kembalikan(request, pk):
    sql = '''
        SELECT p.status, p.buku_id, b.judul, s.nama
        FROM perpustakaan_peminjaman p
        JOIN perpustakaan_buku b ON p.buku_id = b.id
        JOIN perpustakaan_siswa s ON p.peminjam_id = s.id
        WHERE p.id = %s
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql, [pk])
        row = cursor.fetchone()

    if row is None:
        raise Http404('Peminjaman tidak ditemukan.')

    status, buku_id, judul_buku, nama_peminjam = row

    if request.method == 'POST' and status == 'Dipinjam':
        tanggal_kembali = timezone.localdate()
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE perpustakaan_peminjaman SET status = %s, tanggal_kembali = %s WHERE id = %s',
                ['Dikembalikan', tanggal_kembali, pk]
            )
            cursor.execute(
                'UPDATE perpustakaan_buku SET stok = stok + 1 WHERE id = %s',
                [buku_id]
            )

        messages.success(
            request,
            f'Buku "{judul_buku}" yang dipinjam {nama_peminjam} telah dikembalikan.'
        )
    return redirect('peminjaman_list')


# ---------------------------------------------------------------------------
# User (Siswa)
# ---------------------------------------------------------------------------

def user_list(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM perpustakaan_siswa ORDER BY id')
        siswa_qs = dictfetchall(cursor)
    return render(request, 'perpustakaan/user_list.html', {
        'user_list': siswa_qs,
        'active_nav': 'user',
    })


def user_detail(request, pk):
    siswa = raw_get_or_404('perpustakaan_siswa', pk)
    return render(request, 'perpustakaan/user_detail.html', {
        'siswa': siswa,
        'active_nav': 'user',
    })


def user_create(request):
    if request.method == 'POST':
        form = SiswaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            raw_insert('perpustakaan_siswa', data)
            messages.success(request, f'User "{data["nama"]}" berhasil ditambahkan.')
            return redirect('user_list')
    else:
        form = SiswaForm()
    return render(request, 'perpustakaan/user_form.html', {
        'form': form,
        'judul_halaman': 'Tambah User',
        'label_tombol': 'Simpan User',
        'active_nav': 'user',
    })


def user_update(request, pk):
    siswa = raw_get_or_404('perpustakaan_siswa', pk)
    if request.method == 'POST':
        form = SiswaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            raw_update('perpustakaan_siswa', pk, data)
            messages.success(request, f'User "{data["nama"]}" berhasil diperbarui.')
            return redirect('user_list')
    else:
        form = SiswaForm(initial=siswa)
    return render(request, 'perpustakaan/user_form.html', {
        'form': form,
        'siswa': siswa,
        'judul_halaman': 'Edit User',
        'label_tombol': 'Perbarui User',
        'active_nav': 'user',
    })


def user_delete(request, pk):
    siswa = raw_get_or_404('perpustakaan_siswa', pk)
    if request.method == 'POST':
        nama = siswa['nama']
        raw_delete('perpustakaan_siswa', pk)
        messages.success(request, f'User "{nama}" berhasil dihapus.')
        return redirect('user_list')
    return render(request, 'perpustakaan/user_confirm_delete.html', {
        'siswa': siswa,
        'active_nav': 'user',
    })