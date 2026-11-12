import json
from pathlib import Path

def muat_basis_pengetahuan(nama_file="kb_energi.json"):
    """Membaca aturan dan pertanyaan dari file JSON."""
    jalur = Path(__file__).with_name(nama_file)
    with jalur.open("r", encoding="utf-8") as file:
        return json.load(file)

def tanya_fakta(pertanyaan):
    """Mengumpulkan fakta awal dari jawaban pengguna."""
    fakta = set()
    print("\nJawab pertanyaan dengan y (ya) atau t (tidak).")
    for nomor, item in enumerate(pertanyaan, start=1):
        while True:
            jawaban = input(f"{nomor}. {item['teks']} (y/t): ").strip().lower()
            if jawaban in ("y", "ya"):
                fakta.add(item["id"])
                break
            if jawaban in ("t", "tidak"):
                break
            print("Masukkan y untuk ya atau t untuk tidak.")
    return fakta

def syarat_terpenuhi(aturan, fakta):
    """Memeriksa premis aturan berdasarkan mode DAN/ATAU."""
    premis = aturan["jika"]
    mode = aturan.get("mode", "dan").lower()
    if mode == "dan":
        return all(item in fakta for item in premis)
    if mode == "atau":
        return any(item in fakta for item in premis)
    raise ValueError(f"Mode aturan tidak dikenal: {mode}")

def forward_chaining(basis, fakta_awal):
    """Menjalankan inferensi sampai tidak ada fakta baru."""
    fakta = set(fakta_awal)
    jejak = {}
    aturan_terpakai = []
    nomor_siklus = 0

    while True:
        nomor_siklus += 1
        ada_fakta_baru = False

        for aturan in basis["aturan"]:
            hasil = aturan["maka"]
            if hasil not in fakta and syarat_terpenuhi(aturan, fakta):
                fakta.add(hasil)
                jejak[hasil] = {
                    "aturan": aturan["id"],
                    "premis": aturan["jika"],
                    "sumber": aturan["sumber"]
                }
                aturan_terpakai.append(aturan["id"])
                ada_fakta_baru = True
                print(f"Siklus {nomor_siklus}: {aturan['id']} menghasilkan {hasil}")

        if not ada_fakta_baru:
            print(f"Siklus {nomor_siklus}: tidak ada fakta baru, proses berhenti.")
            break

    return fakta, jejak, aturan_terpakai

def tampilkan_hasil(basis, fakta, jejak, aturan_terpakai):
    """Menampilkan kesimpulan dan alasan aturan yang digunakan."""
    print("\n" + "=" * 58)
    print("HASIL SISTEM PAKAR PEMILIHAN ENERGI TERBARUKAN")
    print("=" * 58)

    hasil = [
        (kode, kalimat)
        for kode, kalimat in basis["kesimpulan"].items()
        if kode in fakta
    ]

    if not hasil:
        print("Belum ada rekomendasi yang memenuhi aturan.")
        print("Periksa kembali data kondisi wilayah atau lengkapi kajian sumber daya.")
    else:
        print("\nRekomendasi:")
        for nomor, (kode, kalimat) in enumerate(hasil, start=1):
            print(f"{nomor}. {kalimat}")
            info = jejak[kode]
            print(f"   Alasan: aturan {info['aturan']} terpenuhi.")
            print(f"   Premis: {', '.join(info['premis'])}")
            print(f"   Sumber aturan: {info['sumber']}")

    print("\nAturan yang dijalankan:", ", ".join(aturan_terpakai) if aturan_terpakai else "Tidak ada")
    print("\nCatatan batas keberlakuan:")
    print(basis["batas"])
    print("Hasil ini adalah saran awal, bukan keputusan akhir.")

def main():
    try:
        basis = muat_basis_pengetahuan()
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("Gagal membaca kb_energi.json:", error)
        return

    print("=" * 58)
    print(basis["judul"])
    print("=" * 58)
    print(basis["deskripsi"])
    fakta_awal = tanya_fakta(basis["pertanyaan"])
    print("\nFakta awal:", ", ".join(sorted(fakta_awal)) if fakta_awal else "Tidak ada fakta positif")

    fakta_akhir, jejak, aturan_terpakai = forward_chaining(basis, fakta_awal)
    tampilkan_hasil(basis, fakta_akhir, jejak, aturan_terpakai)

if __name__ == "__main__":
    main()
