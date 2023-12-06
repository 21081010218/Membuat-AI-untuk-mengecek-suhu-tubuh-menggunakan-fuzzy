import numpy as np

# Fungsi Keanggotaan
def rendah(x, a, b):
    if x <= a:
        return 1
    elif a < x < b:
        return (b - x) / (b - a)
    else:
        return 0

def tinggi(x, a, b):
    if x >= b:
        return 1
    elif a < x < b:
        return (x - a) / (b - a)
    else:
        return 0

# Rule Base
rules = [
    # JIKA suhu adalah Rendah MAKA kondisi adalah Dingin
    [(rendah, 35, 36), (rendah, 36.5, 37.5)],

    # JIKA suhu adalah Tinggi MAKA kondisi adalah Panas
    [(tinggi, 37, 38), (tinggi, 36.5, 37.5)],
]

# Fuzzifikasi
def fuzzifikasi(x, a, b):
    return rendah(x, a, b), tinggi(x, a, b)

# Inferensi
def inferensi(suhu_rendah, suhu_tinggi):
    output = np.zeros(3)
    for rule in rules:
        rendah_degree = min(suhu_rendah, rule[0][0](suhu_rendah, *rule[0][1:]))
        tinggi_degree = min(suhu_tinggi, rule[1][0](suhu_tinggi, *rule[1][1:]))
        output[0] = max(output[0], rendah_degree)
        output[1] = max(output[1], tinggi_degree)
        output[2] = max(output[2], min(rendah_degree, tinggi_degree))
    return output

# Defuzzifikasi menggunakan metode Tsukamoto
def defuzzifikasi(output):
    x = np.arange(35, 39, 0.1)
    kondisi = np.zeros_like(x)
    for i, val in enumerate(x):
        kondisi[i] = max(min(rendah(val, 35, 36), output[0]), min(tinggi(val, 36.5, 37.5), output[2]))
    return np.sum(x * kondisi) / np.sum(kondisi)

# Akurasi
def hitung_akurasi(data_referensi):
    total_data = len(data_referensi)
    benar = 0

    for suhu, kondisi_aktual in data_referensi:
        # Fuzzifikasi
        suhu_rendah, suhu_tinggi = fuzzifikasi(suhu, 35, 38)

        # Inferensi
        output = inferensi(suhu_rendah, suhu_tinggi)

        # Defuzzifikasi
        kondisi_tubuh = defuzzifikasi(output)

        # Mendapatkan kondisi tubuh prediksi dalam bentuk teks
        if kondisi_tubuh <= 36.5:
            kondisi_prediksi = "Dingin"
        elif kondisi_tubuh > 36.5 and kondisi_tubuh <= 37.5:
            kondisi_prediksi = "Normal"
        else:
            kondisi_prediksi = "Panas"

        # Memeriksa kesesuaian prediksi dengan kondisi aktual
        if kondisi_prediksi == kondisi_aktual:
            benar += 1

    akurasi = benar / total_data * 100
    return akurasi

# Data Referensi
data_referensi = [
    (36.2, "Dingin"),
    (36.8, "Normal"),
    (37.4, "Normal"),
    (37.9, "Panas"),
    (35.5, "Dingin"),
    (37.2, "Normal"),
    (36.9, "Normal"),
    (38.1, "Panas"),
    # Tambahkan data referensi lainnya sesuai kebutuhan
]

# Program Utama
def main():
    suhu_min = 35
    suhu_max = 38
    suhu_step = 0.1

    print("Status Kondisi Tubuh untuk Setiap Suhu:")
    print("----------------------------------------")
    for suhu in np.arange(suhu_min, suhu_max + suhu_step, suhu_step):
        # Fuzzifikasi
        suhu_rendah, suhu_tinggi = fuzzifikasi(suhu, 35, 38)

        # Inferensi
        output = inferensi(suhu_rendah, suhu_tinggi)

        # Defuzzifikasi
        kondisi_tubuh = defuzzifikasi(output)

        # Mendapatkan kondisi tubuh prediksi dalam bentuk teks
        if kondisi_tubuh <= 36.5:
            kondisi_prediksi = "Dingin"
        elif kondisi_tubuh > 36.5 and kondisi_tubuh <= 37.5:
            kondisi_prediksi = "Normal"
        else:
            kondisi_prediksi = "Panas"

        # Menampilkan hasil
        print(f"Suhu: {suhu:.1f} | Kondisi Tubuh: {kondisi_prediksi}")

    # Menghitung dan menampilkan akurasi
    akurasi = hitung_akurasi(data_referensi)
    print(f"Akurasi: {akurasi:.2f}%")

if __name__ == "__main__":
    main()
