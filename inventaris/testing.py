import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from . import fileio
from .processing import Barang, Inventaris, hitung_total
from .validasi import DataTidakValid, validasi_angka, validasi_teks


class TestInventaris(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "data.txt")
        self.inv = Inventaris([
            Barang("Gula", 17500, 30),
            Barang("Teh", 5000, 3),
            Barang("Beras", 68000, 25),
        ])

    def tearDown(self):
        self.tmp.cleanup()

    def test_total_nilai_barang(self):
        self.assertEqual(Barang("Pensil", 2000, 10).total_nilai(), 20000)

    def test_hitung_total_args(self):
        self.assertEqual(hitung_total(1, 2, 3, 4), 10)

    def test_harga_negatif_raise(self):
        with self.assertRaises(DataTidakValid):
            validasi_angka("-100", "harga")

    def test_nama_kosong_raise(self):
        with self.assertRaises(DataTidakValid):
            validasi_teks(" ", "nama")

    def test_kwargs_atribut(self):
        b = Barang("Mie", 3500, 10, merek="Indomie", satuan="pcs")
        self.assertEqual(b.atribut, {"merek": "Indomie", "satuan": "pcs"})

    def test_stok_menipis(self):
        self.assertEqual(
            [b.nama for b in self.inv.stok_menipis(batas=5)], ["Teh"]
        )

    def test_urutkan_harga_turun(self):
        self.assertEqual(
            [b.nama for b in self.inv.urutkan_harga(turun=True)],
            ["Beras", "Gula", "Teh"],
        )

    def test_baris_rusak_dilewati(self):
        isi = "Gula;17500;30\nTeh;abc;3\n;100;1\nPena;2000;8\n"
        fileio.buat_file_data(self.path, isi)
        daftar, rusak = fileio.baca_data(self.path)
        self.assertEqual(len(daftar), 2)
        self.assertEqual(len(rusak), 2)

    def test_file_tidak_ada(self):
        with redirect_stdout(io.StringIO()) as keluar:
            hasil = fileio.baca_data(
                os.path.join(self.tmp.name, "tidak_ada.txt")
            )
        self.assertEqual(hasil, ([], []))
        self.assertIn("belum ada", keluar.getvalue())

    def test_mode_x_tidak_menimpa(self):
        fileio.buat_file_data(self.path, "ISI LAMA\n")
        with redirect_stdout(io.StringIO()):
            hasil = fileio.buat_file_data(self.path, "ISI BARU\n")
        self.assertFalse(hasil)
        self.assertEqual(fileio.baca_isi(self.path), "ISI LAMA\n")


def jalankan_semua_tes():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestInventaris)
    return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    unittest.main()
