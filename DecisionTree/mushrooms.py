import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Bagian 1: Pelatihan Model ---

try:
    df = pd.read_csv('mushrooms.csv')
    print("Dataset berhasil dimuat.")
except FileNotFoundError:
    print("Error: File 'mushrooms.csv' tidak ditemukan.")
    print("Pastikan file tersebut berada di folder yang sama dengan skrip ini.")
    exit()

df_asli = df.copy()

label_encoders = {}
for column in df.columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

X = df.drop('class', axis=1)
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)
model.fit(X_train, y_train)
print("Model Decision Tree untuk jamur berhasil dilatih.")

# --- Bagian 2: Membuat Visualisasi Penuh dengan Path yang Benar ---

print("\nMembuat peta keputusan visual...")
plt.figure(figsize=(20, 12))
plot_tree(
    model,
    feature_names=X.columns,
    class_names=['Edible', 'Poisonous'],
    filled=True,
    rounded=True,
    fontsize=10,
    node_ids=True 
)

direktori_skrip = os.path.dirname(os.path.abspath(__file__))
nama_file_visualisasi = 'decision_tree_mushroom_map.png'
path_simpan_file = os.path.join(direktori_skrip, nama_file_visualisasi)

plt.savefig(path_simpan_file)
print(f"Peta keputusan telah disimpan di: {path_simpan_file}")
print(">>> Silakan buka file gambar tersebut untuk mengikuti jejak visualnya. <<<")


# --- Bagian 3: Fungsi Analisis Interaktif untuk Satu Jamur ---

def analisis_satu_jamur(model, X_test, y_test, df_asli, label_encoders):
    """
    Memilih satu jamur acak dari data uji dan menunjukkan proses klasifikasinya.
    """
    if X_test.empty:
        print("\nData uji kosong, tidak ada jamur yang bisa dianalisis.")
        return
        
    random_index = X_test.sample(1).index[0]
    jamur_fitur_encoded = X_test.loc[[random_index]]
    jawaban_asli_encoded = y_test.loc[random_index]

    print("\n--- Menganalisis Satu Jamur Misterius dari Dataset ---")
    jamur_asli = df_asli.loc[random_index]
    print("Profil Jamur:")
    profil_list = [f"  - {col:<30}: {val}" for col, val in jamur_asli.items() if col != 'class']
    for i in range((len(profil_list) + 1) // 2):
        kiri = profil_list[i]
        kanan = profil_list[i + (len(profil_list) + 1) // 2] if i + (len(profil_list) + 1) // 2 < len(profil_list) else ""
        print(f"{kiri}{kanan}")

    nama_kelas = label_encoders['class'].classes_
    print(f"\nMenurut data, jamur ini sebenarnya adalah: '{nama_kelas[jawaban_asli_encoded]}' (p=poisonous, e=edible)")

    print("\n--- Menganalisis Data Jamur Melalui Pohon Keputusan ---")
    
    tree = model.tree_
    node_id = 0
    langkah = 1

    while tree.children_left[node_id] != tree.children_right[node_id]:
        feature_index = tree.feature[node_id]
        feature_name = X.columns[feature_index]
        threshold = tree.threshold[node_id]
        user_value = jamur_fitur_encoded[feature_name].iloc[0]
        nilai_asli_fitur = jamur_asli[feature_name]

        print(f"Langkah {langkah}: Berada di Node #{node_id}")
        print(f"   -> Pertanyaan Model: Apakah '{feature_name}' <= {threshold:.2f}?")
        print(f"   -> Ciri Jamur Anda: '{feature_name}' adalah '{nilai_asli_fitur}' (nilai-encode: {user_value}).")
        if user_value <= threshold:
            print(f"   -> Nilai jamur ('{feature_name}' = {user_value}) memenuhi syarat. Pindah ke kiri.")
            node_id = tree.children_left[node_id]
        else:
            print(f"   -> Nilai jamur ('{feature_name}' = {user_value}) tidak memenuhi syarat. Pindah ke kanan.")
            node_id = tree.children_right[node_id]
        
        langkah += 1
        print("-" * 20)
    
    print(f"Langkah {langkah}: Mencapai Daun (Leaf Node) #{node_id}")
    prediksi_index = np.argmax(tree.value[node_id])
    hasil_akhir = nama_kelas[prediksi_index]
    
    print("\n--- Hasil Prediksi Model ---")
    print(f"Berdasarkan analisis, model memprediksi jamur ini sebagai: '{hasil_akhir}'")

    if prediksi_index == jawaban_asli_encoded:
        print("\n>>> KESIMPULAN: Prediksi Model BENAR! <<<")
    else:
        print("\n>>> KESIMPULAN: Prediksi Model SALAH! <<<")


# --- Menjalankan Program Utama ---
if __name__ == "__main__":
    analisis_satu_jamur(model, X_test, y_test, df_asli, label_encoders)