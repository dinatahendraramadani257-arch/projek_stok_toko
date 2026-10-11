import os
from inventaris import fileio
from inventaris.processing import Barang, Inventaris
from inventaris.testing import jalankan_semua_tes
from inventaris.validasi import DataTidakValid

FILE_DATA = os.path.join("data", "inventaris.txt")
FILE_LAPORAN = os.path.join("data", "laporan_inventaris.txt")

DATA_AWAL = """Beras 5kg;68000;25;merek=Sania
Minyak Goreng 2L;36000;4
Gula Pasir 1kg;17500;30
Mie Instan;abc;120
Teh Botol;5000;3
;4000;10
Susu UHT 1L;18500;18
"""


def muat_data():
    daftar, rusak = fileio.baca_data(FILE_DATA)
    for no, alasan in rusak:
        print(f"  [DILEWATI] baris {no}: {alasan}")
    return daftar


def menu_tampilkan():
    daftar = muat_data()
    print(f"\n=== DAFTAR BARANG ({len(daftar)} valid) ===")
    for barang in daftar:
        print(barang)


def menu_tambah():
    print("\n=== TAMBAH BARANG ===")
    nama = input("Nama  : ")
    harga = input("Harga : ")
    stok = input("Stok  : ")
    extra = input(
        "Atribut tambahan (mis. merek=Roma,satuan=bks; boleh kosong): "
    )
    atribut = dict(p.split("=", 1) for p in extra.split(",") if "=" in p)
    try:
        barang = Barang(nama, harga, stok, **atribut)
        fileio.tambah_barang(FILE_DATA, barang)
        print("Barang berhasil ditambahkan.")
    except DataTidakValid as err:
        print(f"Gagal menambah barang: {err}")


def menu_laporan():
    inventaris = Inventaris(muat_data())
    fileio.tulis_laporan(FILE_LAPORAN, inventaris.buat_laporan(batas_stok=5))
    print(f"\nLaporan disimpan ke {FILE_LAPORAN}:\n")
    print(fileio.baca_isi(FILE_LAPORAN))


def main():
    os.makedirs("data", exist_ok=True)
    if fileio.buat_file_data(FILE_DATA, DATA_AWAL):
        print("File data awal dibuat.")

    menu = {
        "1": ("Tampilkan semua barang", menu_tampilkan),
        "2": ("Tambah barang baru", menu_tambah),
        "3": ("Buat & tampilkan laporan", menu_laporan),
        "4": ("Jalankan unit test", jalankan_semua_tes),
    }

    while True:
        print("\n===== STOK TOKO =====")
        for kunci, (judul, _) in menu.items():
            print(f"{kunci}. {judul}")
        print("0. Keluar")

        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Terima kasih.")
            break
        if pilihan in menu:
            menu[pilihan][1]()
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
