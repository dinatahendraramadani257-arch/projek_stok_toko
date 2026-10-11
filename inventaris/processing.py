from .validasi import DataTidakValid, validasi_angka, validasi_teks


def hitung_total(*angka):
    return sum(angka)


class Barang:

    def __init__(self, nama, harga, stok, **atribut):
        self.nama = validasi_teks(nama, "nama")
        self.harga = validasi_angka(harga, "harga")
        self.stok = validasi_angka(stok, "stok")
        self.atribut = atribut

    def total_nilai(self):
        assert self.harga >= 0 and self.stok >= 0, "harga/stok negatif"
        return self.harga * self.stok

    def ke_baris(self):
        baris = f"{self.nama};{self.harga};{self.stok}"
        if self.atribut:
            baris += ";" + ",".join(f"{k}={v}" for k, v in self.atribut.items())
        return baris + "\n"

    @classmethod
    def dari_baris(cls, baris):
        bagian = baris.strip().split(";")
        if len(bagian) < 3:
            raise DataTidakValid(
                "jumlah kolom kurang (butuh nama;harga;stok)"
            )
        atribut = {}
        if len(bagian) > 3:
            for item in bagian[3].split(","):
                kunci, _, nilai = item.partition("=")
                atribut[kunci] = nilai
        return cls(bagian[0], bagian[1], bagian[2], **atribut)

    def __str__(self):
        info = f" {self.atribut}" if self.atribut else ""
        return f"{self.nama:<18} Rp{self.harga:>7,} stok {self.stok:>4}{info}"


class Inventaris:

    def __init__(self, daftar_barang):
        self.daftar = list(daftar_barang)

    def total_nilai_stok(self):
        return hitung_total(*[b.total_nilai() for b in self.daftar])

    def stok_menipis(self, batas=5):
        return list(filter(lambda b: b.stok <= batas, self.daftar))

    def urutkan_harga(self, turun=True):
        return sorted(self.daftar, key=lambda b: b.harga, reverse=turun)

    def buat_laporan(self, batas_stok=5):
        termahal = self.urutkan_harga(turun=True)[0]
        menipis = self.stok_menipis(batas=batas_stok)
        baris = [
            "LAPORAN INVENTARIS TOKO",
            "=======================",
            f"Jumlah jenis barang : {len(self.daftar)}",
            f"Total nilai stok    : Rp{self.total_nilai_stok():,}",
            f"Barang termahal     : {termahal.nama} (Rp{termahal.harga:,})",
            "",
            f"Stok menipis (<= {batas_stok}):",
        ]
        baris += [f"- {b.nama} (sisa {b.stok})" for b in menipis] or [
            "- (tidak ada)"
        ]
        return "\n".join(baris) + "\n"


if __name__ == "__main__":
    contoh = Inventaris([Barang("Gula", 17500, 30), Barang("Teh", 5000, 3)])
    assert contoh.total_nilai_stok() == 17500 * 30 + 5000 * 3
    assert [b.nama for b in contoh.stok_menipis(batas=5)] == ["Teh"]
    print("Pengujian lokal processing.py berhasil")
