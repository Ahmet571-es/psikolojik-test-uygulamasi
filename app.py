# -*- coding: utf-8 -*-
"""
Eğitim Check-Up - Ana Uygulama
Eğitim Psikolojisi Değerlendirme Platformu
"""

import streamlit as st
import json
import time
from datetime import datetime

from config import APP_NAME, APP_VERSION, APP_ICON, TEST_MODULLERI
from utils.stil import uygula_genel_stil, baslik_goster, bilgi_karti

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

uygula_genel_stil()

# --- Veritabanı Otomatik Kurulum ---
if "db_kurulum_yapildi" not in st.session_state:
    st.session_state["db_kurulum_yapildi"] = False

if not st.session_state["db_kurulum_yapildi"]:
    try:
        from veritabani import tablolar_mevcut_mu, tablolari_olustur
        mevcut = tablolar_mevcut_mu()
        if mevcut is not None and len(mevcut) < 5:
            basarili, mesaj = tablolari_olustur()
            if basarili:
                st.session_state["db_kurulum_yapildi"] = True
            # İlk çalıştırmada sessizce kurulum yap
        elif mevcut is not None:
            st.session_state["db_kurulum_yapildi"] = True
    except Exception:
        pass  # DB yoksa sessizce devam et

# --- Session State Başlatma ---
_default_states = {
    "sayfa": "ana_sayfa",
    "secili_test": None,
    "test_asamasi": "bilgi",  # bilgi, sorular, sonuc
    "cevaplar": {},
    "sonuclar": None,
    "ogrenci_bilgi": {},
    "ogretmen_giris": False,
    "ogretmen": None,
    "ogrenciler": [],
    "tum_test_sonuclari": {},
    "ai_analiz_sonucu": None,
    "aile_ozet_metni": None,
}
for key, val in _default_states.items():
    if key not in st.session_state:
        st.session_state[key] = val


# --- Test Modüllerini Yükle ---
def _test_modulu_yukle(test_key):
    """Test modülünü dinamik olarak yükle"""
    modul_map = {
        "enneagram": "testler.enneagram",
        "vark": "testler.vark",
        "holland": "testler.holland",
        "coklu_zeka": "testler.coklu_zeka",
        "beyin": "testler.beyin",
        "sinav_kaygisi": "testler.sinav_kaygisi",
        "calisma_davranisi": "testler.calisma_davranisi",
        "akademik_analiz": "testler.akademik_analiz",
        "hizli_okuma": "testler.hizli_okuma",
        "dikkat": "testler.dikkat",
    }
    import importlib
    modul_yolu = modul_map.get(test_key)
    if modul_yolu:
        return importlib.import_module(modul_yolu)
    return None


# --- Sidebar ---
with st.sidebar:
    st.markdown(f"### {APP_ICON} {APP_NAME}")
    st.caption(f"v{APP_VERSION}")
    st.markdown("---")

    # Navigasyon
    st.markdown("#### Menü")

    if st.button("Ana Sayfa", use_container_width=True):
        st.session_state["sayfa"] = "ana_sayfa"
        st.rerun()

    if st.button("Testler", use_container_width=True):
        st.session_state["sayfa"] = "test_secim"
        st.rerun()

    if st.button("Öğretmen Paneli", use_container_width=True):
        st.session_state["sayfa"] = "ogretmen_paneli"
        st.rerun()

    st.markdown("---")

    # Öğrenci bilgi girişi (testler için)
    if st.session_state["sayfa"] in ("test_secim", "test_uygula"):
        st.markdown("#### Öğrenci Bilgileri")
        ogrenci_ad = st.text_input("Ad Soyad", value=st.session_state["ogrenci_bilgi"].get("ad", ""))
        ogrenci_sinif = st.text_input("Sınıf", value=st.session_state["ogrenci_bilgi"].get("sinif", ""))
        if ogrenci_ad:
            st.session_state["ogrenci_bilgi"]["ad"] = ogrenci_ad
            st.session_state["ogrenci_bilgi"]["sinif"] = ogrenci_sinif

    # Yapılan testler özeti
    if st.session_state.get("tum_test_sonuclari"):
        st.markdown("---")
        st.markdown("#### Yapılan Testler")
        ogrenci_id = st.session_state["ogrenci_bilgi"].get("ad", "default")
        testler = st.session_state["tum_test_sonuclari"].get(ogrenci_id, {})
        for test_adi in testler:
            st.write(f"- {test_adi}")

    st.markdown("---")
    st.caption("Eğitim psikolojisi platformu")


# --- Ana Sayfa ---
def ana_sayfa():
    baslik_goster(APP_NAME, "Eğitim Psikolojisi Değerlendirme Platformu")

    st.markdown("---")

    # İstatistik kartları
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        bilgi_karti("Test Modülü", "10", "📝", "#3B82F6")
    with col2:
        bilgi_karti("Kategori", "6", "📂", "#10B981")
    with col3:
        bilgi_karti("AI Analiz", "Claude", "🤖", "#8B5CF6")
    with col4:
        bilgi_karti("Rapor Formatı", "PDF/DOCX", "📄", "#F59E0B")

    st.markdown("---")
    st.markdown("### Mevcut Testler")

    # Test kartları
    cols = st.columns(2)
    for i, (key, test) in enumerate(TEST_MODULLERI.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="test-card">
                <h4>{test['ikon']} {test['ad']}</h4>
                <p style="color: #64748B; margin: 0.3rem 0;">{test['aciklama']}</p>
                <small style="color: #94A3B8;">Süre: {test['sure']} | Kategori: {test['kategori']}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    col_start1, col_start2 = st.columns(2)
    with col_start1:
        if st.button("Teste Başla", type="primary", use_container_width=True):
            st.session_state["sayfa"] = "test_secim"
            st.rerun()
    with col_start2:
        if st.button("Öğretmen Paneli", use_container_width=True, key="ana_ogretmen"):
            st.session_state["sayfa"] = "ogretmen_paneli"
            st.rerun()


# --- Test Seçim Sayfası ---
def test_secim_sayfasi():
    baslik_goster("Test Seçimi", "Uygulamak istediğiniz testi seçin")

    ogrenci_adi = st.session_state["ogrenci_bilgi"].get("ad", "")
    if not ogrenci_adi:
        st.warning("Lütfen sol panelden öğrenci bilgilerini girin.")
        return

    st.markdown("---")

    for key, test in TEST_MODULLERI.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{test['ikon']} {test['ad']}**")
            st.caption(f"{test['aciklama']} | Süre: {test['sure']}")
        with col2:
            if st.button("Başla", key=f"basla_{key}", use_container_width=True):
                st.session_state["secili_test"] = key
                st.session_state["test_asamasi"] = "bilgi"
                st.session_state["cevaplar"] = {}
                st.session_state["sonuclar"] = None
                st.session_state["sayfa"] = "test_uygula"
                st.rerun()
        st.markdown("---")


# --- Test Uygulama Sayfası ---
def test_uygulama_sayfasi():
    test_key = st.session_state.get("secili_test")
    if not test_key:
        st.session_state["sayfa"] = "test_secim"
        st.rerun()
        return

    modul = _test_modulu_yukle(test_key)
    if not modul:
        st.error("Test modülü yüklenemedi.")
        return

    test_bilgi = TEST_MODULLERI[test_key]
    ogrenci_adi = st.session_state["ogrenci_bilgi"].get("ad", "Öğrenci")

    # Test bilgi sayfası
    if st.session_state["test_asamasi"] == "bilgi":
        baslik_goster(f"{test_bilgi['ikon']} {test_bilgi['ad']}")
        st.info(test_bilgi["aciklama"])
        st.markdown(f"**Öğrenci:** {ogrenci_adi}")
        st.markdown(f"**Tahmini Süre:** {test_bilgi['sure']}")

        if st.button("Teste Başla", type="primary"):
            st.session_state["test_asamasi"] = "sorular"
            st.session_state["cevaplar"] = {}
            if test_key == "dikkat":
                from testler.dikkat import _stimulus_olustur
                st.session_state["dikkat_satirlar"] = _stimulus_olustur()
                st.session_state["dikkat_baslangic"] = time.time()
            elif test_key == "hizli_okuma":
                st.session_state["okuma_baslangic"] = None
                st.session_state["okuma_bitti"] = False
            st.rerun()
        return

    # Soru sayfası
    if st.session_state["test_asamasi"] == "sorular":
        _test_sorulari_goster(test_key, modul)
        return

    # Sonuç sayfası
    if st.session_state["test_asamasi"] == "sonuc":
        _test_sonuclari_goster(test_key, modul, ogrenci_adi)


def _test_sorulari_goster(test_key, modul):
    """Test sorularını göster (test tipine göre farklı akış)"""
    test_bilgi = TEST_MODULLERI[test_key]
    st.markdown(f"### {test_bilgi['ikon']} {test_bilgi['ad']}")

    # Özel testler
    if test_key == "hizli_okuma":
        _hizli_okuma_akisi(modul)
        return

    if test_key == "dikkat":
        _dikkat_testi_akisi(modul)
        return

    # VARK özel: çoktan seçmeli
    if test_key == "vark":
        _vark_akisi(modul)
        return

    # Standart Likert ölçekli testler
    sorular = modul.SORULAR
    secenekler = modul.SECENEKLER

    # İlerleme çubuğu
    cevaplanan = len(st.session_state["cevaplar"])
    st.progress(cevaplanan / len(sorular), text=f"{cevaplanan}/{len(sorular)} soru cevaplandı")

    with st.form("test_formu"):
        for soru in sorular:
            st.markdown(f"""
            <div class="question-card">
                <strong>{soru['id']}.</strong> {soru['metin']}
            </div>
            """, unsafe_allow_html=True)

            secim = st.radio(
                f"Soru {soru['id']}",
                options=list(secenekler.keys()),
                format_func=lambda x: secenekler[x],
                key=f"soru_{soru['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state["cevaplar"][soru["id"]] = secim

        if st.form_submit_button("Testi Tamamla", type="primary"):
            # Tüm soruların cevaplanıp cevaplanmadığını kontrol et
            st.session_state["test_asamasi"] = "sonuc"
            st.rerun()


def _vark_akisi(modul):
    """VARK testi akışı (çoktan seçmeli)"""
    sorular = modul.SORULAR
    cevaplanan = len(st.session_state["cevaplar"])
    st.progress(cevaplanan / len(sorular), text=f"{cevaplanan}/{len(sorular)} soru cevaplandı")

    with st.form("vark_formu"):
        for soru in sorular:
            st.markdown(f"""
            <div class="question-card">
                <strong>{soru['id']}.</strong> {soru['metin']}
            </div>
            """, unsafe_allow_html=True)

            secenek_metinleri = [s["metin"] for s in soru["secenekler"]]
            secim = st.radio(
                f"Soru {soru['id']}",
                options=range(len(soru["secenekler"])),
                format_func=lambda x, s=soru: s["secenekler"][x]["metin"],
                key=f"vark_{soru['id']}",
                label_visibility="collapsed"
            )
            st.session_state["cevaplar"][soru["id"]] = soru["secenekler"][secim]["stil"]

        if st.form_submit_button("Testi Tamamla", type="primary"):
            st.session_state["test_asamasi"] = "sonuc"
            st.rerun()


def _hizli_okuma_akisi(modul):
    """Hızlı okuma testi akışı"""
    from testler.hizli_okuma import OKUMA_METNI, ANLAMA_SORULARI

    if not st.session_state.get("okuma_bitti", False):
        # Okuma aşaması
        st.markdown("#### Aşağıdaki metni dikkatlice okuyun")
        st.info("Okuma süreniz ölçülmektedir. Okumayı bitirdiğinizde butona tıklayın.")

        if st.session_state.get("okuma_baslangic") is None:
            st.session_state["okuma_baslangic"] = time.time()

        st.markdown(f"""
        <div class="rapor-bolumu" style="font-size: 14px; line-height: 1.8;">
            <h4>{OKUMA_METNI['baslik']}</h4>
            <p>{OKUMA_METNI['metin']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Okudum, Sorulara Geç", type="primary"):
            st.session_state["okuma_suresi"] = time.time() - st.session_state["okuma_baslangic"]
            st.session_state["okuma_bitti"] = True
            st.rerun()
    else:
        # Anlama soruları
        st.markdown("#### Anlama Soruları")
        st.caption(f"Okuma süreniz: {st.session_state.get('okuma_suresi', 0):.1f} saniye")

        with st.form("okuma_sorulari"):
            for soru in ANLAMA_SORULARI:
                st.markdown(f"**{soru['id']}.** {soru['metin']}")
                secim = st.radio(
                    f"Soru {soru['id']}",
                    options=soru["secenekler"],
                    key=f"okuma_{soru['id']}",
                    label_visibility="collapsed"
                )
                st.session_state["cevaplar"][soru["id"]] = secim

            if st.form_submit_button("Sonuçları Gör", type="primary"):
                st.session_state["test_asamasi"] = "sonuc"
                st.rerun()


def _dikkat_testi_akisi(modul):
    """P2 Dikkat testi akışı"""
    st.markdown("#### P2 Dikkat Testi")
    st.info("""
    **Talimat:** Aşağıdaki satırlarda **d** harflerinden **toplamda 2 işareti** olanları bulun ve işaretleyin.
    - d'' (iki üst işaret) = HEDEF
    - d.. (iki alt işaret) = HEDEF
    - d'. (bir üst bir alt) = HEDEF
    - p harfli olanlar ve 2'den farklı işaretli d'ler HEDEF DEĞİL
    """)

    satirlar = st.session_state.get("dikkat_satirlar", [])
    if not satirlar:
        from testler.dikkat import _stimulus_olustur
        satirlar = _stimulus_olustur()
        st.session_state["dikkat_satirlar"] = satirlar
        st.session_state["dikkat_baslangic"] = time.time()

    with st.form("dikkat_formu"):
        for satir_idx, satir in enumerate(satirlar):
            st.markdown(f"**Satır {satir_idx + 1}**")
            cols = st.columns(len(satir))
            for stim_idx, stim in enumerate(satir):
                with cols[stim_idx]:
                    anahtar = f"{satir_idx}_{stim_idx}"
                    isaretlendi = st.checkbox(
                        stim["gosterim"],
                        key=f"dikkat_{anahtar}",
                        label_visibility="visible"
                    )
                    if isaretlendi:
                        st.session_state["cevaplar"][anahtar] = True

        if st.form_submit_button("Testi Bitir", type="primary"):
            st.session_state["dikkat_sure"] = time.time() - st.session_state.get("dikkat_baslangic", time.time())
            st.session_state["test_asamasi"] = "sonuc"
            st.rerun()


def _test_sonuclari_goster(test_key, modul, ogrenci_adi):
    """Test sonuçlarını hesapla ve göster"""
    test_bilgi = TEST_MODULLERI[test_key]

    baslik_goster(f"Sonuçlar: {test_bilgi['ad']}")
    st.markdown(f"**Öğrenci:** {ogrenci_adi}")
    st.markdown("---")

    # Sonuçları hesapla
    cevaplar = st.session_state["cevaplar"]

    if test_key == "hizli_okuma":
        okuma_suresi = st.session_state.get("okuma_suresi", 60)
        sonuclar = modul.hesapla(okuma_suresi, cevaplar)
    elif test_key == "dikkat":
        sure = st.session_state.get("dikkat_sure", 120)
        satirlar = st.session_state.get("dikkat_satirlar", [])
        sonuclar = modul.hesapla(cevaplar, sure, satirlar)
    else:
        sonuclar = modul.hesapla(cevaplar)

    st.session_state["sonuclar"] = sonuclar

    # Sonuçları göster
    modul.sonuc_goster(sonuclar)

    # Test sonucunu kaydet
    ogrenci_id = st.session_state["ogrenci_bilgi"].get("ad", "default")
    if ogrenci_id not in st.session_state["tum_test_sonuclari"]:
        st.session_state["tum_test_sonuclari"][ogrenci_id] = {}
    st.session_state["tum_test_sonuclari"][ogrenci_id][test_bilgi["ad"]] = sonuclar

    # Veritabanına kaydet
    try:
        from veritabani import test_sonucu_kaydet
        db_ogrenci_id = st.session_state["ogrenci_bilgi"].get("id")
        if db_ogrenci_id:
            test_sonucu_kaydet(db_ogrenci_id, test_key, cevaplar, sonuclar, sonuclar)
    except Exception:
        pass

    st.markdown("---")

    # Rapor indirme butonları
    col1, col2 = st.columns(2)
    with col1:
        from rapor_olusturucu import pdf_olustur
        grafik_verileri = _grafik_verisi_hazirla(test_key, sonuclar)
        pdf_data = pdf_olustur(ogrenci_adi, test_bilgi["ad"], sonuclar, grafik_verileri)
        st.download_button(
            "PDF Rapor İndir",
            data=pdf_data,
            file_name=f"{ogrenci_adi}_{test_key}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
    with col2:
        from rapor_olusturucu import docx_olustur
        docx_data = docx_olustur(ogrenci_adi, test_bilgi["ad"], sonuclar, grafik_verileri)
        st.download_button(
            "DOCX Rapor İndir",
            data=docx_data,
            file_name=f"{ogrenci_adi}_{test_key}_{datetime.now().strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    st.markdown("---")

    # AI Analiz
    st.markdown("### AI Analiz")
    col_ai1, col_ai2 = st.columns(2)

    with col_ai1:
        if st.button("Tekli AI Analiz", type="primary"):
            with st.spinner("AI analiz yapılıyor..."):
                from ai_analiz import tekli_analiz
                analiz = tekli_analiz(ogrenci_adi, test_bilgi["ad"], sonuclar)
                if analiz:
                    st.session_state["ai_analiz_sonucu"] = analiz

    with col_ai2:
        # Çoklu analiz (birden fazla test yapılmışsa)
        tum_sonuclar = st.session_state["tum_test_sonuclari"].get(ogrenci_id, {})
        if len(tum_sonuclar) > 1:
            if st.button("Çoklu AI Analiz (Tüm Testler)"):
                with st.spinner("Çoklu AI analiz yapılıyor..."):
                    from ai_analiz import coklu_analiz
                    analiz = coklu_analiz(ogrenci_adi, tum_sonuclar)
                    if analiz:
                        st.session_state["ai_analiz_sonucu"] = analiz

    # AI analiz sonucu gösterimi
    if st.session_state.get("ai_analiz_sonucu"):
        st.markdown("---")
        st.markdown("### AI Değerlendirme Raporu")
        st.markdown(st.session_state["ai_analiz_sonucu"])

        # Aile Bilgilendirme Modülü
        yapilan_testler = list(
            k for k, v in TEST_MODULLERI.items()
            if v["ad"] in st.session_state["tum_test_sonuclari"].get(ogrenci_id, {})
        )

        from aile_bilgilendirme import aile_bilgilendirme_goster
        aile_bilgilendirme_goster(
            ogrenci_adi=ogrenci_adi,
            analiz_sonuclari=st.session_state["ai_analiz_sonucu"],
            yapilan_testler=yapilan_testler if yapilan_testler else [test_key],
            ogrenci_id=st.session_state["ogrenci_bilgi"].get("id"),
            ogretmen_id=st.session_state.get("ogretmen", {}).get("id")
        )

    # Yeni test butonu
    st.markdown("---")
    col_yeni1, col_yeni2 = st.columns(2)
    with col_yeni1:
        if st.button("Başka Test Yap", use_container_width=True):
            st.session_state["secili_test"] = None
            st.session_state["test_asamasi"] = "bilgi"
            st.session_state["cevaplar"] = {}
            st.session_state["sonuclar"] = None
            st.session_state["ai_analiz_sonucu"] = None
            st.session_state["aile_ozet_metni"] = None
            st.session_state["sayfa"] = "test_secim"
            st.rerun()
    with col_yeni2:
        if st.button("Ana Sayfaya Dön", use_container_width=True):
            st.session_state["sayfa"] = "ana_sayfa"
            st.rerun()


def _grafik_verisi_hazirla(test_key, sonuclar):
    """Test sonuçlarından grafik verisi hazırla"""
    grafik_verileri = []

    if test_key == "enneagram":
        tip_yuzdeleri = sonuclar.get("tip_yuzdeleri", {})
        from testler.enneagram import TIPLER
        etiketler = [TIPLER[t]["ad"].split("(")[0].strip() for t in sorted(tip_yuzdeleri.keys())]
        degerler = [tip_yuzdeleri[t] for t in sorted(tip_yuzdeleri.keys())]
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": "Enneagram Profili", "tip": "radar"})

    elif test_key == "vark":
        from testler.vark import STILLER
        stil_yuzdeleri = sonuclar.get("stil_yuzdeleri", {})
        etiketler = [STILLER[s]["ad"] for s in stil_yuzdeleri]
        degerler = list(stil_yuzdeleri.values())
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": "VARK Profili", "tip": "radar"})

    elif test_key == "holland":
        from testler.holland import TIPLER as H_TIPLER
        tip_yuzdeleri = sonuclar.get("tip_yuzdeleri", {})
        etiketler = [H_TIPLER[t]["ad"].split("(")[0].strip() for t in tip_yuzdeleri]
        degerler = list(tip_yuzdeleri.values())
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": "RIASEC Profili", "tip": "radar"})

    elif test_key == "coklu_zeka":
        from testler.coklu_zeka import ZEKA_TURLERI
        zeka_yuzdeleri = sonuclar.get("zeka_yuzdeleri", {})
        etiketler = [ZEKA_TURLERI[z]["ad"].split("(")[0].strip()[:12] for z in zeka_yuzdeleri]
        degerler = list(zeka_yuzdeleri.values())
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": "Çoklu Zekâ Profili", "tip": "radar"})

    elif test_key == "beyin":
        etiketler = ["Sol Beyin", "Sağ Beyin"]
        degerler = [sonuclar.get("sol_yuzde", 0), sonuclar.get("sag_yuzde", 0)]
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": "Beyin Dominansı", "tip": "cubuk"})

    elif test_key in ("sinav_kaygisi", "calisma_davranisi", "akademik_analiz"):
        boyut_yuzdeleri = sonuclar.get("boyut_yuzdeleri", {})
        if test_key == "sinav_kaygisi":
            from testler.sinav_kaygisi import BOYUTLAR
        elif test_key == "calisma_davranisi":
            from testler.calisma_davranisi import BOYUTLAR
        else:
            from testler.akademik_analiz import BOYUTLAR
        etiketler = [BOYUTLAR[b]["ad"] for b in boyut_yuzdeleri]
        degerler = list(boyut_yuzdeleri.values())
        grafik_verileri.append({"etiketler": etiketler, "degerler": degerler, "baslik": TEST_MODULLERI[test_key]["ad"], "tip": "cubuk"})

    return grafik_verileri


# --- Öğretmen Paneli Sayfası ---
def ogretmen_paneli_sayfasi():
    baslik_goster("Öğretmen Paneli")

    if not st.session_state.get("ogretmen_giris"):
        from ogretmen_paneli import ogretmen_giris_formu
        ogretmen_giris_formu()
        return

    ogretmen = st.session_state["ogretmen"]
    st.success(f"Giriş yapıldı: {ogretmen.get('ad', '')} {ogretmen.get('soyad', '')}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Öğrenci Yönetimi", "Test Sonuçları", "AI Analiz", "Toplu İndirme", "Veritabanı Kurulumu"
    ])

    with tab1:
        from ogretmen_paneli import ogrenci_yonetimi
        ogrenci_yonetimi()

    with tab2:
        _ogretmen_test_sonuclari()

    with tab3:
        _ogretmen_ai_analiz()

    with tab4:
        from ogretmen_paneli import toplu_export
        toplu_export()

    with tab5:
        _veritabani_kurulum_paneli()

    st.markdown("---")
    if st.button("Çıkış Yap"):
        st.session_state["ogretmen_giris"] = False
        st.session_state["ogretmen"] = None
        st.rerun()


def _veritabani_kurulum_paneli():
    """Veritabanı kurulum ve durum paneli"""
    st.markdown("### Veritabanı Kurulumu")

    from veritabani import tablolar_mevcut_mu, tablolari_olustur

    # Mevcut durum kontrolü
    mevcut = tablolar_mevcut_mu()
    beklenen = ["ogretmenler", "ogrenciler", "test_sonuclari", "ai_analizler", "aile_ozetleri"]

    if mevcut is None:
        st.warning("Veritabanına bağlanılamadı. DATABASE_URL ayarını kontrol edin.")
        st.code("DATABASE_URL=postgresql://user:pass@host:5432/postgres", language="bash")
    else:
        st.markdown("#### Tablo Durumu")
        for tablo in beklenen:
            if tablo in mevcut:
                st.write(f"  {tablo}")
            else:
                st.write(f"  {tablo} (eksik)")

        eksik = [t for t in beklenen if t not in mevcut]
        if not eksik:
            st.success(f"Tüm tablolar mevcut ({len(mevcut)}/5)")
        else:
            st.warning(f"{len(eksik)} tablo eksik: {', '.join(eksik)}")

    # Kurulum butonu
    if st.button("Tabloları Oluştur / Güncelle", type="primary"):
        with st.spinner("Tablolar oluşturuluyor..."):
            basarili, mesaj = tablolari_olustur()
            if basarili:
                st.success(mesaj)
                st.session_state["db_kurulum_yapildi"] = True
                st.rerun()
            else:
                st.error(mesaj)


def _ogretmen_test_sonuclari():
    """Öğretmen panelinde test sonuçlarını göster"""
    st.markdown("### Test Sonuçları")

    ogrenciler = st.session_state.get("ogrenciler", [])
    tum_sonuclar = st.session_state.get("tum_test_sonuclari", {})

    if not tum_sonuclar:
        st.info("Henüz test sonucu bulunmuyor.")
        return

    for ogrenci_id, testler in tum_sonuclar.items():
        with st.expander(f"Öğrenci: {ogrenci_id}"):
            for test_adi, sonuc in testler.items():
                st.markdown(f"**{test_adi}**")
                if isinstance(sonuc, dict):
                    for k, v in sonuc.items():
                        if not isinstance(v, (list, dict)):
                            st.write(f"- {k}: {v}")
                st.markdown("---")


def _ogretmen_ai_analiz():
    """Öğretmen panelinde AI analiz"""
    st.markdown("### AI Analiz")

    ogrenciler = st.session_state.get("ogrenciler", [])
    tum_sonuclar = st.session_state.get("tum_test_sonuclari", {})

    if not tum_sonuclar:
        st.info("AI analiz için önce test sonuçları gereklidir.")
        return

    secili_ogrenci = st.selectbox(
        "Öğrenci Seçin",
        options=list(tum_sonuclar.keys())
    )

    if secili_ogrenci:
        testler = tum_sonuclar[secili_ogrenci]
        st.write(f"Yapılan testler: {', '.join(testler.keys())}")

        col1, col2 = st.columns(2)
        with col1:
            secili_test = st.selectbox("Test Seçin", options=list(testler.keys()))
            if st.button("Tekli Analiz", key="ogretmen_tekli"):
                with st.spinner("AI analiz yapılıyor..."):
                    from ai_analiz import tekli_analiz
                    analiz = tekli_analiz(secili_ogrenci, secili_test, testler[secili_test])
                    if analiz:
                        st.session_state["ai_analiz_sonucu"] = analiz

        with col2:
            if len(testler) > 1:
                if st.button("Çoklu Analiz (Tüm Testler)", key="ogretmen_coklu"):
                    with st.spinner("Çoklu AI analiz yapılıyor..."):
                        from ai_analiz import coklu_analiz
                        analiz = coklu_analiz(secili_ogrenci, testler)
                        if analiz:
                            st.session_state["ai_analiz_sonucu"] = analiz

        if st.session_state.get("ai_analiz_sonucu"):
            st.markdown("---")
            st.markdown("### AI Değerlendirme Raporu")
            st.markdown(st.session_state["ai_analiz_sonucu"])

            # Aile Bilgilendirme butonu
            yapilan_testler = list(
                k for k, v in TEST_MODULLERI.items()
                if v["ad"] in testler
            )

            from aile_bilgilendirme import aile_bilgilendirme_goster
            aile_bilgilendirme_goster(
                ogrenci_adi=secili_ogrenci,
                analiz_sonuclari=st.session_state["ai_analiz_sonucu"],
                yapilan_testler=yapilan_testler,
                ogretmen_id=st.session_state.get("ogretmen", {}).get("id")
            )


# --- Sayfa Yönlendirme ---
sayfa = st.session_state.get("sayfa", "ana_sayfa")

if sayfa == "ana_sayfa":
    ana_sayfa()
elif sayfa == "test_secim":
    test_secim_sayfasi()
elif sayfa == "test_uygula":
    test_uygulama_sayfasi()
elif sayfa == "ogretmen_paneli":
    ogretmen_paneli_sayfasi()
else:
    ana_sayfa()
