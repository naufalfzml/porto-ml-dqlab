import streamlit as st
import pandas as pd
import pickle
import time
from PIL import Image

st.set_page_config(page_title="Cardio Care+",
                   layout="wide")

st.markdown("""
    <div style="text-align: center;">
        <h1>Cardio Care+ : Aplikasi Prediksi Penyakit Jantung</h1>
        <p>Created by: Fawwaz Naufal Maulana</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        <img src="https://awsimages.detik.net.id/visual/2020/08/05/ilustrasi-sakit-jantung-akibat-tersumbat-pembuluh-darah-istockphotowildpixel_169.jpeg?w=650" alt="Gambar Jantung" style="width: 400px;">
        <br> </br>
    </div>
""", unsafe_allow_html=True)


sex_labels = {
    0: "Perempuan",
    1: "Laki - laki"}
integer_labels = {
    0: "Tidak",
    1: "Ya"
}

slope_labels = {
    0: "Meningkat",
    1: "Datar",
    2: "Menurun"
}

cp_labels = {
    1: "Typical Angina",
    2: "Atypical Angina",
    3: "Non-anginal Pain",
    4: "Asimptomatik"
}
thal_labels = {
    1: "Normal",
    2: "Defek Tetap",
    3: "Defek Reversibel"
}

with st.expander("Tentang Cardio Care+"):
            st.write("""Aplikasi ini dibuat untuk mendeteksi risiko penyakit jantung dengan menggunakan model prediksi berbasis Machine Learning. 
                     Dengan menganalisis data kesehatan pengguna yang sudah diinputkan, seperti denyut jantung, jenis nyeri dada, dan riwayat kesehatan lainnya. Aplikasi ini akan memprediksi ada atau tidaknya risiko penyakit jantung pada tubuh pengguna.
                    Data diperoleh dari [Heart Disease dataset](https://archive.ics.uci.edu/dataset/45/heart+disease) by UCIML. 
""")
            
with st.expander("Penjelasan Feature"):
    st.markdown("""
    **1. Jenis Nyeri Dada yang Pernah Anda Alami (cp):**
    - **Typical Angina**    : Nyeri dada karena kekurangan aliran darah ke jantung.
    - **Atypical Angina**   : Nyeri dada yang gejalanya tidak memenuhi kriteria nyeri dada tipikal.
    - **Non-anginal Pain**  : Nyeri dada yang bukan disebabkan oleh penyakit jantung.
    - **Asimptomatik**      : Tidak ada nyeri yang dirasakan.

    **2. Denyut Jantung Maksimum (thalach):**
    - Jumlah maksimum detak jantung saat olahraga.
                
    **3. Segmen ST pada EKG Selama Aktivitas Fisik (slope):**
    - Meningkat : Kemiringan segmen ST meningkat setelah aktivitas fisik.
    - Datar     : Kemiringan segmen ST tetap datar setelah aktivitas fisik.
    - Menurun   : Kemiringan segmen ST menurun setelah aktivitas fisik.
                
    **4. Depresi ST Saat Melakukan Aktivitas Fisik (oldpeak):**
    - Penurunan segmen ST selama aktivitas menunjukkan masalah dengan aliran darah.
                
    **5. Nyeri Dada Ketika Melakukan Aktivitas Fisik (exang):**
    - Tidak     : Tidak mengalami nyeri dada selama aktivitas fisik.
    - Ya        : Mengalami nyeri dada selama aktivitas fisik.
                
    **6. Jumlah Pembuluh Darah Utama(ca):**
    - Jumlah pembuluh darah utama yang terlihat dalam sinar-X dengan kontras.
                
    **7. Hasil Tes Thalium (thal):**
    - Normal            : Hasil tes normal.
    - Defek Tetap       : Defek Thalassemia tetap.
    - Defek Reversibel  : Defek Thalassemia yang dapat kembali normal.

    **8. Jenis Kelamin (sex):**      
    - Perempuan     : Jenis kelamin perempuan.
    - Laki - laki   : Jenis kelamin laki - laki.
    
    **9. Usia (age):**
    - Usia dalam tahun.
    """)

st.header('User Input Features:')
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file is not None:
     input_df = pd.read_csv(uploaded_file)
else:  
    def user_input_features():
        st.header("Input Manual")
        cp = st.selectbox("Jenis Nyeri Dada yang Pernah Anda Alami:", 
                        options=list(cp_labels.keys()), format_func=lambda x: f" {cp_labels[x]}")
        thalach = st.slider("Denyut Jantung Maksimum (per menit)?", 
                            min_value=71, max_value=202, value=137)
        slope = st.radio("Segmen ST pada Elektrodiagram (EKG) Selama Aktivitas Fisik: ", 
                            options=list(slope_labels.keys()), format_func=lambda x: f" {slope_labels[x]}")
        oldpeak = st.slider("Depresi ST Saat Melakukan Aktivitas Fisik (dalam mm):", 
                                min_value=0.0, max_value=6.2, value=1.0)
        exang = st.radio("Apakah Anda Pernah Mengalami Nyeri Dada (Angina) Ketika Melakukan Aktivitas Fisik?", 
                            options=list(integer_labels.keys()), format_func=lambda x: f" {integer_labels[x]}")
        ca = st.selectbox("Jumlah Pembuluh Darah Utama:", 
                            options=(0, 1, 2, 3))
        thal = st.radio("Hasil Tes Thalium: ", 
                            options=list(thal_labels.keys()), format_func=lambda x: f" {thal_labels[x]}")
        sex = st.selectbox("Pilih jenis kelamin Anda:", options=list(sex_labels.keys()), format_func=lambda x: f" {sex_labels[x]}")
        age = st.slider("Masukkan usia Anda:", min_value=29, max_value=77, step=1, value=55)

        data = {       
                'cp': cp,
                'thalach': thalach,
                'slope': slope,
                'oldpeak': oldpeak,
                'exang': exang,
                'ca': ca,
                'thal': thal,
                'sex': sex,
                'age': age
                }
        features = pd.DataFrame(data, index=[0])
        return features

input_df = user_input_features()

button_style = """
<style>
div.stButton > button {
    background-color: #28a745;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    border: none;
}
div.stButton > button:hover {
    background-color: #218838;
    color: white;
}
</style>
"""
st.markdown(button_style, unsafe_allow_html=True)


if st.button('Prediksi'):
    df = input_df
    st.write(df)
    with open("model_best.pkl", "rb") as file:
        model = pickle.load(file)
    
    prediction = model.predict(df)
    result = ['Kamu Tidak Terdeteksi Penyakit Jantung!' if prediction == 0 else 'Kamu Terdeteksi Penyakit Jantung']  

    st.subheader("Prediksi: ")
    output = str(result[0])
    with st.spinner('Tunggu sebentar...'):
        time.sleep(3)
        st.success(f"Prediksi: {output}")

st.markdown("""
---
<p style="text-align: center;">
    <a href="https://github.com/naufalfzml" target="_blank" style="text-decoration: none;">
        <img src="https://img.icons8.com/?size=100&id=efFfwotdkiU5&format=png&color=000000" width="30" style="vertical-align: middle;"> GitHub
    </a> &nbsp; | &nbsp;
    <a href="https://www.linkedin.com/in/fawwaz-naufal-maulana-4701792ab/" target="_blank" style="text-decoration: none;">
        <img src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" width="30" style="vertical-align: middle;"> LinkedIn
    </a>
</p>
""", unsafe_allow_html=True)