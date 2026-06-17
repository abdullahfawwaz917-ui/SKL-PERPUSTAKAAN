from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import BukuForm, SiswaForm, PeminjamanForm
from .models import Buku, Siswa, Peminjaman


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def dashboard(request):
    semua_buku = Buku.objects.all()
    total_buku = semua_buku.aggregate(total=Sum('stok'))['total'] or 0
    total_judul = semua_buku.count()
    sedang_dipinjam = Peminjaman.objects.filter(status='Dipinjam').count()
    sudah_dikembalikan = Peminjaman.objects.filter(status='Dikembalikan').count()

    stok_max = max([b.stok for b in semua_buku], default=0) or 1
    distribusi_stok = [
        {'buku': b, 'persen': round(b.stok / stok_max * 100)} for b in semua_buku
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
    buku_qs = Buku.objects.all()
    return render(request, 'perpustakaan/buku_list.html', {
        'buku_list': buku_qs,
        'active_nav': 'buku',
    })


def buku_detail(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    return render(request, 'perpustakaan/buku_detail.html', {
        'buku': buku,
        'active_nav': 'buku',
    })


def buku_create(request):
    if request.method == 'POST':
        form = BukuForm(request.POST)
        if form.is_valid():
            buku = form.save()
            messages.success(request, f'Buku "{buku.judul}" berhasil ditambahkan.')
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
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        form = BukuForm(request.POST, instance=buku)
        if form.is_valid():
            form.save()
            messages.success(request, f'Buku "{buku.judul}" berhasil diperbarui.')
            return redirect('buku_list')
    else:
        form = BukuForm(instance=buku)
    return render(request, 'perpustakaan/buku_form.html', {
        'form': form,
        'buku': buku,
        'judul_halaman': 'Edit Buku',
        'label_tombol': 'Perbarui Buku',
        'active_nav': 'buku',
    })


def buku_delete(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        judul = buku.judul
        buku.delete()
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
    peminjaman_qs = Peminjaman.objects.select_related('peminjam', 'buku').all()
    return render(request, 'perpustakaan/peminjaman_list.html', {
        'peminjaman_list': peminjaman_qs,
        'active_nav': 'peminjaman',
    })


def peminjaman_create(request):
    if request.method == 'POST':
        form = PeminjamanForm(request.POST)
        if form.is_valid():
            peminjaman = form.save(commit=False)
            buku = peminjaman.buku
            if buku.stok < 1:
                messages.error(request, f'Stok buku "{buku.judul}" tidak tersedia.')
            else:
                buku.stok -= 1
                buku.save()
                peminjaman.status = 'Dipinjam'
                peminjaman.save()
                messages.success(
                    request,
                    f'Peminjaman buku "{buku.judul}" oleh {peminjaman.peminjam.nama} berhasil dicatat.'
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
    peminjaman = get_object_or_404(Peminjaman, pk=pk)
    if request.method == 'POST' and peminjaman.status == 'Dipinjam':
        peminjaman.status = 'Dikembalikan'
        peminjaman.tanggal_kembali = timezone.localdate()
        peminjaman.save()

        buku = peminjaman.buku
        buku.stok += 1
        buku.save()

        messages.success(
            request,
            f'Buku "{buku.judul}" yang dipinjam {peminjaman.peminjam.nama} telah dikembalikan.'
        )
    return redirect('peminjaman_list')


# ---------------------------------------------------------------------------
# User (Siswa)
# ---------------------------------------------------------------------------

def user_list(request):
    siswa_qs = Siswa.objects.all()
    return render(request, 'perpustakaan/user_list.html', {
        'user_list': siswa_qs,
        'active_nav': 'user',
    })


def user_detail(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    return render(request, 'perpustakaan/user_detail.html', {
        'siswa': siswa,
        'active_nav': 'user',
    })


def user_create(request):
    if request.method == 'POST':
        form = SiswaForm(request.POST)
        if form.is_valid():
            siswa = form.save()
            messages.success(request, f'User "{siswa.nama}" berhasil ditambahkan.')
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
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        form = SiswaForm(request.POST, instance=siswa)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{siswa.nama}" berhasil diperbarui.')
            return redirect('user_list')
    else:
        form = SiswaForm(instance=siswa)
    return render(request, 'perpustakaan/user_form.html', {
        'form': form,
        'siswa': siswa,
        'judul_halaman': 'Edit User',
        'label_tombol': 'Perbarui User',
        'active_nav': 'user',
    })


def user_delete(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        nama = siswa.nama
        siswa.delete()
        messages.success(request, f'User "{nama}" berhasil dihapus.')
        return                                          redirect('user_list')
    return render(request, 'perpustakaan/user_confirm_delete.html', {
        'siswa': siswa,
        'active_nav': 'user',
    })
