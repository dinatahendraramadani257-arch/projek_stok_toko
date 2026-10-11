class DataTidakValid(Exception):
    pass


def validasi_teks(nilai, nama_field):
    teks = str(nilai).strip()
    if not teks:
        raise DataTidakValid(f"'{nama_field}' tidak boleh kosong")
    return teks


def validasi_angka(nilai, nama_field):
    try:
        angka = int(nilai)
    except ValueError:
        raise DataTidakValid(f"'{nama_field}' harus angka: {nilai!r}") from None
    if angka < 0:
        raise DataTidakValid(f"'{nama_field}' tidak boleh negatif: {angka}")
    return angka


if __name__ == "__main__":
    assert validasi_angka("15000", "harga") == 15000
    assert validasi_teks(" Beras ", "nama") == "Beras"
    print("Pengujian lokal validasi.py berhasil")
