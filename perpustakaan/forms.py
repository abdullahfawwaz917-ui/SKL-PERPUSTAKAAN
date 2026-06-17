from django import forms

from .models import Buku, Siswa, Peminjaman


class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ['judul', 'pengarang', 'kategori', 'penerbit', 'tahun_terbit',
                  'stok', 'isbn', 'rak_lokasi', 'deskripsi']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'field-input'}),
            'pengarang': forms.TextInput(attrs={'class': 'field-input'}),
            'kategori': forms.Select(attrs={'class': 'field-input'}),
            'penerbit': forms.TextInput(attrs={'class': 'field-input'}),
            'tahun_terbit': forms.NumberInput(attrs={'class': 'field-input'}),
            'stok': forms.NumberInput(attrs={'class': 'field-input'}),
            'isbn': forms.TextInput(attrs={'class': 'field-input'}),
            'rak_lokasi': forms.TextInput(attrs={'class': 'field-input'}),
            'deskripsi': forms.Textarea(attrs={'class': 'field-input', 'rows': 4}),
        }


class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = ['nama', 'kelas', 'nis', 'status']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'field-input'}),
            'kelas': forms.TextInput(attrs={'class': 'field-input'}),
            'nis': forms.TextInput(attrs={'class': 'field-input'}),
            'status': forms.Select(attrs={'class': 'field-input'}),
        }


class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = ['peminjam', 'buku', 'tanggal_pinjam', 'tanggal_jatuh_tempo',
                  'keperluan', 'petugas', 'catatan']
        widgets = {
            'peminjam': forms.Select(attrs={'class': 'field-input'}),
            'buku': forms.Select(attrs={'class': 'field-input'}),
            'tanggal_pinjam': forms.DateInput(attrs={'class': 'field-input', 'type': 'date'}),
            'tanggal_jatuh_tempo': forms.DateInput(attrs={'class': 'field-input', 'type': 'date'}),
            'keperluan': forms.Select(attrs={'class': 'field-input'}),
            'petugas': forms.TextInput(attrs={'class': 'field-input'}),
            'catatan': forms.Textarea(attrs={
                'class': 'field-input',
                'rows': 4,
                'placeholder': 'Contoh: buku untuk tugas Bahasa Indonesia',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hanya tampilkan siswa yang masih aktif sebagai pilihan peminjam.
        self.fields['peminjam'].queryset = Siswa.objects.filter(status='Aktif')
        self.fields['peminjam'].label_from_instance = lambda s: f'{s.nama} - {s.kelas} ({s.nis})'
        self.fields['buku'].label_from_instance = lambda b: f'{b.judul} ({b.stok} stok)'
        # Hanya tampilkan buku yang masih memiliki stok (kecuali saat edit buku yang sama).
        if not (self.instance and self.instance.pk):
            self.fields['buku'].queryset = Buku.objects.filter(stok__gt=0)
