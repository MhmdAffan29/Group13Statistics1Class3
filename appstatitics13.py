import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from fpdf import FPDF
import tempfile
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Statistical Analysis App",
    page_icon="📊",
    layout="wide"
)

# Set Seaborn Style (Earth Tone Palette for Charts)
sns.set_theme(style="whitegrid")
EARTH_PALETTE = sns.color_palette("BrBG", 10) # Brown-Blue-Green Earthy tones

# ==========================================
# 1. KAMUS BAHASA (TRANSLATION DICTIONARY)
# ==========================================
translations = {
    "en": {
        "nav_title": "Navigation",
        "nav_options": ["Home", "Data Analysis Tools", "Team Members"],
        "lang_label": "Language / Bahasa",
        
        # Home Page
        "home_title": "Automated Statistical Analysis",
        "home_overview_title": "🎓 Project Overview",
        "home_desc": """
Welcome to our Statistical Analysis Web Application! This project demonstrates fundamental concepts 
of **Descriptive Statistics** and **Association Analysis**.

We utilize Python libraries (Pandas, Scipy, Seaborn) to process data, calculate statistics, and visualize relationships automatically.
""",
        "home_sec1": "1. Descriptive Statistics",
        "home_sec1_desc": "Summarizing data using measures of central tendency and dispersion.",
        "home_sec1_note": "Includes: Mean, Median, Mode, Standard Deviation, and Frequency Tables.",
        "home_sec2": "2. Association Analysis",
        "home_sec2_desc": "Determining relationships between two variables (X and Y).",
        "home_sec2_note": "Methods: Pearson (Numeric-Normal), Spearman (Numeric-NonNormal), Chi-Square (Categorical).",
        "home_info": "👈 Navigate to 'Data Analysis Tools' to start analyzing your data!",

        # Tools Page
        "tools_title": "🛠️ Data Analysis Tools",
        "upload_header": "1. Upload Dataset",
        "upload_label": "Upload CSV or Excel file",
        "preview_header": "Data Preview",
        "setup_header": "2. Variable Setup",
        "desc_header": "Descriptive Statistics",
        "assoc_header": "Association Analysis",
        "select_vars": "Select Variables for Analysis",
        "var_x": "Select Variable X (Independent)",
        "var_y": "Select Variable Y (Dependent)",
        "calc_composites": "Calculate Composite Scores (Summation)",
        "select_items_x": "Items for Composite X",
        "select_items_y": "Items for Composite Y",
        "generate_btn": "Run Analysis",
        "export_btn": "Export to PDF",
        "warn_upload": "Please upload a dataset via the tool to begin.",
        "dataset_info": "Dataset Info",
        "success_composite": "Composite scores calculated successfully!",
        
        # Stats Results
        "mean": "Mean",
        "median": "Median",
        "mode": "Mode",
        "min": "Min",
        "max": "Max",
        "std": "Std Dev",
        "freq_table": "Frequency Table",
        "auto_method": "Method Automatically Selected",
        "pearson_desc": "Both variables are Numeric and Normally Distributed.",
        "spearman_desc": "Variables are Numeric but NOT Normally Distributed.",
        "chisquare_desc": "Both variables are Categorical.",
        "interp": "Interpretation",
        "result_summary": "Result Summary",

        # Team Page
        "team_title": "👥 The Team",
        "team_intro": "Meet the team behind this statistical application.",
        "role_label": "Role:",
        "about_title": "💡 How We Built This",
        "about_desc": """
**Team Contribution Summary:**
We collaborated to build a robust tool that simplifies statistical analysis. 
The work was divided into **Data Processing Logic**, **Statistical Algorithms**, **User Interface**, and **Reporting System**.
"""
    },
    "id": {
        "nav_title": "Navigasi",
        "nav_options": ["Beranda", "Alat Analisis Data", "Anggota Tim"],
        "lang_label": "Language / Bahasa",

        # Home Page
        "home_title": "Analisis Statistik Otomatis",
        "home_overview_title": "🎓 Ringkasan Proyek",
        "home_desc": """
Selamat datang di Aplikasi Web Analisis Statistik kami! Proyek ini mendemonstrasikan konsep dasar 
dari **Statistik Deskriptif** dan **Analisis Asosiasi**.

Kami menggunakan pustaka Python (Pandas, Scipy, Seaborn) untuk memproses data, menghitung statistik, dan memvisualisasikan hubungan secara otomatis.
""",
        "home_sec1": "1. Statistik Deskriptif",
        "home_sec1_desc": "Meringkas data menggunakan ukuran pemusatan dan penyebaran.",
        "home_sec1_note": "Meliputi: Mean, Median, Modus, Standar Deviasi, dan Tabel Frekuensi.",
        "home_sec2": "2. Analisis Asosiasi",
        "home_sec2_desc": "Menentukan hubungan antara dua variabel (X dan Y).",
        "home_sec2_note": "Metode: Pearson (Numerik-Normal), Spearman (Numerik-Tidak Normal), Chi-Square (Kategorikal).",
        "home_info": "👈 Buka 'Alat Analisis Data' untuk mulai menganalisis data Anda!",

        # Tools Page
        "tools_title": "🛠️ Alat Analisis Data",
        "upload_header": "1. Unggah Dataset",
        "upload_label": "Unggah file CSV atau Excel",
        "preview_header": "Pratinjau Data",
        "setup_header": "2. Pengaturan Variabel",
        "desc_header": "Statistik Deskriptif",
        "assoc_header": "Analisis Asosiasi",
        "select_vars": "Pilih Variabel untuk Analisis",
        "var_x": "Pilih Variabel X (Independen)",
        "var_y": "Pilih Variabel Y (Dependen)",
        "calc_composites": "Hitung Skor Komposit (Penjumlahan)",
        "select_items_x": "Item untuk Komposit X",
        "select_items_y": "Item untuk Komposit Y",
        "generate_btn": "Mulai Analisis",
        "export_btn": "Ekspor ke PDF",
        "warn_upload": "Silakan unggah dataset melalui alat ini untuk memulai.",
        "dataset_info": "Info Dataset",
        "success_composite": "Skor komposit berhasil dihitung!",
        
        # Stats Results
        "mean": "Rata-rata (Mean)",
        "median": "Median",
        "mode": "Modus",
        "min": "Min",
        "max": "Maks",
        "std": "Simpangan Baku",
        "freq_table": "Tabel Frekuensi",
        "auto_method": "Metode Dipilih Otomatis",
        "pearson_desc": "Kedua variabel Numerik dan Berdistribusi Normal.",
        "spearman_desc": "Variabel Numerik tetapi TIDAK Berdistribusi Normal.",
        "chisquare_desc": "Kedua variabel Kategorikal.",
        "interp": "Interpretasi",
        "result_summary": "Ringkasan Hasil",

        # Team Page
        "team_title": "👥 Anggota Tim",
        "team_intro": "Kenalan dengan tim di balik aplikasi statistik ini.",
        "role_label": "Peran:",
        "about_title": "💡 Bagaimana Kami Membuat Ini",
        "about_desc": """
**Ringkasan Kontribusi Tim:**
Kami bekerja sama membangun alat yang menyederhanakan analisis statistik. 
Pekerjaan dibagi menjadi **Logika Pemrosesan Data**, **Algoritma Statistik**, **Antarmuka Pengguna**, dan **Sistem Pelaporan**.
"""
    }
}

# --- Sidebar Language Selector ---
st.sidebar.title("Settings / Pengaturan")
lang_choice = st.sidebar.radio("Language / Bahasa", ["English", "Bahasa Indonesia"])
lang = "en" if lang_choice == "English" else "id"
t = translations[lang]

# ==========================================
# 2. HELPER FUNCTIONS (LOGIC)
# ==========================================

def get_descriptive_stats(df, column):
    """Calculates descriptive stats for a numerical column."""
    desc = df[column].describe()
    mode = df[column].mode()[0] if not df[column].mode().empty else np.nan
    return {
        "Mean": desc['mean'],
        "Median": desc['50%'],
        "Mode": mode,
        "Min": desc['min'],
        "Max": desc['max'],
        "Std": desc['std']
    }

def check_normality(data):
    """Performs Shapiro-Wilk test. Returns True if Normal, False otherwise."""
    data = data.dropna()
    if len(data) < 3: return False, 0
    stat, p_value = stats.shapiro(data)
    return p_value > 0.05, p_value

def interpret_correlation(r, p):
    """Returns text interpretation of correlation r and p-value."""
    strength = ""
    abs_r = abs(r)
    if abs_r < 0.3: strength = "Weak/Lemah"
    elif abs_r < 0.7: strength = "Moderate/Sedang"
    else: strength = "Strong/Kuat"
    
    direction = "Positive (+)" if r > 0 else "Negative (-)"
    significance = "Significant/Signifikan (p<0.05)" if p < 0.05 else "Not Significant/Tidak Signifikan"
    
    return strength, direction, significance

def analyze_association_logic(df, col_x, col_y):
    """Automatically selects method and computes stats."""
    clean_df = df[[col_x, col_y]].dropna()
    x = clean_df[col_x]
    y = clean_df[col_y]
    
    if len(x) == 0:
        return "Error", {"Error": "No valid data"}, None

    is_x_numeric = pd.api.types.is_numeric_dtype(x)
    is_y_numeric = pd.api.types.is_numeric_dtype(y)
    
    method = "Unknown"
    res = {}
    fig = None

    if is_x_numeric and is_y_numeric:
        norm_x, p_x = check_normality(x)
        norm_y, p_y = check_normality(y)
        
        if norm_x and norm_y:
            method = "Pearson Correlation"
            r, p = stats.pearsonr(x, y)
        else:
            method = "Spearman Rank Correlation"
            r, p = stats.spearmanr(x, y)
            
        strength, direction, sig = interpret_correlation(r, p)
        res = {
            "Coefficient (r)": f"{r:.4f}",
            "p-value": f"{p:.4f}",
            "Normality X (p)": f"{p_x:.4f}",
            "Normality Y (p)": f"{p_y:.4f}",
            "Interpretation": f"{strength}, {direction}, {sig}"
        }
        
        # Scatterplot with Earth Tones
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(x=x, y=y, ax=ax, color='#8c564b', s=80, alpha=0.8) # Chestnut Brown
        if method == "Pearson Correlation":
            sns.regplot(x=x, y=y, ax=ax, scatter=False, color='#556B2F') # Olive Green
        ax.set_title(f"Scatterplot: {col_x} vs {col_y}")
        plt.tight_layout()
        
    elif not is_x_numeric and not is_y_numeric:
        method = "Chi-Square Test"
        contingency = pd.crosstab(x, y)
        stat, p, dof, expected = stats.chi2_contingency(contingency)
        
        res = {
            "Chi2 Stat": f"{stat:.4f}",
            "p-value": f"{p:.4f}",
            "Result": "Significant" if p < 0.05 else "Not Significant"
        }
        
        # Heatmap with Earth Tones
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(contingency, annot=True, fmt='d', cmap="BrBG", ax=ax, linewidths=1)
        ax.set_title(f"Heatmap: {col_x} vs {col_y}")
        plt.tight_layout()
        
    else:
        method = "Mixed Types (Not Supported)"
        res = {"Error": "Please select two numeric or two categorical variables."}
        
    return method, res, fig

# ==========================================
# 3. PDF CLASS
# ==========================================
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Statistical Analysis Report', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        try: safe_body = body.encode('latin-1', 'replace').decode('latin-1')
        except: safe_body = body
        self.multi_cell(0, 5, safe_body)
        self.ln()

# ==========================================
# NAVIGATION
# ==========================================
st.sidebar.markdown("---")
st.sidebar.title(t["nav_title"])
page = st.sidebar.radio("Go to", t["nav_options"])

# ==========================================
# PAGE 1: HOME
# ==========================================
if page == t["nav_options"][0]: # Home
    st.title(t["home_title"])
    st.markdown(f"### {t['home_overview_title']}")
    st.write(t["home_desc"])
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.header(t["home_sec1"])
        st.write(t["home_sec1_desc"])
        st.info(t["home_sec1_note"])
        
    with col2:
        st.header(t["home_sec2"])
        st.write(t["home_sec2_desc"])
        st.warning(t["home_sec2_note"])
        
    st.success(t["home_info"])

# ==========================================
# PAGE 2: ANALYSIS TOOLS
# ==========================================
elif page == t["nav_options"][1]: # Tools
    st.title(t["tools_title"])
    
    # --- Step 1: Upload ---
    st.header(t["upload_header"])
    uploaded_file = st.file_uploader(t["upload_label"], type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

        with st.expander(t["preview_header"], expanded=True):
            st.dataframe(df.head(), use_container_width=True)
            st.caption(f"{t['dataset_info']}: {df.shape[0]} rows, {df.shape[1]} columns")

        st.markdown("---")
        
        # --- Step 2: Setup ---
        st.header(t["setup_header"])
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.subheader(t["calc_composites"])
            cols_num = df.select_dtypes(include=np.number).columns.tolist()
            items_x = st.multiselect(t["select_items_x"], cols_num)
            items_y = st.multiselect(t["select_items_y"], cols_num)
            
            if items_x: df['X_Total'] = df[items_x].sum(axis=1)
            if items_y: df['Y_Total'] = df[items_y].sum(axis=1)
            if items_x or items_y: st.success(t["success_composite"])
            
        with col_s2:
            st.subheader(t["select_vars"])
            all_cols = df.columns.tolist()
            ix_x = all_cols.index('X_Total') if 'X_Total' in all_cols else 0
            ix_y = all_cols.index('Y_Total') if 'Y_Total' in all_cols else (1 if len(all_cols) > 1 else 0)
            
            col_x = st.selectbox(t["var_x"], all_cols, index=ix_x)
            col_y = st.selectbox(t["var_y"], all_cols, index=ix_y)

        # --- Step 3: Action ---
        st.markdown("---")
        if st.button(t["generate_btn"], type="primary"):
            
            report_content = []
            
            # --- Analysis A: Descriptive ---
            st.header(t["desc_header"])
            report_content.append(("header", t["desc_header"]))
            
            for col in list(set([col_x, col_y])):
                st.subheader(f"Variable: {col}")
                report_content.append(("subheader", f"Variable: {col}"))
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    stats_dict = get_descriptive_stats(df, col)
                    st.table(pd.DataFrame(stats_dict, index=[0]))
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        fig1, ax1 = plt.subplots(figsize=(6,4))
                        sns.histplot(df[col], kde=True, ax=ax1, color='#8c564b') # Brown
                        ax1.set_title(f"Histogram: {col}")
                        st.pyplot(fig1)
                        report_content.append(("plot", fig1))
                    with c2:
                        fig2, ax2 = plt.subplots(figsize=(6,4))
                        sns.boxplot(x=df[col], ax=ax2, color='#d9c0a3') # Beige
                        ax2.set_title(f"Boxplot: {col}")
                        st.pyplot(fig2)
                        report_content.append(("plot", fig2))
                        
                    stats_str = ", ".join([f"{k}: {v:.2f}" for k,v in stats_dict.items()])
                    report_content.append(("text", stats_str))
                
                else:
                    freq = df[col].value_counts().reset_index()
                    freq.columns = ['Category', 'Frequency']
                    st.table(freq.head())
                    
                    fig3, ax3 = plt.subplots(figsize=(6,4))
                    sns.barplot(data=freq, x='Category', y='Frequency', ax=ax3, palette="BrBG")
                    ax3.set_title(f"Frequency: {col}")
                    st.pyplot(fig3)
                    report_content.append(("plot", fig3))
                    report_content.append(("text", f"Categorical: {col}"))

            st.markdown("---")
            
            # --- Analysis B: Association ---
            st.header(t["assoc_header"])
            report_content.append(("header", t["assoc_header"]))
            
            method, res, fig_assoc = analyze_association_logic(df, col_x, col_y)
            
            st.info(f"**{t['auto_method']}:** {method}")
            report_content.append(("subheader", f"Method: {method}"))
            
            c_res, c_plot = st.columns([1, 2])
            with c_res:
                st.subheader(t["result_summary"])
                st.json(res)
                res_str = "\n".join([f"{k}: {v}" for k,v in res.items()])
                report_content.append(("text", res_str))
            
            with c_plot:
                if fig_assoc:
                    st.pyplot(fig_assoc)
                    report_content.append(("plot", fig_assoc))
                elif "Error" in res:
                    st.error(res["Error"])

            # --- PDF Generation ---
            st.markdown("---")
            pdf = PDFReport()
            pdf.add_page()
            
            try:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    for item_type, content in report_content:
                        if item_type == "header": pdf.chapter_title(content)
                        elif item_type == "subheader": 
                            pdf.set_font('Arial', 'B', 11)
                            pdf.cell(0, 10, content.encode('latin-1','replace').decode('latin-1'), 0, 1)
                        elif item_type == "text": pdf.chapter_body(content)
                        elif item_type == "plot":
                            fname = os.path.join(tmpdirname, f"p_{np.random.randint(100000)}.png")
                            content.savefig(fname, bbox_inches='tight', dpi=100)
                            if pdf.get_y() > 200: pdf.add_page()
                            pdf.image(fname, w=150)
                            pdf.ln(10)
                    
                    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'replace')
                    st.download_button(t["export_btn"], pdf_bytes, "Analysis_Report.pdf", "application/pdf")
            except Exception as e:
                st.error(f"PDF Error: {e}")
                
    else:
        st.warning(t["warn_upload"])

# ==========================================
# PAGE 3: TEAM
# ==========================================
elif page == t["nav_options"][2]: # Team
    st.title(t["team_title"])
    st.write(t["team_intro"])
    st.markdown("---")
    
    def display_member(name, role, description, img_source):
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                # Cek apakah file foto ada di folder
                if os.path.exists(img_source):
                    st.image(img_source, width=150, caption=name)
                else:
                    # Tampilkan placeholder/error jika foto tidak ditemukan
                    st.warning(f"Foto tidak ditemukan: {img_source}")
                    st.image("https://via.placeholder.com/150", width=150)
            
            with col2:
                st.subheader(name)
                st.markdown(f"**{t['role_label']}** {role}")
                st.write(description)
            st.markdown("---")
            
    # --- DAFTAR ANGGOTA TIM (Edit di sini) ---
    # Format: ("Nama", "Peran", "Deskripsi", "nama_file_foto.jpg")
    members = [
        ("Hamzah Sholehudin Yusuf", "Project Manager", "Mengkoordinasikan timeline proyek.", "hamzah.jpg"),
        ("Muhammad Affan Rasyidin", "UI/UX Designer", "Mendesain tata letak Streamlit.", "affan.jpg"),
        ("Muhammad Darrel Yashaq", "Researcher", "Menyusun metodologi penelitian.", "darrel.jpg"),
        ("Muhammad Emil Lutfi", "Data Analyst", "Bertanggung jawab atas logika statistik.", "emil.jpg")
    ]
    
    for m in members:
        display_member(m[0], m[1], m[2], m[3])
        
    st.header(t["about_title"])
    st.info(t["about_desc"])