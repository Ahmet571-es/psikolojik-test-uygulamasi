# -*- coding: utf-8 -*-
"""Sınav Kaygısı Ölçeği Modülü"""

import streamlit as st

TEST_ADI = "Sınav Kaygısı Ölçeği"
TEST_ACIKLAMA = "Sınav öncesi, sırası ve sonrasındaki kaygı düzeyinizi değerlendirin."

BOYUTLAR = {
    "bilissel": {"ad": "Bilişsel Kaygı", "aciklama": "Sınav hakkındaki olumsuz düşünceler, başarısızlık korkusu."},
    "bedensel": {"ad": "Bedensel Kaygı", "aciklama": "Kalp çarpıntısı, terleme, mide bulantısı gibi fiziksel belirtiler."},
    "duygusal": {"ad": "Duygusal Kaygı", "aciklama": "Gerginlik, sinirlilik, panik hissi."},
    "davranissal": {"ad": "Davranışsal Kaygı", "aciklama": "Kaçınma, erteleme, uyku bozuklukları."}
}

SORULAR = [
    {"id": 1, "metin": "Sınav öncesi gece uyuyamam.", "boyut": "bedensel"},
    {"id": 2, "metin": "Sınav sırasında kalbim çok hızlı atar.", "boyut": "bedensel"},
    {"id": 3, "metin": "Sınav öncesi midem bulanır veya karnım ağrır.", "boyut": "bedensel"},
    {"id": 4, "metin": "Sınav sırasında ellerim terler.", "boyut": "bedensel"},
    {"id": 5, "metin": "Sınav öncesi baş ağrısı çekerim.", "boyut": "bedensel"},
    {"id": 6, "metin": "Sınavda başarısız olacağımı düşünürüm.", "boyut": "bilissel"},
    {"id": 7, "metin": "Sınav sırasında bildiklerimi unutacağımdan korkarım.", "boyut": "bilissel"},
    {"id": 8, "metin": "Diğer öğrencilerin benden daha iyi yapacağını düşünürüm.", "boyut": "bilissel"},
    {"id": 9, "metin": "Sınavda yapamadığım soruları görünce paniklerim.", "boyut": "bilissel"},
    {"id": 10, "metin": "Sınav notlarım zekâmı yansıtmaz diye endişelenirim.", "boyut": "bilissel"},
    {"id": 11, "metin": "Sınav yaklaştıkça gergin ve sinirli olurum.", "boyut": "duygusal"},
    {"id": 12, "metin": "Sınav sırasında panik hissi yaşarım.", "boyut": "duygusal"},
    {"id": 13, "metin": "Sınav sonuçlarını görmeye korkuyorum.", "boyut": "duygusal"},
    {"id": 14, "metin": "Sınav günü kendimi çaresiz hissederim.", "boyut": "duygusal"},
    {"id": 15, "metin": "Sınav stresi nedeniyle ağlamak isterim.", "boyut": "duygusal"},
    {"id": 16, "metin": "Sınav çalışmasını son güne bırakırım.", "boyut": "davranissal"},
    {"id": 17, "metin": "Sınav yaklaşınca ders çalışmak yerine başka şeyler yaparım.", "boyut": "davranissal"},
    {"id": 18, "metin": "Sınav öncesi dikkatimi toplamakta zorlanırım.", "boyut": "davranissal"},
    {"id": 19, "metin": "Sınav için yeterince çalışamam.", "boyut": "davranissal"},
    {"id": 20, "metin": "Sınav döneminde arkadaşlarımdan uzaklaşırım.", "boyut": "davranissal"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}

KAYGI_SEVIYELERI = {
    (0, 30): {"seviye": "Düşük", "renk": "green", "aciklama": "Sınav kaygınız düşük düzeyde. Bu sağlıklı bir durum."},
    (30, 50): {"seviye": "Normal", "renk": "blue", "aciklama": "Sınav kaygınız normal düzeyde. Hafif bir kaygı performansı artırabilir."},
    (50, 70): {"seviye": "Orta-Yüksek", "renk": "orange", "aciklama": "Sınav kaygınız ortanın üzerinde. Baş etme stratejileri geliştirmeniz faydalı olabilir."},
    (70, 101): {"seviye": "Yüksek", "renk": "red", "aciklama": "Sınav kaygınız yüksek düzeyde. Profesyonel destek almanız önerilir."}
}


def hesapla(cevaplar):
    """Sınav kaygısı puanlarını hesapla"""
    boyut_puanlari = {b: 0 for b in BOYUTLAR}
    boyut_soru_sayisi = {b: 0 for b in BOYUTLAR}

    for soru in SORULAR:
        soru_id = soru["id"]
        boyut = soru["boyut"]
        if soru_id in cevaplar:
            boyut_puanlari[boyut] += cevaplar[soru_id]
            boyut_soru_sayisi[boyut] += 1

    boyut_yuzdeleri = {}
    for boyut in BOYUTLAR:
        if boyut_soru_sayisi[boyut] > 0:
            max_puan = boyut_soru_sayisi[boyut] * 5
            boyut_yuzdeleri[boyut] = round((boyut_puanlari[boyut] / max_puan) * 100, 1)
        else:
            boyut_yuzdeleri[boyut] = 0

    toplam_yuzde = round(sum(boyut_yuzdeleri.values()) / max(len(boyut_yuzdeleri), 1), 1)

    # Kaygı seviyesi belirleme
    kaygi_seviyesi = "Normal"
    kaygi_aciklama = ""
    for aralik, bilgi in KAYGI_SEVIYELERI.items():
        if aralik[0] <= toplam_yuzde < aralik[1]:
            kaygi_seviyesi = bilgi["seviye"]
            kaygi_aciklama = bilgi["aciklama"]
            break

    return {
        "boyut_puanlari": boyut_puanlari,
        "boyut_yuzdeleri": boyut_yuzdeleri,
        "toplam_yuzde": toplam_yuzde,
        "kaygi_seviyesi": kaygi_seviyesi,
        "kaygi_aciklama": kaygi_aciklama,
    }


def sonuc_goster(sonuclar):
    """Sınav kaygısı sonuçlarını göster"""
    seviye = sonuclar["kaygi_seviyesi"]
    st.markdown(f"### Kaygı Düzeyiniz: **{seviye}** (%{sonuclar['toplam_yuzde']})")

    if seviye in ("Düşük", "Normal"):
        st.success(sonuclar["kaygi_aciklama"])
    elif seviye == "Orta-Yüksek":
        st.warning(sonuclar["kaygi_aciklama"])
    else:
        st.error(sonuclar["kaygi_aciklama"])

    st.markdown("#### Boyut Analizi")
    for boyut, yuzde in sonuclar["boyut_yuzdeleri"].items():
        st.progress(yuzde / 100, text=f"{BOYUTLAR[boyut]['ad']}: %{yuzde}")
