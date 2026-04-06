import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Zee AI Studio", layout="wide", page_icon="✨")

# --- 2. MANAJEMEN MULTIPLE API KEYS (ANTI-LIMIT) ---
# Mengambil daftar kunci dari Secrets Streamlit Cloud
keys_list = [
    st.secrets.get("GEMINI_KEY_1"), 
    st.secrets.get("GEMINI_KEY_2")
]

# Inisialisasi awal agar tidak 'NameError'
if keys_list[0]:
    genai.configure(api_key=keys_list[0])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ API Key belum terpasang di Secrets!")

# FUNGSI SAKTI UNTUK GENERATE (DENGAN AUTO-SWITCH)
def get_ai_response_safe(prompt_data, is_vision=False):
    for i, key in enumerate(keys_list):
        if not key: continue
        try:
            genai.configure(api_key=key)
            temp_model = genai.GenerativeModel('gemini-1.5-flash')
            
            if is_vision:
                # prompt_data = [instruksi, img]
                response = temp_model.generate_content(prompt_data)
            else:
                # prompt_data = string teks
                response = temp_model.generate_content(prompt_data)
            
            return response.text
        except Exception as e:
            if "429" in str(e) and i < len(keys_list) - 1:
                st.sidebar.warning(f"⚠️ Kunci {i+1} Limit, pindah ke cadangan...")
                continue
            else:
                raise e
    return None

# --- 3. DESAIN UI AESTHETIC ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    .stApp { background: radial-gradient(circle at top right, #1e293b, #0f172a); font-family: 'Poppins', sans-serif; color: #e2e8f0; }
    .glass-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); border-left: 4px solid #3b82f6; }
    .main-title { background: linear-gradient(to right, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; font-size: 3.5rem; text-align: center; }
    .stButton>button { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border-radius: 12px; width: 100%; transition: 0.3s; border: none; padding: 10px; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION STATE ---
if "hasil_caption" not in st.session_state:
    st.session_state.hasil_caption = ""

# --- 5. TAMPILAN UTAMA ---
st.markdown('<h1 class="main-title">Zee AI Content Studio</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #94a3b8;">Sistem Multimodal AI untuk Affiliate Marketing 2026</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Script Generator", "👁️ Vision Analysis"])

with tab1:
    col_kiri, col_kanan = st.columns([1, 1.2], gap="large")
    with col_kiri:
        st.markdown("### 📝 Input Produk")
        prod_info = st.text_area("Detail/Link Produk:", height=150)
        gaya = st.selectbox("Gaya Bahasa:", ["Persuasif", "Review Jujur", "Hard Sell"])
        if st.button("🚀 Craft My Caption"):
            if prod_info:
                with st.spinner("AI sedang meracik naskah..."):
                    try:
                        prompt = f"Buat caption affiliate untuk: {prod_info} dengan gaya {gaya}. Langsung berikan teksnya."
                        st.session_state.hasil_caption = get_ai_response_safe(prompt)
                    except Exception as e:
                        st.error(f"Gagal: {e}")
            else: st.warning("Masukkan detail produk!")

    with col_kanan:
        st.markdown("### 💎 Hasil Naskah AI")
        if st.session_state.hasil_caption:
            st.markdown(f'<div class="glass-card">{st.session_state.hasil_caption}</div>', unsafe_allow_html=True)
            # Bagian Export Word
            doc = Document()
            doc.add_heading('Script Affiliate by Zee', 0)
            doc.add_paragraph(st.session_state.hasil_caption)
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button("📥 Download Word", data=buffer, file_name="script_zee.docx")

with tab2:
    st.markdown("### 👁️ AI Vision Studio")
    uploaded_file = st.file_uploader("Upload Foto Produk", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400)
        instruksi = st.text_input("Instruksi AI:", "Analisis foto ini dan berikan deskripsi marketing.")
        if st.button("🔍 Analisis Visual"):
            with st.spinner("Menganalisis gambar..."):
                try:
                    hasil_v = get_ai_response_safe([instruksi, img], is_vision=True)
                    st.markdown(f'<div class="glass-card">{hasil_v}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Gagal Vision: {e}")

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #60a5fa;'>🛡️ Zee Admin Panel</h2>", unsafe_allow_html=True)
    status = "Online 🟢" if keys_list[0] else "Offline 🔴"
    st.info(f"Status Sistem: {status}")
    
    if st.button("Cek Model Aktif"):
        try:
            # Gunakan genai langsung, bukan variabel model
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.code(models)
        except: st.error("Gagal cek model.")
    st.caption("© 2026 Zee AI Studio v3.2 - Stable Version")