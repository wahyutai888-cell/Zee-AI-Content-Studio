import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from PIL import Image

# --- 1. KONFIGURASI HALAMAN (Wajib Paling Atas) ---
st.set_page_config(page_title="Zee AI Studio", layout="wide", page_icon="✨")

# --- 1. KONFIGURASI API KEY (AMANKAN!) ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "" # Kosongkan saja untuk keamanan di GitHub
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        # Sidebar sukses dipindah ke dalam pengecekan
        st.sidebar.success("Koneksi Aman & Stabil ✅")
    except Exception as e:
        st.error(f"Gagal inisialisasi AI: {e}")
# --- 3. DESAIN UI AESTHETIC (CUSTOM CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Body & Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        font-family: 'Poppins', sans-serif;
        color: #e2e8f0;
    }

    /* Modern Glassmorphism Card (Untuk Hasil Teks) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border-left: 4px solid #3b82f6;
    }

    /* Custom Header Aesthetic */
    .main-title {
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    /* Stylish Button with Hover Effect */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        color: white;
    }

    /* Input & Text Area Modern */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* Sidebar Aesthetic */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Tab Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #94a3b8;
        padding: 0 30px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
        color: #60a5fa !important;
        border: 1px solid #3b82f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MANAJEMEN MEMORI (SESSION STATE) ---
if "hasil_caption" not in st.session_state:
    st.session_state.hasil_caption = ""

# --- 5. TAMPILAN UTAMA ---
st.markdown('<h1 class="main-title">Zee AI Content Studio</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 40px;">Sistem Generator Naskah Affiliate & Visual Analysis Terintegrasi.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Script Generator", "👁️ Vision Analysis"])

# --- MODUL 1: SCRIPT AFFILIATE (Layout 2 Kolom) ---
with tab1:
    col_kiri, col_kanan = st.columns([1, 1.2], gap="large")
    
    with col_kiri:
        st.markdown("### 📝 Input Produk")
        prod_info = st.text_area("Detail/Link Produk:", placeholder="Contoh: Sepatu lari Nike Air Max, bahan breathable...", height=150)
        
        c1, c2 = st.columns(2)
        with c1:
            gaya = st.selectbox("Gaya Bahasa:", ["Persuasif/Mengajak", "Review Jujur", "Hard Sell", "Storytelling"])
        with c2:
            panjang = st.select_slider("Panjang Teks:", options=["Singkat", "Menengah", "Panjang"])
        
        if st.button("🚀 Craft My Caption"):
            if not prod_info:
                st.warning("Mohon masukkan detail produk terlebih dahulu!")
            else:
                with st.spinner("AI sedang meracik naskah..."):
                    try:
                        prompt = f"""
                        Tugasmu adalah membuat SATU CAPTION MEDIA SOSIAL (Instagram/TikTok/WhatsApp) untuk produk affiliate.

                        DETAIL PRODUK: {prod_info}
                        GAYA BAHASA: {gaya}
                        PANJANG: {panjang}

                        INSTRUKSI KHUSUS (WAJIB DIIKUTI):
                        1. JANGAN memberikan kalimat pembuka atau penutup tambahan.
                        2. JANGAN menggunakan label naskah seperti (Opening), (Hook), atau (Closing).
                        3. LANGSUNG berikan teks caption yang siap copy-paste.
                        4. Gunakan Headline yang "hooking" (menangkap perhatian).
                        5. Gunakan poin-poin dengan emoji untuk menjelaskan keunggulan.
                        6. PENTING: Di bagian Call to Action (CTA), WAJIB TULISKAN KEMBALI LINK PRODUK secara persis seperti yang ada di 'DETAIL PRODUK'. JANGAN gunakan placeholder seperti '[Link Produk]'.
                        7. Berikan 5-7 hashtag relevan di paling bawah.
                        """
                        response = model.generate_content(prompt)
                        st.session_state.hasil_caption = response.text
                    except Exception as e:
                        st.error(f"Terjadi kesalahan pada server AI: {e}")

    with col_kanan:
        st.markdown("### 💎 Hasil Naskah AI")
        if st.session_state.hasil_caption:
            # Tampilan Glassmorphism untuk hasil teks
            st.markdown(f'<div class="glass-card">{st.session_state.hasil_caption}</div>', unsafe_allow_html=True)
            
            st.write("") # Spasi
            
            # Fitur Ekspor ke Word
            doc = Document()
            doc.add_heading('Script Affiliate by Zee AI', 0)
            doc.add_paragraph(f"Produk: {prod_info}")
            doc.add_paragraph(f"Gaya: {gaya}")
            doc.add_paragraph("-" * 20)
            doc.add_paragraph(st.session_state.hasil_caption)
            
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.download_button(
                label="📥 Download to Word (.docx)",
                data=buffer,
                file_name="script_affiliate_zee.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.info("Naskah estetikmu akan muncul di sini setelah AI selesai memproses.")

# --- MODUL 2: AI VISION STUDIO ---
with tab2:
    st.markdown("### 👁️ AI Vision Studio")
    st.write("Unggah foto produk untuk dianalisis oleh AI.")
    
    uploaded_file = st.file_uploader("Pilih Foto Produk", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        c_img, c_res = st.columns([1, 1.5], gap="medium")
        with c_img:
            img = Image.open(uploaded_file)
            st.image(img, use_container_width=True, caption="Foto Produk Terunggah")
        
        with c_res:
            instruksi = st.text_input("Instruksi untuk AI:", "Berikan deskripsi produk yang estetik dan list fitur yang terlihat di foto ini.")
            
            if st.button("🔍 Analisis Visual dengan AI"):
                with st.spinner("Vision AI sedang melihat foto..."):
                    try:
                        response = model.generate_content([instruksi, img])
                        st.success("Analisis Selesai!")
                        st.markdown(f'<div class="glass-card">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Gagal memproses gambar: {e}")

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #60a5fa;'>🛡️ Zee Admin Panel</h2>", unsafe_allow_html=True)
    
    if API_KEY:
        st.success("Sistem API: Online 🟢")
    else:
        st.error("Sistem API: Offline 🔴")
    
    st.divider()
    st.write("🔍 **System Diagnostics**")
    if st.button("Cek Daftar Model"):
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.code(models)
        except Exception as e:
            st.error(f"Gagal: {e}")
            
    st.divider()
    st.caption("© 2026 Skripsi Zee - Sistem Aplikasi Generator Konten Terintegrasi v3.0 (Aesthetic Edition)")
