# -*- coding: utf-8 -*-
"""Sağ-Sol Beyin Dominansı Testi Modülü"""

import streamlit as st

TEST_ADI = "Sağ-Sol Beyin Dominansı"
TEST_ACIKLAMA = "Beyin yarıküre baskınlığınızı ve düşünme stilinizi keşfedin."

YARIKURELER = {
    "sol": {
        "ad": "Sol Beyin Dominansı",
        "aciklama": "Analitik, mantıksal, sıralı ve detay odaklı düşünme. Dil, matematik ve mantık alanlarında güçlü.",
        "ozellikler": ["Analitik düşünme", "Mantıksal yaklaşım", "Detay odaklı", "Planlı çalışma", "Dil becerileri"]
    },
    "sag": {
        "ad": "Sağ Beyin Dominansı",
        "aciklama": "Yaratıcı, sezgisel, bütüncül ve görsel düşünme. Sanat, müzik ve hayal gücü alanlarında güçlü.",
        "ozellikler": ["Yaratıcı düşünme", "Sezgisel yaklaşım", "Bütüncül bakış", "Görsel hafıza", "Hayal gücü"]
    },
    "dengeli": {
        "ad": "Dengeli Beyin Kullanımı",
        "aciklama": "Her iki yarıküreyi de etkili kullanan dengeli bir düşünme stili.",
        "ozellikler": ["Esnek düşünme", "Çok yönlü yaklaşım", "Uyum yeteneği"]
    }
}

SORULAR = [
    {"id": 1, "metin": "Bir problemi çözerken adım adım ilerlerim.", "yari_kure": "sol"},
    {"id": 2, "metin": "Not alırken listeler ve maddeler kullanırım.", "yari_kure": "sol"},
    {"id": 3, "metin": "Zamanı iyi yönetirim ve plan yaparım.", "yari_kure": "sol"},
    {"id": 4, "metin": "Sayılarla ve hesaplamalarla aram iyidir.", "yari_kure": "sol"},
    {"id": 5, "metin": "Yazılı talimatları takip etmekte iyiyimdir.", "yari_kure": "sol"},
    {"id": 6, "metin": "Gramer ve dil kurallarına dikkat ederim.", "yari_kure": "sol"},
    {"id": 7, "metin": "Bir şeyi öğrenirken mantıksal sıraya dikkat ederim.", "yari_kure": "sol"},
    {"id": 8, "metin": "Gerçeklere ve kanıtlara dayalı kararlar veririm.", "yari_kure": "sol"},
    {"id": 9, "metin": "Detayları fark etmekte iyiyimdir.", "yari_kure": "sol"},
    {"id": 10, "metin": "Tek bir konuya odaklanmayı tercih ederim.", "yari_kure": "sol"},
    {"id": 11, "metin": "Sezgilerime güvenirim.", "yari_kure": "sag"},
    {"id": 12, "metin": "Hayal kurmak ve düşünmekten keyif alırım.", "yari_kure": "sag"},
    {"id": 13, "metin": "Renkler ve görsel düzen benim için önemlidir.", "yari_kure": "sag"},
    {"id": 14, "metin": "Müzik dinlerken duygusal olurum.", "yari_kure": "sag"},
    {"id": 15, "metin": "Birden fazla şeyi aynı anda yapabilirim.", "yari_kure": "sag"},
    {"id": 16, "metin": "Yüzleri isimlere göre daha iyi hatırlarım.", "yari_kure": "sag"},
    {"id": 17, "metin": "Yaratıcı çözümler bulmakta iyiyimdir.", "yari_kure": "sag"},
    {"id": 18, "metin": "Not alırken çizimler ve şekiller kullanırım.", "yari_kure": "sag"},
    {"id": 19, "metin": "Beden dili ve ses tonundan çok şey anlarım.", "yari_kure": "sag"},
    {"id": 20, "metin": "Büyük resmi görmeyi, detaylardan önce bütünü anlamayı tercih ederim.", "yari_kure": "sag"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Sağ-Sol beyin puanlarını hesapla"""
    sol_puan = 0
    sag_puan = 0
    sol_sayisi = 0
    sag_sayisi = 0

    for soru in SORULAR:
        soru_id = soru["id"]
        if soru_id in cevaplar:
            if soru["yari_kure"] == "sol":
                sol_puan += cevaplar[soru_id]
                sol_sayisi += 1
            else:
                sag_puan += cevaplar[soru_id]
                sag_sayisi += 1

    sol_yuzde = round((sol_puan / max(sol_sayisi * 5, 1)) * 100, 1)
    sag_yuzde = round((sag_puan / max(sag_sayisi * 5, 1)) * 100, 1)

    fark = abs(sol_yuzde - sag_yuzde)
    if fark <= 10:
        dominant = "dengeli"
    elif sol_yuzde > sag_yuzde:
        dominant = "sol"
    else:
        dominant = "sag"

    return {
        "sol_puan": sol_puan,
        "sag_puan": sag_puan,
        "sol_yuzde": sol_yuzde,
        "sag_yuzde": sag_yuzde,
        "dominant": dominant,
        "dominant_ad": YARIKURELER[dominant]["ad"],
        "dominant_aciklama": YARIKURELER[dominant]["aciklama"],
        "ozellikler": YARIKURELER[dominant]["ozellikler"]
    }


def sonuc_goster(sonuclar):
    """Beyin dominansı sonuçlarını göster"""
    st.markdown(f"### {sonuclar['dominant_ad']}")
    st.info(sonuclar["dominant_aciklama"])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sol Beyin", f"%{sonuclar['sol_yuzde']}")
        st.progress(sonuclar["sol_yuzde"] / 100)
    with col2:
        st.metric("Sağ Beyin", f"%{sonuclar['sag_yuzde']}")
        st.progress(sonuclar["sag_yuzde"] / 100)

    st.markdown("#### Düşünme Özellikleri")
    for oz in sonuclar["ozellikler"]:
        st.write(f"- {oz}")
