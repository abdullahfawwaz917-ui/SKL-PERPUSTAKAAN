from django.conf import settings


def admin_aktif(request):
    """Membuat nama admin/petugas yang sedang aktif tersedia di semua template."""
    return {
        'admin_aktif_nama': getattr(settings, 'ADMIN_AKTIF_NAMA', 'Admin'),
    }
