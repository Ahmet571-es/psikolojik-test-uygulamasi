import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
import os

# --- 1. SAYFA KONFİGÜRASYONU VE STİL (PREMIUM UI) ---
st.set_page_config(
    page_title="Balaban Neuro-Psych | Elite Edition",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS: Modern, ferah ve 'Elite' hissettiren tasarım
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    .main-header {
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #1E293B, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    
    .question-card {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        border-left: 6px solid #3B82F6;
        transition: transform 0.2s;
    }
    
    .question-card:hover {
        transform: translateY(-2px);
    }
    
    .report-section {
        background-color: #F8FAFC;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02);
    }
    
    /* Buton Tasarımı */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        font-weight: 600;
        font-size: 1rem;
        background-color: #3B82F6;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #2563EB;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Radyo Butonları */
    div.stRadio > label {
        font-weight: 500;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. API YÖNETİMİ ---
GROK_API_KEY = None

if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        GROK_API_KEY = os.getenv('GROK_API_KEY')
    except:
        pass

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=70)
    st.markdown("### 🧠 Balaban Neuro-Psych")
    st.caption("v4.1 Fast-Reasoning Engine")
    st.markdown("---")
    
    if not GROK_API_KEY:
        st.error("🔴 API Bağlantısı Yok")
        st.stop()
    else:
        st.success("🟢 Neural Link Aktif")
        st.caption("Model: grok-4-1-fast-reasoning")
    
    st.info("""
    **Teknoloji:**
    Bu sistem, psikolojik verileri işlemek için en yeni nesil **Reasoning (Akıl Yürütme)** modelini kullanır. 
    
    **Güvenilirlik:**
    Dinamik soru sayısı algoritması, testin bilimsel geçerliliği için gereken optimal madde sayısını (50-100) anlık hesaplar.
    """)

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# --- 3. TEST VERİTABANI ---
TESTLER = {
    "Big Five (OCEAN)": "Kişiliğin 5 temel boyutunu (Açıklık, Sorumluluk, Dışadönüklük, Uyumluluk, Nevrotiklik) analiz eden altın standart.",
    "MBTI Tipi (Fonksiyonel)": "Bilişsel fonksiyonlarınızı (Ni, Ne, Ti, Te vb.) analiz ederek 16 tipten hangisine yakın olduğunuzu belirler.",
    "Çoklu Zeka (Gardner)": "Sözel, sayısal, görsel, müzikal gibi 8 farklı zeka türündeki potansiyelinizi haritalandırır.",
    "Duygusal Zeka (EQ-i)": "Duyguları tanıma, yönetme ve empati yeteneğinizi ölçen klinik tabanlı analiz.",
    "Enneagram & Kanatlar": "Temel korku ve arzularınıza dayalı 9 kişilik tipinden hangisi olduğunuzu ve gelişim yollarınızı bulur.",
    "Karakter Güçleri (VIA)": "Sizi özgün kılan 24 karakter gücünden (Cesaret, Bilgelik, Adalet vb.) hangilerinin imza güçleriniz olduğunu keşfeder.",
    "Bağlanma Stilleri": "İlişkilerdeki güven, kaygı ve kaçınma dinamiklerinizi analiz eder (Güvenli, Kaygılı, Kaçıngan).",
    "Yetişkin DEHB Tarama": "Dikkat eksikliği ve hiperaktivite belirtilerini nöropsikolojik çerçevede tarar (Tanı koymaz, farkındalık sağlar).",
    "Tükenmişlik (Burnout)": "Mesleki ve duygusal tükenmişlik seviyenizi ölçer.",
    "Liderlik Stili Analizi": "Yönetim ve liderlik potansiyelinizi ve tarzınızı (Dönüştürücü, Hizmetkar vb.) analiz eder."
}

# --- 4. YARDIMCI FONKSİYONLAR ---

def clean_json_string(json_string):
    if "```json" in json_string:
        json_string = json_string.split("```json")[1].split("```")[0]
    elif "```" in json_string:
        json_string = json_string.split("```")[1].split("```")[0]
    return json_string.strip()

def create_radar_chart(labels, stats, title):
    try:
        labels = np.array(labels)
        stats = np.array(stats)
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        stats = np.concatenate((stats,[stats[0]]))
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='#3B82F6', alpha=0.25)
        ax.plot(angles, stats, color='#2563EB', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10, color="#334155", weight="bold")
        ax.set_title(title, y=1.1, fontsize=14, color="#0F172A", fontweight="bold")
        ax.spines['polar'].set_visible(False)
        ax.grid(color='#E2E8F0', linestyle='--')
        return fig
    except Exception as e:
        st.error(f"Grafik hatası: {e}")
        return None

# --- 5. ANA UYGULAMA AKIŞI ---

st.markdown('<div class="main-header">Balaban Neuro-Psych</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Grok-4 Reasoning Engine ile Güçlendirilmiş Klinik Analiz</div>', unsafe_allow_html=True)

if "current_stage" not in st.session_state: st.session_state.current_stage = "selection"
if "selected_test" not in st.session_state: st.session_state.selected_test = None
if "questions" not in st.session_state: st.session_state.questions = []
if "answers" not in st.session_state: st.session_state.answers = {}

# AŞAMA 1: TEST SEÇİMİ
if st.session_state.current_stage == "selection":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 📋 Envanter Seçimi")
        selected = st.radio("Test Listesi:", list(TESTLER.keys()), label_visibility="collapsed")
    
    with col2:
        st.info(f"**{selected}**\n\n{TESTLER[selected]}")
        st.markdown("---")
        if st.button("🚀 Analiz Protokolünü Başlat", type="primary"):
            st.session_state.selected_test = selected
            with st.spinner("Grok-4 Reasoning Engine çalışıyor: Akademik literatür taranıyor ve dinamik soru seti oluşturuluyor..."):
                # SORU ÜRETİMİ - MODEL: grok-4-1-fast-reasoning
                system_prompt = """
                Sen dünyanın en iyi psikometristisin. Görevin, belirtilen psikolojik test için kapsamlı bir soru seti hazırlamaktır.
                KURALLAR:
                1. **AKADEMİK GEÇERLİLİK:** Sorular, seçilen testin bilimsel literatürdeki alt boyutlarını tam olarak ölçmelidir.
                2. **DİL SEVİYESİ (HAYATİ ÖNEMLİ):** Soruları bir ilkokul 4. sınıf öğrencisinin bile yanlış anlamadan, tek seferde anlayabileceği kadar YALIN, BASİT ve NET bir Türkçe ile sor.
                   - Asla akademik terim kullanma. Günlük hayattan örnekler ver.
                   - Örnek: "Dürtüselliğim yüksektir" DEME -> "Sıramı beklerken çok zorlanırım" DE.
                   - Devrik cümle kurma.
                3. **YÖNLENDİRME YOK:** Soru nötr olmalı.
                4. **TERS MADDELER:** Soruların %30'u ters puanlanmalı (reverse_scored: true).
                5. **FORMAT:** Sadece ve sadece belirtilen JSON formatında çıktı ver.
                """
                
                user_prompt = f"""
                Test Konusu: {selected}
                Soru Sayısı: Testin bilimsel güvenilirliği (reliability) için gereken ideal sayı. (Minimum 50 soru, Maksimum 80 soru). Konuya göre optimize et.
                İstenen JSON Formatı:
                {{ "questions": [ {{"id": 1, "text": "Soru metni", "category": "Alt Boyut", "reverse_scored": false}}, ... ] }}
                """
                
                try:
                    response = client.chat.completions.create(
                        model="grok-4-1-fast-reasoning", # SORU ÜRETİMİ İÇİN GÜÇLÜ MODEL
                        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                        temperature=0.4,
                        response_format={"type": "json_object"}
                    )
                    raw_json = clean_json_string(response.choices[0].message.content)
                    data = json.loads(raw_json)
                    st.session_state.questions = data["questions"]
                    st.session_state.answers = {}
                    st.session_state.current_stage = "testing"
                    st.rerun()
                except Exception as e:
                    st.error(f"Soru seti oluşturulurken hata: {e}")

# AŞAMA 2: TEST UYGULAMA
elif st.session_state.current_stage == "testing":
    percent = len(st.session_state.answers) / len(st.session_state.questions)
    st.progress(percent)
    st.markdown(f"### 📝 {st.session_state.selected_test}")
    st.caption(f"Toplam {len(st.session_state.questions)} madde. Lütfen samimiyetle cevaplayın.")
    
    questions = st.session_state.questions
    with st.form("test_form"):
        for q in questions:
            st.markdown(f"""
            <div class="question-card">
                <h4 style="margin:0; color:#1E293B; font-weight:600;">{q['id']}. {q['text']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            options = [("1", "Hiç Katılmıyorum"), ("2", "Katılmıyorum"), ("3", "Kararsızım"), ("4", "Katılıyorum"), ("5", "Tamamen Katılıyorum")]
            choice = st.radio(f"q_{q['id']}", options, format_func=lambda x: x[1], key=f"rad_{q['id']}", horizontal=True, label_visibility="collapsed")
            
            st.session_state.answers[q['id']] = {
                "score": int(choice[0]),
                "text": q['text'],
                "category": q.get('category', 'Genel'),
                "reverse": q.get('reverse_scored', False)
            }
        
        if st.form_submit_button("✅ Testi Tamamla ve Raporla"):
            st.session_state.current_stage = "report"
            st.rerun()

# AŞAMA 3: RAPOR VE ANALİZ
elif st.session_state.current_stage == "report":
    st.markdown("## 📊 Klinik Analiz Raporu")
    
    with st.spinner("Grok-4 Reasoning Engine verileri işliyor: Milyarlarca parametre ile derin analiz yapılıyor..."):
        answers_json = json.dumps(st.session_state.answers, ensure_ascii=False)
        
        # RAPORLAMA - MODEL: grok-4-1-fast-reasoning
        system_prompt_report = """
        Sen dünyanın en saygın klinik psikologlarından birisin (Irvin Yalom ekolü).
        Elinizdeki verileri analiz ederek, danışana hayatını değiştirecek derinlikte bir rapor yazacaksın.
        
        HEDEF KİTLE VE DİL:
        - Raporu lise mezunu biri rahatça anlayabilmeli.
        - Asla ağır akademik terim kullanma, kullanırsan parantez içinde açıkla.
        - Ton: Bilge, destekleyici, profesyonel ve içten.
        
        İÇERİK DERİNLİĞİ:
        - Sadece puanları söyleme, bu puanların hayata, ilişkilere ve kariyere etkisini YORUMLA.
        - Çelişkili cevapları, gizli riskleri ve potansiyelleri bul.
        
        ÇIKTI FORMATI (JSON):
        {
            "executive_summary": "Kişinin 2-3 cümlelik özeti.",
            "deep_analysis": "HTML formatında (<h3>Başlık</h3> <p>Metin</p>) detaylı analiz.",
            "hidden_patterns": "Farkında olunmayan gizli örüntüler.",
            "action_plan": ["Öneri 1", "Öneri 2", "Öneri 3"],
            "chart_data": { "labels": ["Kat1", "Kat2"], "scores": [80, 50] }
        }
        """
        
        try:
            response_report = client.chat.completions.create(
                model="grok-4-1-fast-reasoning", # RAPORLAMA İÇİN DE GÜÇLÜ MODEL
                messages=[
                    {"role": "system", "content": system_prompt_report},
                    {"role": "user", "content": f"Test: {st.session_state.selected_test}\nCevaplar: {answers_json}"}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            raw_report = clean_json_string(response_report.choices[0].message.content)
            report_data = json.loads(raw_report)
            
            # Sunum
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.markdown("### 🎯 Yönetici Özeti")
            st.info(report_data["executive_summary"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_graph, col_text = st.columns([1, 1])
            with col_graph:
                st.markdown("### 🕸️ Yetkinlik Haritası")
                if "chart_data" in report_data:
                    chart_fig = create_radar_chart(
                        report_data["chart_data"]["labels"],
                        report_data["chart_data"]["scores"],
                        "Kişilik Profili (%)"
                    )
                    if chart_fig: st.pyplot(chart_fig)
            
            with col_text:
                st.markdown("### 🔍 Farkındalık")
                st.write(report_data.get("hidden_patterns", "..."))
                st.markdown("### 🚀 Aksiyon Planı")
                for item in report_data.get("action_plan", []):
                    st.success(f"📌 {item}")

            st.markdown("---")
            st.markdown("### 🧠 Derinlemesine Klinik Analiz")
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.markdown(report_data["deep_analysis"], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.warning("⚠️ YASAL UYARI: Bu analiz yapay zeka destekli olup tıbbi tanı yerine geçmez.")
            
            if st.button("🔄 Yeni Analiz Başlat"):
                st.session_state.current_stage = "selection"
                st.session_state.answers = {}
                st.session_state.questions = []
                st.rerun()

        except Exception as e:
            st.error(f"Rapor hatası: {e}")
