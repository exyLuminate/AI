def forward_chaining(rules, facts):
    inferred_facts = set(facts)
    inferred_in_this_pass = True
    while inferred_in_this_pass:
        inferred_in_this_pass = False
        for rule in rules:
            premises = rule['if']
            conclusion = rule['then']
            if conclusion in inferred_facts:
                continue
            if all(premise in inferred_facts for premise in premises):
                print(f"-> Aturan Cocok: JIKA {premises} MAKA {conclusion}")
                print(f"   -> Fakta Baru Ditemukan: {conclusion}\n")
                inferred_facts.add(conclusion)
                inferred_in_this_pass = True
    return inferred_facts

def display_results(final_facts):
   
    print("\n\n--- Hasil Akhir Konsultasi ---")
    diagnosis = [fact[1].replace("_", " ").title() for fact in final_facts if fact[0] == 'diagnosis']
    tindakan = [fact[1].replace("_", " ").title() for fact in final_facts if fact[0] == 'tindakan']
    saran = [fact[1].replace("_", " ").title() for fact in final_facts if fact[0] == 'saran']

    if diagnosis:
        print(f"\nDiagnosis Sistem: {', '.join(diagnosis)}")
    else:
        print("\nDiagnosis Sistem: Tidak ada diagnosis spesifik yang dapat disimpulkan.")
    if tindakan:
        print(f"Rekomendasi Tindakan: {', '.join(tindakan)}")
    else:
        print("Rekomendasi Tindakan: Tidak ada tindakan spesifik.")
    if saran:
        print(f"Saran Tambahan: {', '.join(saran)}")
    else:
        print("Saran Tambahan: Tidak ada saran tambahan.")

def get_user_facts_dinamis():
   
    print("--- Konsultasi Sistem Pakar Medis ---")
    print("Silakan jawab pertanyaan berikut dengan 'y' (ya) atau 'n' (tidak).")
    
    initial_facts = []

    def tanya(pertanyaan):
        while True:
            answer = input(f"{pertanyaan} (y/n): ").lower()
            if answer in ['y', 'n']:
                return answer == 'y'
            print("Input tidak valid. Harap jawab dengan 'y' atau 'n'.")

    if tanya("Apakah pasien seorang dewasa (17+ tahun)?"):
        initial_facts.append(('profil', 'pasien_dewasa'))
    else:
        initial_facts.append(('profil', 'pasien_anak'))

    if tanya("Apakah pasien mengalami demam?"):
        initial_facts.append(('gejala', 'demam'))
        if tanya("Apakah demamnya tergolong tinggi (di atas 38.5°C)?"):
            initial_facts.append(('gejala', 'demam_tinggi'))
    if tanya("Apakah pasien mengalami batuk?"):
        initial_facts.append(('gejala', 'batuk'))
        if tanya("Apakah batuknya tidak berdahak (kering)?"):
            initial_facts.append(('gejala', 'batuk_kering'))
    if tanya("Apakah pasien mengalami sakit kepala?"):
        initial_facts.append(('gejala', 'sakit_kepala'))
    if tanya("Apakah pasien mengalami nyeri pada tubuh/persendian?"):
        initial_facts.append(('gejala', 'nyeri_tubuh'))
    if tanya("Apakah pasien mengalami sesak napas atau kesulitan bernapas?"):
        initial_facts.append(('gejala', 'sesak_napas'))
            
    return initial_facts

# Basis Pengetahuan (Knowledge Base)
knowledge_base = [
    # Level 0: Aturan Umum
    {'if': [('gejala', 'demam_tinggi')], 'then': ('saran', 'segera_konsultasi_medis')},
    {'if': [('gejala', 'demam')], 'then': ('saran', 'minum_banyak_air')},
    {'if': [('gejala', 'sakit_kepala')], 'then': ('saran', 'pertimbangkan_minum_pereda_nyeri')},
    # Level 1: Gejala -> Indikasi Awal
    {'if': [('gejala', 'demam'), ('gejala', 'nyeri_tubuh')], 'then': ('indikasi', 'infeksi_virus_umum')},
    {'if': [('gejala', 'demam'), ('gejala', 'sakit_kepala')], 'then': ('indikasi', 'infeksi_virus_umum')},
    {'if': [('gejala', 'batuk'), ('gejala', 'sesak_napas')], 'then': ('indikasi', 'masalah_paru_bawah')},
    # Level 2: Indikasi -> Diagnosis
    {'if': [('indikasi', 'infeksi_virus_umum'), ('gejala', 'batuk_kering')], 'then': ('diagnosis', 'kemungkinan_flu_biasa')},
    {'if': [('indikasi', 'infeksi_virus_umum'), ('indikasi', 'masalah_paru_bawah')], 'then': ('diagnosis', 'kemungkinan_bronkitis_akut')},
    {'if': [('indikasi', 'infeksi_virus_umum'), ('indikasi', 'masalah_paru_bawah'), ('gejala', 'demam_tinggi')], 'then': ('diagnosis', 'kemungkinan_pneumonia')},
    # Level 3: Diagnosis -> Tindakan
    {'if': [('diagnosis', 'kemungkinan_flu_biasa')], 'then': ('tindakan', 'perawatan_mandiri')},
    {'if': [('diagnosis', 'kemungkinan_bronkitis_akut')], 'then': ('tindakan', 'konsultasi_dokter_jika_gejala_bertahan')},
    {'if': [('diagnosis', 'kemungkinan_pneumonia'), ('profil', 'pasien_dewasa')], 'then': ('tindakan', 'rujuk_spesialis_paru')},
    {'if': [('diagnosis', 'kemungkinan_pneumonia'), ('profil', 'pasien_dewasa')], 'then': ('tindakan', 'resep_antibiotik')},
    {'if': [('diagnosis', 'kemungkinan_pneumonia'), ('profil', 'pasien_anak')], 'then': ('tindakan', 'bawa_segera_ke_UGD')},
    # Level 4: Tindakan -> Saran Tambahan
    {'if': [('tindakan', 'perawatan_mandiri')], 'then': ('saran', 'istirahat_dan_minum_air')},
    {'if': [('tindakan', 'konsultasi_dokter_jika_gejala_bertahan')], 'then': ('saran', 'hindari_iritan_seperti_asap_rokok')},
    {'if': [('tindakan', 'resep_antibiotik')], 'then': ('saran', 'habiskan_obat_sesuai_resep')},
    {'if': [('tindakan', 'bawa_segera_ke_UGD')], 'then': ('saran', 'pantau_tanda_vital_selama_perjalanan')}
]

# Menjalankan Program Utama
if __name__ == "__main__":
    user_facts = get_user_facts_dinamis()
    print("\nFakta awal yang terkumpul dari pengguna:")
    print(sorted(user_facts))
    print("\n--- Memulai Proses Penalaran ---")
    final_facts = forward_chaining(knowledge_base, user_facts)
    display_results(final_facts)