# konsultan_bmi_visual.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np
# --- SOLUSI UNTUK ERROR TclError ---
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# ------------------------------------

# --- Bagian 1: Pelatihan Model ---

# Memuat dan Mempersiapkan Data
try:
    df = pd.read_csv('500_Person_Gender_Height_Weight_Index.csv')
except FileNotFoundError:
    print("Error: File '500_Person_Gender_Height_Weight_Index.csv' tidak ditemukan.")
    exit()

# Pra-pemrosesan
le = LabelEncoder()
df['Gender'] = le.fit_transform(df['Gender'])

# Pisahkan Fitur (X) dan Target (y)
X = df[['Gender', 'Height', 'Weight']]
y = df['Index']

kategori_bmi = [
    'Sangat Kurus', 'Kurus', 'Normal', 'Gemuk', 'Obesitas', 'Obesitas Ekstrim'
]

# Latih model menggunakan SELURUH data
model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X, y)
print("Model Decision Tree berhasil dilatih.")


# --- Bagian 2: Membuat Visualisasi Penuh (BARU!) ---

print("\nMembuat peta keputusan visual...")
plt.figure(figsize=(20, 12))
plot_tree(
    model,
    feature_names=X.columns,
    class_names=kategori_bmi,
    filled=True,
    rounded=True,
    fontsize=10,
    node_ids=True # Menampilkan ID untuk setiap node agar mudah dilacak
)
plt.savefig('decision_tree_bmi_map.png')
print("Peta keputusan telah disimpan sebagai 'decision_tree_bmi_map.png'")
print(">>> Silakan buka file gambar tersebut untuk mengikuti jejak visualnya. <<<")


# --- Bagian 3: Fungsi Konsultasi Interaktif ---

def jalankan_konsultasi_interaktif(model, feature_names, class_names):
    """
    Memandu pengguna melalui pohon keputusan secara interaktif.
    """
    print("\n--- Selamat Datang di Konsultan BMI Interaktif ---")
    
    try:
        gender_input = input("Masukkan Gender Anda (pria/wanita): ").lower()
        gender = 0 if gender_input == 'wanita' else 1

        height = float(input("Masukkan Tinggi Badan Anda (dalam cm): "))
        weight = float(input("Masukkan Berat Badan Anda (dalam kg): "))
        
        user_data = pd.DataFrame([[gender, height, weight]], columns=feature_names)
        
    except ValueError:
        print("Input tidak valid. Harap masukkan angka untuk tinggi dan berat.")
        return

    print("\n--- Menganalisis Data Anda Melalui Peta Keputusan ---")
    
    tree = model.tree_
    node_id = 0
    langkah = 1

    while tree.children_left[node_id] != tree.children_right[node_id]:
        feature_index = tree.feature[node_id]
        feature_name = feature_names[feature_index]
        threshold = tree.threshold[node_id]
        user_value = user_data[feature_name].iloc[0]

        print(f"Langkah {langkah}: Berada di Node #{node_id}")
        print(f"   -> Pertanyaan Model: Apakah '{feature_name}' <= {threshold:.2f}?")
        
        if user_value <= threshold:
            print(f"   -> Jawaban Anda ({user_value}) memenuhi syarat. Pindah ke kiri.")
            node_id = tree.children_left[node_id]
        else:
            print(f"   -> Jawaban Anda ({user_value}) tidak memenuhi syarat. Pindah ke kanan.")
            node_id = tree.children_right[node_id]
        
        langkah += 1
        print("-" * 20)

    print(f"Langkah {langkah}: Mencapai Daun (Leaf Node) #{node_id}")
    prediksi_index = np.argmax(tree.value[node_id])
    hasil_akhir = class_names[prediksi_index]
    
    print("\n--- Hasil Akhir ---")
    print(f"Berdasarkan analisis, kategori BMI Anda adalah: {hasil_akhir}")


# --- Menjalankan Program Utama ---
if __name__ == "__main__":
    jalankan_konsultasi_interaktif(model, X.columns, kategori_bmi)