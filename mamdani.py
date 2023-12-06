import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi Keanggotaan
suhu = ctrl.Antecedent(np.arange(35, 39, 0.1), 'suhu')
kondisi = ctrl.Consequent(np.arange(35, 39, 0.1), 'kondisi')

# Fungsi keanggotaan suhu
suhu['rendah'] = fuzz.trimf(suhu.universe, [34, 35, 36.5])
suhu['normal'] = fuzz.trimf(suhu.universe, [35.5, 36.5, 37.5])
suhu['tinggi'] = fuzz.trimf(suhu.universe, [36.5, 38, 39])

# Fungsi keanggotaan kondisi
kondisi['dingin'] = fuzz.trimf(kondisi.universe, [35, 35.8, 36.5])
kondisi['normal'] = fuzz.trimf(kondisi.universe, [35.8, 36.5, 37.2])
kondisi['panas'] = fuzz.trimf(kondisi.universe, [36.5, 37.2, 38])

# Rule Base
rule1 = ctrl.Rule(suhu['rendah'], kondisi['dingin'])
rule2 = ctrl.Rule(suhu['tinggi'], kondisi['panas'])
rule3 = ctrl.Rule(suhu['normal'], kondisi['normal'])

# Sistem Inferensi Fuzzy
kondisi_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kondisi_prediksi = ctrl.ControlSystemSimulation(kondisi_ctrl)

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
]

# Program Utama
def main():
    suhu_min = 35
    suhu_max = 38
    suhu_step = 0.1

    print("Status Kondisi Tubuh untuk Setiap Suhu:")
    print("----------------------------------------")
    for suhu_val in np.arange(suhu_min, suhu_max + suhu_step, suhu_step):
        kondisi_prediksi.input['suhu'] = suhu_val
        kondisi_prediksi.compute()

        # Mengambil crisp output dari kondisi_prediksi
        kondisi_tubuh = kondisi_prediksi.output['kondisi']

        # Menentukan kondisi prediksi berdasarkan crisp output
        if kondisi_tubuh <= 36.5:
            kondisi_prediksi_str = "Dingin"
        elif kondisi_tubuh <= 37.2:
            kondisi_prediksi_str = "Normal"
        else:
            kondisi_prediksi_str = "Panas"

        # Menampilkan hasil
        print(f"Suhu: {suhu_val:.1f}  ->  Kondisi Tubuh: {kondisi_prediksi_str}")

    # Menghitung dan menampilkan akurasi
    akurasi = hitung_akurasi(data_referensi)
    print(f"\nAkurasi: {akurasi:.2f}%")

# Fungsi Akurasi
def hitung_akurasi(data_referensi):
    total_data = len(data_referensi)
    benar = 0

    for suhu, kondisi_aktual in data_referensi:
        kondisi_prediksi.input['suhu'] = suhu
        kondisi_prediksi.compute()

        # Mengambil crisp output dari kondisi_prediksi
        kondisi_tubuh = kondisi_prediksi.output['kondisi']

        # Menentukan kondisi prediksi berdasarkan crisp output
        if kondisi_tubuh <= 36.5:
            kondisi_prediksi_str = "Dingin"
        elif kondisi_tubuh <= 37.2:
            kondisi_prediksi_str = "Normal"
        else:
            kondisi_prediksi_str = "Panas"

        # Memeriksa kesesuaian prediksi dengan kondisi aktual
        if kondisi_prediksi_str == kondisi_aktual:
            benar += 1

    akurasi = benar / total_data * 100
    return akurasi

if __name__ == "__main__":
    main()
