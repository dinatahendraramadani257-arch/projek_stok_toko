from .processing import Barang
from .validasi import DataTidakValid


def buat_file_data(path, isi_awal=""):
    try:
        with open(path, "x", encoding="utf-8") as file:
            file.write(isi_awal)
        return True
    except FileExistsError:
        print(f"[INFO] File '{path}' sudah ada, tidak ditimpa.")
        return False


def tambah_barang(path, barang):
    with open(path, "a", encoding="utf-8") as file:
        file.write(barang.ke_baris())


def baca_data(path):
    daftar, rusak = [], []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for no, baris in enumerate(file, start=1):
                if not baris.strip():
                    continue
                try:
                    daftar.append(Barang.dari_baris(baris))
                except DataTidakValid as err:
                    rusak.append((no, str(err)))
    except FileNotFoundError:
        print(f"[ERROR] File '{path}' belum ada.")
    return daftar, rusak


def tulis_laporan(path, teks):
    with open(path, "w", encoding="utf-8") as file:
        file.write(teks)


def baca_isi(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
