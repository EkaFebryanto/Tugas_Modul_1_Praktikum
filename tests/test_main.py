# tests/test_main.py
import pytest

from src.models import DaftarMahasiswa, Mahasiswa


class TestMahasiswa:
    def test_buat_mahasiswa_valid(self):
        mhs = Mahasiswa("2024SI001", "Andi Pratama", "Sistem Informasi", 2024, 3.50)
        assert mhs.nim == "2024SI001"
        assert mhs.ipk == 3.50

    def test_nim_tidak_valid(self):
        with pytest.raises(ValueError):
            Mahasiswa("abc", "Test", "SI", 2024, 3.0)

    def test_ipk_diluar_range(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI002", "Test", "SI", 2024, 5.0)


class TestDaftarMahasiswa:
    def test_tambah_dan_cari(self):
        db = DaftarMahasiswa()
        mhs = Mahasiswa("2024SI001", "Andi", "SI", 2024)
        db.tambah(mhs)
        assert db.cari("2024SI001") == mhs
        assert db.jumlah == 1

    def test_nim_duplikat(self):
        db = DaftarMahasiswa()
        m1 = Mahasiswa("2024SI001", "Andi", "SI", 2024)
        m2 = Mahasiswa("2024SI001", "Budi", "SI", 2024)
        db.tambah(m1)
        with pytest.raises(ValueError):
            db.tambah(m2)


# ---------------------------------------------------------------------------
# Tugas Pengayaan: test tambahan untuk edge case
# ---------------------------------------------------------------------------
class TestEdgeCaseMahasiswa:
    def test_nim_kosong(self):
        with pytest.raises(ValueError, match="NIM tidak valid"):
            Mahasiswa("", "Andi", "SI", 2024, 3.0)

    def test_nim_terlalu_pendek_batas(self):
        with pytest.raises(ValueError):
            Mahasiswa("12345", "Andi", "SI", 2024)  # 5 karakter -> tidak valid
        assert Mahasiswa("123456", "Andi", "SI", 2024).nim == "123456"  # 6 -> valid

    def test_nama_kosong_dan_spasi(self):
        with pytest.raises(ValueError, match="Nama tidak boleh kosong"):
            Mahasiswa("2024SI003", "", "SI", 2024)
        with pytest.raises(ValueError, match="Nama tidak boleh kosong"):
            Mahasiswa("2024SI003", "   ", "SI", 2024)

    def test_nama_sangat_panjang_ditolak(self):
        with pytest.raises(ValueError, match="maksimal"):
            Mahasiswa("2024SI004", "A" * 101, "SI", 2024)

    def test_nama_panjang_batas_diterima(self):
        assert len(Mahasiswa("2024SI004", "A" * 100, "SI", 2024).nama) == 100

    def test_ipk_boundary_nol_dan_empat(self):
        assert Mahasiswa("2024SI005", "Nol", "SI", 2024, 0.0).ipk == 0.0
        assert Mahasiswa("2024SI006", "Empat", "SI", 2024, 4.0).ipk == 4.0

    def test_ipk_tepat_di_luar_batas(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI007", "Minus", "SI", 2024, -0.01)
        with pytest.raises(ValueError):
            Mahasiswa("2024SI008", "Lebih", "SI", 2024, 4.01)

    def test_ipk_default_nol(self):
        assert Mahasiswa("2024SI009", "Default", "SI", 2024).ipk == 0.0

    def test_str_menampilkan_ipk_dua_desimal(self):
        assert "IPK: 3.50" in str(Mahasiswa("2024SI010", "Format", "SI", 2024, 3.5))


class TestEdgeCaseDaftar:
    def setup_method(self):
        self.db = DaftarMahasiswa()
        self.db.tambah(Mahasiswa("2024SI001", "Andi", "SI", 2024, 3.0))

    def test_hapus_nim_tidak_ada(self):
        assert self.db.hapus("TIDAKADA") is False
        assert self.db.jumlah == 1  # data tidak berubah

    def test_cari_nim_tidak_ada(self):
        assert self.db.cari("TIDAKADA") is None

    def test_hapus_nim_ada(self):
        assert self.db.hapus("2024SI001") is True
        assert self.db.jumlah == 0
        assert self.db.cari("2024SI001") is None

    def test_hapus_dari_daftar_kosong(self):
        assert DaftarMahasiswa().hapus("2024SI001") is False

    def test_duplikat_tidak_menambah_data(self):
        with pytest.raises(ValueError, match="sudah terdaftar"):
            self.db.tambah(Mahasiswa("2024SI001", "Budi", "SI", 2024))
        assert self.db.jumlah == 1

    def test_edit_ipk_berhasil(self):
        assert self.db.edit_ipk("2024SI001", 3.75) is True
        assert self.db.cari("2024SI001").ipk == 3.75

    def test_edit_ipk_boundary(self):
        assert self.db.edit_ipk("2024SI001", 0.0) is True
        assert self.db.edit_ipk("2024SI001", 4.0) is True

    def test_edit_ipk_di_luar_range(self):
        with pytest.raises(ValueError):
            self.db.edit_ipk("2024SI001", 4.5)
        assert self.db.cari("2024SI001").ipk == 3.0  # tidak berubah

    def test_edit_ipk_nim_tidak_ada(self):
        assert self.db.edit_ipk("TIDAKADA", 3.0) is False
