import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
import os

# --- 1. SAYFA KONFİGÜRASYONU VE STİL (PROFESYONEL UI) ---
st.set_page_config(
    page_title="Balaban Neuro-Psych | Gelişmiş Analiz",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Özel CSS: Modern, temiz ve okunabilir bir arayüz için
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: #1E293B;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .question-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border-left: 5px solid #3B82F6;
    }
    
    .report-section {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
    }
    
    .highlight {
        color: #2563EB;
        font-weight: 600;
    }
    
    /* Streamlit butonlarını özelleştirme */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
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

# Sidebar: API Durumu ve Hakkında
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=80)
    st.markdown("### 🧠 Balaban Neuro-Psych")
    st.markdown("---")
    if not GROK_API_KEY:
        st.error("🔴 API Bağlantısı Yok")
        st.warning("Lütfen API anahtarınızı .env dosyasına veya Secrets alanına ekleyin.")
        st.stop()
    else:
        st.success("🟢 Sistem Çevrimiçi")
    
    st.info("""
    **Sistem Mimarisi:**
    Bu uygulama, klinik psikoloji literatürünü tarayan **Grok-2** (Beta) yapay zeka modelini kullanır. 
    
    **Metodoloji:**
    Sorular, psikometrik geçerlilik esas alınarak dinamik üretilir.
    """)

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# --- 3. TEST VERİTABANI VE İÇERİK ---
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
    """LLM bazen JSON'ı markdown blokları içine yazar, bunu temizler."""
    if "```json" in json_string:
        json_string = json_string.split("```json")[1].split("```")[0]
    elif "```" in json_string:
        json_string = json_string.split("```")[1].split("```")[0]
    return json_string.strip()

def create_radar_chart(labels, stats, title):
    """Matplotlib ile profesyonel Radar (Örümcek) Grafiği çizer."""
    try:
        labels = np.array(labels)
        stats = np.array(stats)

        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        
        # Grafiği kapatmak için ilk değeri sona ekle
        stats = np.concatenate((stats,[stats[0]]))
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        
        ax.fill(angles, stats, color='#3B82F6', alpha=0.25)
        ax.plot(angles, stats, color='#2563EB', linewidth=2)
        
        # Etiketleri ayarla
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9, color="#475569")
        
        ax.set_title(title, y=1.1, fontsize=14, color="#1E293B", fontweight="bold")
        
        # Arka planı temizle
        ax.spines['polar'].set_visible(False)
        ax.grid(color='#E2E8F0', linestyle='--')
        
        return fig
    except Exception as e:
        st.error(f"Grafik hatası: {e}")
        return None

# --- 5. ANA UYGULAMA AKIŞI ---

# Başlık Alanı
st.markdown('<div class="main-header">Balaban Neuro-Psych Analiz Merkezi</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Yapay Zeka Destekli, Klinik Derinlikte, Herkes İçin Anlaşılır.</div>', unsafe_allow_html=True)

# Session State Başlatma
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "selection" # selection -> testing -> report
if "selected_test" not in st.session_state:
    st.session_state.selected_test = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

# AŞAMA 1: TEST SEÇİMİ
if st.session_state.current_stage == "selection":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📋 Test Envanteri")
        selected = st.radio(
            "Lütfen uygulamak istediğiniz testi seçin:",
            list(TESTLER.keys()),
            label_visibility="collapsed"
        )
    
    with col2:
        st.info(f"**{selected}**\n\n{TESTLER[selected]}")
        st.markdown("---")
        st.markdown("""
        **Süreç Nasıl İşler?**
        1. **Hazırlık:** Yapay zeka, seçilen konuda akademik literatürü tarayarak size özel 20 adet soru hazırlar.
        2. **Uygulama:** Sorular, herkesin anlayabileceği kadar sade bir dille sorulur.
        3. **Analiz:** Cevaplarınız, klinik psikoloji uzmanı seviyesinde bir yapay zeka tarafından analiz edilir.
        4. **Rapor:** Sonuçlar, derinlemesine içgörüler ve grafiklerle sunulur.
        """)
        
        if st.button("🚀 Analizi Başlat", type="primary"):
            st.session_state.selected_test = selected
            
            with st.spinner("Nöro-psikolojik soru seti oluşturuluyor... Lütfen bekleyin."):
                # --- PROMPT MÜHENDİSLİĞİ: SORU ÜRETİMİ ---
                # Hedef: Akademik derinlikte construct (yapı), İlkokul seviyesinde dil.
                system_prompt = """
                Sen dünyanın en iyi psikometristisin. Görevin, belirtilen psikolojik test için soru seti hazırlamaktır.
                
                KURALLAR:
                1. **AKADEMİK GEÇERLİLİK:** Sorular, seçilen testin bilimsel literatürdeki (örn: Big Five için Costa & McCrae) alt boyutlarını tam olarak ölçmelidir.
                2. **DİL SEVİYESİ (ÇOK ÖNEMLİ):** Soruları bir ilkokul 4. sınıf öğrencisinin bile yanlış anlamadan, tek seferde anlayabileceği kadar YALIN, BASİT ve NET bir Türkçe ile sor.
                   - Asla akademik terim (örn: "bilişsel çarpıtma", "dürtüsellik") kullanma. Bunun yerine günlük hayattan örnekler ver.
                   - Örnek: "Dürtüselliğim yüksektir" DEME -> "Sıramı beklerken çok zorlanırım" DE.
                   - Devrik cümle kurma. Dolaylı anlatım yapma.
                3. **YÖNLENDİRME YOK:** Soru, "iyi" veya "kötü" cevabı hissettirmemeli. Nötr olmalı.
                4. **TERS MADDELER:** Soruların %30'u ters puanlanmalı (reverse_scored: true).
                5. **FORMAT:** Sadece ve sadece belirtilen JSON formatında çıktı ver.
                """
                
                user_prompt = f"""
                Test Konusu: {selected}
                Soru Sayısı: 20
                
                İstenen JSON Formatı:
                {{
                    "questions": [
                        {{"id": 1, "text": "Buraya çok basit, anlaşılır soru metni gelecek", "category": "Alt Boyut Adı", "reverse_scored": false}},
                        ...
                    ]
                }}
                """
                
                try:
                    response = client.chat.completions.create(
                        model="grok-2-latest", # En son model
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.4, # Yaratıcılık düşük, tutarlılık orta
                        response_format={"type": "json_object"}
                    )
                    
                    raw_json = clean_json_string(response.choices[0].message.content)
                    data = json.loads(raw_json)
                    st.session_state.questions = data["questions"]
                    st.session_state.answers = {} # Cevapları sıfırla
                    st.session_state.current_stage = "testing"
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Soru seti oluşturulurken bir hata oluştu: {e}")

# AŞAMA 2: TEST UYGULAMA
elif st.session_state.current_stage == "testing":
    st.progress(len(st.session_state.answers) / len(st.session_state.questions))
    
    st.markdown(f"### 📝 {st.session_state.selected_test}")
    st.caption("Aşağıdaki ifadeleri sizi ne kadar iyi tanımladığına göre derecelendirin.")
    
    questions = st.session_state.questions
    
    # Form kullanımı: Her seçimde sayfa yenilenmesini engeller
    with st.form("test_form"):
        for q in questions:
            st.markdown(f"""
            <div class="question-card">
                <h4 style="margin:0; color:#1E293B;">{q['id']}. {q['text']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Radyo butonlarını yatay ve temiz göster
            col_opts = st.columns(5)
            options = [
                ("1", "Hiç Katılmıyorum"),
                ("2", "Katılmıyorum"),
                ("3", "Kararsızım"),
                ("4", "Katılıyorum"),
                ("5", "Tamamen Katılıyorum")
            ]
            
            # Benzersiz key kullanarak cevapları al
            choice = st.radio(
                f"Soru {q['id']} cevabı:",
                options,
                format_func=lambda x: x[1], # Sadece metni göster
                key=f"q_{q['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            # Cevabı kaydet (1-5 arası int)
            st.session_state.answers[q['id']] = {
                "score": int(choice[0]),
                "text": q['text'],
                "category": q.get('category', 'Genel'),
                "reverse": q.get('reverse_scored', False)
            }
            st.markdown("---")

        submitted = st.form_submit_button("✅ Testi Bitir ve Analiz Et")
        
        if submitted:
            st.session_state.current_stage = "report"
            st.rerun()

# AŞAMA 3: RAPOR VE ANALİZ
elif st.session_state.current_stage == "report":
    st.markdown("## 📊 Analiz Raporunuz")
    
    with st.spinner("Verileriniz uzman sistem tarafından işleniyor... Milyarlarca parametre taranıyor..."):
        # --- PROMPT MÜHENDİSLİĞİ: RAPORLAMA ---
        # Hedef: Akademik/Klinik derinlikte analiz, Lise mezunu anlaşılırlığında dil.
        
        answers_json = json.dumps(st.session_state.answers, ensure_ascii=False)
        
        system_prompt_report = """
        Sen dünyanın en saygın klinik psikologlarından birisin (Örn: Irvin Yalom veya Carl Rogers tarzında).
        Elinizdeki verileri analiz ederek, danışanınıza hayatını değiştirecek derinlikte bir rapor yazacaksın.
        
        HEDEF KİTLE VE DİL:
        - Rapor, bir lise mezununun rahatça okuyup anlayabileceği akıcılıkta olmalı.
        - Asla "Duygulanım küntlüğü", "Bilişsel disonans" gibi ağır terimler kullanma. Kullanacaksan da parantez içinde halk diliyle açıkla.
        - Tonun: Destekleyici, profesyonel, bilge ve içten olsun.
        
        İÇERİK DERİNLİĞİ:
        - Sadece puanları söyleyip geçme. (Örn: "Dışadönüklüğünüz 5 üzerinden 4" DEME.)
        - Bu puanın onun hayatına etkisini, potansiyel kör noktalarını, ilişkilerine yansımasını ANALİZ ET.
        - Satır aralarını oku. Çelişkili cevaplar varsa (ters maddeler) bunları yorumla.
        
        ÇIKTI FORMATI (JSON):
        Aşağıdaki JSON yapısında çıktı ver:
        {
            "executive_summary": "Yöneticiler için özet gibi, kişinin genel profilinin 2-3 cümlelik özü.",
            "deep_analysis": "Her bir alt boyut veya kategori için detaylı, derinlemesine paragraflar. Başlıklar HTML formatında olsun (<h3>Başlık</h3> gibi).",
            "hidden_patterns": "Kişinin belki de farkında olmadığı, cevaplardaki gizli örüntüler veya riskler.",
            "action_plan": [
                "Somut, uygulanabilir öneri 1",
                "Somut, uygulanabilir öneri 2",
                "Somut, uygulanabilir öneri 3"
            ],
            "chart_data": {
                "labels": ["Kategori1", "Kategori2", "Kategori3"...],
                "scores": [85, 40, 60...] (100 üzerinden normalize edilmiş puanlar)
            }
        }
        """
        
        try:
            response_report = client.chat.completions.create(
                model="grok-2-latest",
                messages=[
                    {"role": "system", "content": system_prompt_report},
                    {"role": "user", "content": f"Test: {st.session_state.selected_test}\nCevaplar: {answers_json}"}
                ],
                temperature=0.6,
                response_format={"type": "json_object"}
            )
            
            raw_report = clean_json_string(response_report.choices[0].message.content)
            report_data = json.loads(raw_report)
            
            # 1. Yönetici Özeti
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.markdown("### 🎯 Genel Bakış")
            st.info(report_data["executive_summary"])
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_graph, col_text = st.columns([1, 1])
            
            # 2. Grafiksel Analiz
            with col_graph:
                st.markdown("### 🕸️ Profil Haritası")
                if "chart_data" in report_data:
                    chart_fig = create_radar_chart(
                        report_data["chart_data"]["labels"],
                        report_data["chart_data"]["scores"],
                        "Yetkinlik Dağılımı (%)"
                    )
                    if chart_fig:
                        st.pyplot(chart_fig)
            
            # 3. Gizli Örüntüler (Farkındalık)
            with col_text:
                st.markdown("### 🔍 Farkındalık Alanları")
                st.write(report_data.get("hidden_patterns", "Analiz ediliyor..."))
                
                st.markdown("### 🌱 Gelişim Adımları")
                for item in report_data.get("action_plan", []):
                    st.success(f"📌 {item}")

            # 4. Derinlemesine Analiz (Uzun Metin)
            st.markdown("---")
            st.markdown("### 🧠 Detaylı Klinik Analiz")
            st.markdown('<div class="report-section">', unsafe_allow_html=True)
            st.markdown(report_data["deep_analysis"], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.warning("⚠️ YASAL UYARI: Bu rapor yapay zeka tarafından eğitim ve farkındalık amaçlı üretilmiştir. Tıbbi tanı veya tedavi yerine geçmez. Lütfen profesyonel destek alınız.")
            
            if st.button("🔄 Yeni Test Başlat"):
                st.session_state.current_stage = "selection"
                st.session_state.answers = {}
                st.session_state.questions = []
                st.rerun()

        except Exception as e:
            st.error(f"Rapor oluşturulurken hata: {e}")
