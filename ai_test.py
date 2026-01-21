import streamlit as st
import json
import matplotlib.pyplot as plt
from openai import OpenAI
import os

# --- API ANAHTARI YÖNETİMİ (TEK BLOK, HEM LOKAL HEM BULUT UYUMLU) ---
GROK_API_KEY = None

# 1. Streamlit Cloud Secrets (bulutta çalışırken öncelikli)
if "GROK_API_KEY" in st.secrets:
    GROK_API_KEY = st.secrets["GROK_API_KEY"]
else:
    # 2. Lokal .env dosyası (bilgisayarda test ederken)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        GROK_API_KEY = os.getenv('GROK_API_KEY')
    except:
        pass

# Tek kontrol ve mesaj
if not GROK_API_KEY:
    st.error("⚠️ GROK_API_KEY bulunamadı! Streamlit Cloud 'Secrets' kısmına veya lokal .env dosyasına ekleyin.")
    st.stop()

st.success("✅ Grok API hazır!")

# OpenAI client (Grok için)
client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# Test listesi
TESTLER = {
    "Big Five Kişilik Testi": "Big Five Kişilik Testi",
    "MBTI Temelli Kişilik Tipi Testi": "MBTI Temelli Kişilik Tipi Testi",
    "Çoklu Zeka Testi (Gardner temelli)": "Çoklu Zeka Testi (Gardner temelli)",
    "Seçici Dikkat Testi (D2 ilhamlı)": "Seçici Dikkat Testi (D2 ilhamlı)",
    "Sürekli Dikkat Testi (MOXO ilhamlı)": "Sürekli Dikkat Testi (MOXO ilhamlı)",
    "Yetişkin DEHB Tarama Testi (DIVA ilhamlı)": "Yetişkin DEHB Tarama Testi (DIVA ilhamlı)",
    "Duygusal Zeka (EQ) Testi": "Duygusal Zeka (EQ) Testi",
    "Karakter Güçleri Testi (VIA 24 güç)": "Karakter Güçleri Testi (VIA 24 güç)",
    "Bağlanma Stili Testi": "Bağlanma Stili Testi",
    "Enneagram Kişilik Tipi Testi": "Enneagram Kişilik Tipi Testi (9 tip + kanatlar)",
    "Pozitif Psikoloji ve İyi Oluş Testi": "Pozitif Psikoloji ve İyi Oluş Testi (PERMA + VIA + Flourishing)"
}

# Tüm testlerin çok detaylı akademik açıklamaları
TEST_ACIKLAMALARI = {
    "Big Five Kişilik Testi": """
**Big Five Kişilik Testi (OCEAN Modeli)**  
**Bilimsel Temel ve Köken:** Lexical hipotezden türetilmiş, Allport & Odbert (1936)'tan başlayarak Goldberg (1990) ve Costa & McCrae (1992) tarafından NEO-PI-R ile standardize edilmiş. Binlerce kültürlerarası çalışma (McCrae & Costa, 2008) ile en güvenilir kişilik modeli kabul edilir.  
**Alt Boyutlar ve Detaylar:**  
- Açıklık: Yeni deneyimlere açıklık, hayal gücü, estetik hassasiyet, liberal değerler.  
- Sorumluluk: Düzenlilik, öz disiplin, planlama, güvenilirlik.  
- Dışadönüklük: Sosyal etkileşim, heyecan arayışı, pozitif duygular.  
- Uyumluluk: Empati, altruizm, işbirliği, güven.  
- Duygusal Dengelilik: Kaygı, depresyon ve öfkeye karşı direnç (Neuroticism ters skorlanır).  
**Akademik Geçerlilik:** Yüksek test-retest güvenilirliği (α > .80), öngörü gücü (iş performansı, ilişki tatmini, sağlık sonuçları).  
**Uygulamamızda:** 50+ derin akademik madde, percentile karşılaştırması, davranış tahminleri ve gelişim planı içeren klinik üstü rapor.
    """,
    "MBTI Temelli Kişilik Tipi Testi": """
**MBTI Temelli Kişilik Tipi Testi**  
**Bilimsel Temel:** Carl Jung'un Psikolojik Tipler (1921) kitabından, Isabel Myers ve Katharine Briggs tarafından geliştirilmiş (1940'lar). Modern versiyonlar fonksiyon yığını (Ni, Se vb.) içerir.  
**Alt Boyutlar:** E/I (Enerji kaynağı), S/N (Bilgi toplama), T/F (Karar verme), J/P (Yaşam tarzı) → 16 tip.  
**Akademik Geçerlilik:** Big Five ile yüksek korelasyon, kariyer danışmanlığında yaygın (CPP, Inc.).  
**Uygulamamızda:** Sürekli ölçüm, fonksiyon gelişimi tavsiyeleri, tip + ikincil tip analizi, derin içgörü raporu.
    """,
    "Çoklu Zeka Testi (Gardner temelli)": """
**Çoklu Zeka Testi**  
**Bilimsel Temel:** Howard Gardner, Frames of Mind (1983, revize 2011). Geleneksel g faktörüne karşı, nörobilim ve antropolojik kanıtlarla 8-9 bağımsız zeka önerir.  
**Zekâ Türleri Detayları:**  
- Dilsel, Mantıksal-Matematiksel, Bedensel-Kinestetik, Müzikal, Uzamsal, Kişilerarası, İçsel, Doğacı, Varoluşsal.  
**Akademik Geçerlilik:** Eğitim psikolojisinde etkili, öğrenme stilleri üzerine çalışmalarla desteklenir.  
**Uygulamamızda:** Baskın/ikincil zekâlar tespiti, kariyer ve öğrenme stili önerileriyle zengin rapor.
    """,
    "Seçici Dikkat Testi (D2 ilhamlı)": """
**Seçici Dikkat Testi (D2 İlhamlı)**  
**Bilimsel Temel:** Rolf Brickenkamp'ın D2 Testi (1962, revize 2003), nöropsikolojide standart seçici dikkat ölçümü.  
**Ölçtüğü Detaylar:** Görsel tarama hızı, doğruluk, konsantrasyon altında performans, distraktör direnci.  
**Akademik Geçerlilik:** Klinik tanı için yüksek güvenilirlik.  
**Uygulamamızda:** Şıklı senaryolarla simülasyon, dikkat geliştirme egzersizleri içeren rapor.
    """,
    "Sürekli Dikkat Testi (MOXO ilhamlı)": """
**Sürekli Dikkat Testi (MOXO İlhamlı)**  
**Bilimsel Temel:** MOXO-CPT (Berger et al., 2013), sürekli performans testi.  
**Ölçtüğü İndeksler:** Dikkat, Zamanlama, Dürtüsellik, Hiperaktivite.  
**Akademik Geçerlilik:** DEHB tanısında yüksek sensitivite/specificity.  
**Uygulamamızda:** Distraktör simülasyonu, strateji ve farkındalık raporu.
    """,
    "Yetişkin DEHB Tarama Testi (DIVA ilhamlı)": """
**Yetişkin DEHB Tarama Testi**  
**Bilimsel Temel:** DIVA 5.0 (Kooij et al., 2019), DSM-5 kriterlerine dayalı.  
**Ölçtüğü:** 18 kriter (dikkat eksikliği + hiperaktivite/dürtüsellik).  
**Uygulamamızda:** Farkındalık amaçlı, profesyonel yönlendirme içeren derin rapor.
    """,
    "Duygusal Zeka (EQ) Testi": """
**Duygusal Zeka Testi**  
**Bilimsel Temel:** Mayer-Salovey-Caruso (MSCEIT, 2002), Goleman (1995).  
**Alt Boyutlar:** Duygu algısı, kullanım, anlama, yönetim.  
**Uygulamamızda:** Senaryo temelli, pratik egzersizlerle rapor.
    """,
    "Karakter Güçleri Testi (VIA 24 güç)": """
**Karakter Güçleri Testi**  
**Bilimsel Temel:** Peterson & Seligman (2004), VIA Enstitüsü.  
**Ölçtüğü:** 24 imza güç (6 erdem altında).  
**Uygulamamızda:** Güç kullanımı egzersizleri, pozitif müdahale planı.
    """,
    "Bağlanma Stili Testi": """
**Bağlanma Stili Testi**  
**Bilimsel Temel:** Bowlby-Ainsworth (1969-80), Bartholomew (1991).  
**Stiller:** Güvenli, Kaygılı, Kaçıngan-Korkulu, Kaçıngan-Reddedici.  
**Uygulamamızda:** ECR-R temelli ilişki dinamikleri analizi.
    """,
    "Enneagram Kişilik Tipi Testi": """
**Enneagram Kişilik Tipi Testi**  
**Bilimsel Temel:** Riso-Hudson (1990’lar), Big Five korelasyonları.  
**Detaylı Tip + Kanat + Sağlık Seviyeleri:** 9 tip (1 Mükemmeliyetçi - 9 Barışçı), kanatlar (w9/w2 vb.), korku/arzu, büyüme/stres yolları.  
**Uygulamamızda:** Tip + kanat + sağlık seviyesi tespiti, derin gelişim raporu.
    """,
    "Pozitif Psikoloji ve İyi Oluş Testi": """
**Pozitif Psikoloji ve İyi Oluş Testi**  
**Bilimsel Temel:** Martin Seligman (1998-2011), Csikszentmihalyi akış teorisi.  
**PERMA Modeli Detaylı Açıklama:**  
- **P - Positive Emotion:** Fredrickson broaden-and-build (2001).  
- **E - Engagement:** Csikszentmihalyi (1990).  
- **R - Relationships:** Sosyal bağlar.  
- **M - Meaning:** Frankl etkisi.  
- **A - Accomplishment:** Grit (Duckworth, 2007).  
**Ek Modeller:** VIA 24 güç, Flourishing (Diener 2010), resilience, optimism.  
**Uygulamamızda:** 60+ madde, PERMA + imza güçler + adım adım müdahale planı.
    """
}

# Sayfa başlığı
st.markdown("# 🧠 BALABAN KOÇLUK – Ultimate Psikolojik Test Uygulaması")
st.markdown("**Aşağıdan istediğiniz testi seçin, detaylı akademik açıklamayı okuyun ve testi başlatın.**")

# Test seçimi
test_secimi = st.selectbox(
    "UYGULAMAK İSTEDİĞİNİZ TESTİ SEÇİNİZ",
    options=["-- Lütfen bir test seçin --"] + list(TESTLER.keys())
)

# Açıklama gösterimi
if test_secimi and not test_secimi.startswith("--"):
    st.markdown(f"## {test_secimi} - Detaylı Akademik Açıklama")
    st.markdown(TEST_ACIKLAMALARI.get(test_secimi, "Açıklama bulunamadı."))
else:
    st.info("Lütfen yukarıdan bir test seçerek detaylı akademik açıklamayı okuyun.")

# Test başlatma
if test_secimi and not test_secimi.startswith("--"):
    if st.button("🚀 Testi Başlat", type="primary"):
        with st.spinner("50 derin akademik soru Grok-4 ile üretiliyor... Lütfen bekleyin (10-30 saniye sürebilir)"):
            soru_prompt = f"""
            Sen akademik psikoloji profesörüsün. Dünyanın en iyi akademik psikoloji profesörü sensin. {test_secimi} için tam 50 adet üst düzey bilimsel, orijinal soru üret.
            Gereksinimler:
            - Her soru: Seçilen teste o testin konusuna göre; mükemmel, derin ve ayrıntılı, eşsiz, akademik kalitede, çok üst seviye sorulardan oluşsun.
            - Her soru 5 şıklı Likert ölçeği.
            - Kusursuz, doğal ve akıcı Türkçe (devrik cümle asla yok).
            - En az %40 ters puanlanan madde (sosyal desirability bias önleme).
            - 10+ kontrol/tekrar sorusu.
            - HER SORUDA 'reverse_scored' ALANI ZORUNLU (true/false).
            - Çıktı KESİNLİKLE sadece şu JSON olsun:
            {{
              "questions": [
                {{"id": 1, "text": "Soru metni burada.", "reverse_scored": false}},
                ...
              ]
            }}
            JSON dışında hiçbir şey yazma!
            """
            try:
                response = client.chat.completions.create(
                    model="grok-4",
                    messages=[
                        {"role": "system", "content": "Sadece tam JSON üret, ekstra hiçbir şey yazma."},
                        {"role": "user", "content": soru_prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                questions_data = json.loads(response.choices[0].message.content)
                questions = questions_data.get("questions", [])
                
                if len(questions) == 0:
                    st.error("Soru üretimi başarısız oldu. Lütfen tekrar deneyin.")
                    st.stop()
                    
            except Exception as e:
                st.error(f"Soru üretimi sırasında hata: {e}")
                st.stop()

        st.session_state.questions = questions
        st.session_state.test_name = test_secimi
        st.session_state.answers = {}
        st.session_state.report = None  # Rapor sıfırlansın
        st.rerun()

# Sorular gösterimi
if "questions" in st.session_state:
    st.markdown(f"## 📋 {st.session_state.test_name}")
    st.markdown("Lütfen tüm soruları dikkatle cevaplayın. Tüm sorular zorunludur.")

    questions = st.session_state.questions
    answers = st.session_state.get("answers", {})

    for q in questions:
        q_id = q["id"]
        q_text = q["text"]
        reverse = q.get("reverse_scored", False)
        
        st.markdown(f"**Soru {q_id}:** {q_text}")
        if reverse:
            st.caption("⚠️ Bu madde ters puanlanıyor (dikkatli cevaplayın)")

        cevap = st.radio(
            "Seçiminiz:",
            options=[
                "Kesinlikle Katılmıyorum (1)",
                "Katılmıyorum (2)",
                "Kararsızım (3)",
                "Katılıyorum (4)",
                "Kesinlikle Katılıyorum (5)"
            ],
            index=None,  # İşaretsiz başlasın
            key=f"q_{q_id}"
        )
        
        if cevap:
            value = int(cevap.split("(")[1][0])
            answers[q_id] = {"answer": value, "reverse": reverse}

    st.session_state.answers = answers

    if st.button("📊 Çok Detaylı Raporu Göster", type="primary"):
        if len(answers) < len(questions):
            st.warning("⚠️ Lütfen tüm soruları cevaplayın!")
        else:
            with st.spinner("Dünyanın en derin psikolojik analizi hazırlanıyor... (20-40 saniye sürebilir)"):
                answers_list = [
                    {"id": q_id, "answer": info["answer"]} 
                    for q_id, info in answers.items()
                ]
                
                analiz_prompt = f"""
                Sen dünyanın en iyi klinik psikoloğu ve akademik araştırmacısısın. {st.session_state.test_name} sonuçlarını inanılmaz derinlikte analiz et.
                Cevaplar: {json.dumps(answers_list, ensure_ascii=False)}
                
                Rapor KESİNLİKLE şu JSON formatında olsun (HER ALAN ZORUNLU ve dolu olsun):
                {{
                  "summary": "Percentile'li özet metin",
                  "scientific_explanation": "Referanslı bilimsel açıklama",
                  "detailed_analysis": "Katmanlı detaylı analiz",
                  "strengths": ["Güçlü yön 1", "Güçlü yön 2", ...],
                  "improvements": ["Geliştirilebilir yön 1", "Geliştirilebilir yön 2", ...],
                  "recommendations": ["Adım adım tavsiye 1", "Adım adım tavsiye 2", ...],
                  "graphics": {{
                    "bar": {{"labels": ["Boyut1", "Boyut2", "..."], "data": [85, 70, ...]}},
                    "radar": {{"labels": ["Boyut1", "Boyut2", "..."], "data": [85, 70, ...]}},
                    "pie": {{"labels": ["Güçlü", "Orta", "Geliştirilebilir"], "data": [60, 30, 10]}}
                  }},
                  "disclaimer": "Bu test eğlence ve kendini tanıma amaçlıdır. Profesyonel tanı yerine geçmez."
                }}
                Akıcı, olumlu ve motive edici Türkçe yaz. JSON dışında hiçbir şey yazma!
                """
                try:
                    response2 = client.chat.completions.create(
                        model="grok-4",
                        messages=[
                            {"role": "system", "content": "Sadece tam JSON üret, ekstra metin yok."},
                            {"role": "user", "content": analiz_prompt}
                        ],
                        temperature=0.7,
                        response_format={"type": "json_object"}
                    )
                    report = json.loads(response2.choices[0].message.content)
                    st.session_state.report = report  # Raporu kaydet (kaybolmasın!)
                except Exception as e:
                    st.error(f"Rapor üretimi hatası: {e}")
                    st.stop()

            st.rerun()  # Raporu göstermek için rerun

# Rapor gösterimi (kalıcı olsun)
if "report" in st.session_state and st.session_state.report:
    report = st.session_state.report
    test_name = st.session_state.test_name
    
    st.markdown(f"# 📊 {test_name} – İnanılmaz Derin Rapor")
    
    st.markdown(f"**Özet:** {report.get('summary', '')}")
    st.markdown(f"**Bilimsel Açıklama:**\n{report.get('scientific_explanation', '')}")
    st.markdown(f"**Detaylı Analiz:**\n{report.get('detailed_analysis', '')}")
    
    st.markdown("### 💪 Güçlü Yönler")
    for s in report.get("strengths", []):
        st.markdown(f"- {s}")
    
    st.markdown("### 🔧 Geliştirilebilir Yönler")
    for i in report.get("improvements", []):
        st.markdown(f"- {i}")
    
    st.markdown("### 🎯 Kişiselleştirilmiş Tavsiyeler")
    for r in report.get("recommendations", []):
        st.markdown(f"- {r}")
    
    # Grafikler
    if "graphics" in report:
        g = report["graphics"]
        
        col1, col2, col3 = st.columns(3)
        
        if "bar" in g:
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            ax1.bar(g["bar"]["labels"], g["bar"]["data"], color='skyblue')
            ax1.set_title("Boyut Puanları")
            ax1.set_ylabel("Puan (%)")
            plt.xticks(rotation=45)
            col1.pyplot(fig1)
        
        if "radar" in g:
            labels = g["radar"]["labels"]
            data = g["radar"]["data"]
            angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
            angles += angles[:1]
            data += data[:1]
            
            fig2, ax2 = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
            ax2.plot(angles, data, 'o-', linewidth=3, color='purple')
            ax2.fill(angles, data, alpha=0.3, color='purple')
            ax2.set_xticks(angles[:-1])
            ax2.set_xticklabels(labels)
            ax2.set_title("Profil Radar Grafiği")
            col2.pyplot(fig2)
        
        if "pie" in g:
            fig3, ax3 = plt.subplots(figsize=(7, 7))
            ax3.pie(g["pie"]["data"], labels=g["pie"]["labels"], autopct='%1.1f%%', startangle=90)
            ax3.set_title("Genel Dağılım")
            col3.pyplot(fig3)
    
    st.info(report.get("disclaimer", "Bu test profesyonel tanı yerine geçmez."))
    
    st.success("🎉 Raporunuz hazır! Kendinizi daha iyi tanımaya bir adım daha yaklaştınız.")
    
    if st.button("🔄 Yeni Test Yap"):
        st.session_state.clear()
        st.rerun()