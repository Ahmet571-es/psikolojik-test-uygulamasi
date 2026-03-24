# -*- coding: utf-8 -*-
"""Akademik Başarı Analizi Modülü"""

import streamlit as st

TEST_ADI = "Akademik Başarı Analizi"
TEST_ACIKLAMA = "Ders bazında güçlü ve zayıf yönlerinizi, çalışma stratejilerinizi değerlendirin."

BOYUTLAR = {
    "sayisal": {"ad": "Sayısal Yatkınlık", "aciklama": "Matematik, fen ve sayısal düşünme becerileri."},
    "sozel": {"ad": "Sözel Yatkınlık", "aciklama": "Türkçe, edebiyat ve sözel ifade becerileri."},
    "yabanci_dil": {"ad": "Yabancı Dil Yatkınlığı", "aciklama": "İngilizce ve yabancı dil öğrenme becerileri."},
    "sosyal": {"ad": "Sosyal Bilimler", "aciklama": "Tarih, coğrafya ve sosyal bilimler alanına ilgi."},
    "oz_duzenleme": {"ad": "Öz Düzenleme", "aciklama": "Kendi öğrenmesini yönetme ve düzenleme becerisi."},
    "hedef": {"ad": "Hedef Odaklılık", "aciklama": "Akademik hedef belirleme ve takip etme."}
}

SORULAR = [
    {"id": 1, "metin": "Matematik problemlerini çözmekten keyif alırım.", "boyut": "sayisal"},
    {"id": 2, "metin": "Fen derslerindeki deneyleri severim.", "boyut": "sayisal"},
    {"id": 3, "metin": "Formülleri ve hesaplamaları anlamakta zorlanmam.", "boyut": "sayisal"},
    {"id": 4, "metin": "Geometrik şekilleri ve uzamsal problemleri çözmekte iyiyimdir.", "boyut": "sayisal"},
    {"id": 5, "metin": "Sayısal verileri analiz etmek ilgimi çeker.", "boyut": "sayisal"},
    {"id": 6, "metin": "Kompozisyon yazmakta başarılıyımdır.", "boyut": "sozel"},
    {"id": 7, "metin": "Okuduğum metinleri kolayca anlarım.", "boyut": "sozel"},
    {"id": 8, "metin": "Dilbilgisi kurallarını bilir ve uygularım.", "boyut": "sozel"},
    {"id": 9, "metin": "Şiir ve edebiyat eserlerini okumayı severim.", "boyut": "sozel"},
    {"id": 10, "metin": "Düşüncelerimi sözlü olarak rahatça ifade ederim.", "boyut": "sozel"},
    {"id": 11, "metin": "İngilizce kelime öğrenmek bana kolay gelir.", "boyut": "yabanci_dil"},
    {"id": 12, "metin": "Yabancı dilde film veya dizi izlemeyi severim.", "boyut": "yabanci_dil"},
    {"id": 13, "metin": "İngilizce metinleri anlamaya çalışırım.", "boyut": "yabanci_dil"},
    {"id": 14, "metin": "Yeni bir dil öğrenmeye meraklıyımdır.", "boyut": "yabanci_dil"},
    {"id": 15, "metin": "Tarih dersi ilgimi çeker.", "boyut": "sosyal"},
    {"id": 16, "metin": "Toplumsal olayları takip ederim.", "boyut": "sosyal"},
    {"id": 17, "metin": "Farklı kültürleri öğrenmek hoşuma gider.", "boyut": "sosyal"},
    {"id": 18, "metin": "Coğrafya ve haritalar ilgimi çeker.", "boyut": "sosyal"},
    {"id": 19, "metin": "Sınavlardan sonra hatalarımı analiz ederim.", "boyut": "oz_duzenleme"},
    {"id": 20, "metin": "Anlamadığım konuları araştırırım.", "boyut": "oz_duzenleme"},
    {"id": 21, "metin": "Kendi öğrenme yöntemimi bilirim.", "boyut": "oz_duzenleme"},
    {"id": 22, "metin": "Ders notlarımı düzenli tutarım.", "boyut": "oz_duzenleme"},
    {"id": 23, "metin": "Net hedeflerim vardır (üniversite, meslek vb.).", "boyut": "hedef"},
    {"id": 24, "metin": "Hangi mesleği seçeceğimi biliyorum.", "boyut": "hedef"},
    {"id": 25, "metin": "Akademik başarım için plan yaparım.", "boyut": "hedef"},
    {"id": 26, "metin": "Gelecek planlarım motivasyonumu artırır.", "boyut": "hedef"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Akademik analiz puanlarını hesapla"""
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

    sirali = sorted(boyut_yuzdeleri.items(), key=lambda x: x[1], reverse=True)

    # Alan yatkınlığı belirleme
    sayisal = boyut_yuzdeleri.get("sayisal", 0)
    sozel = boyut_yuzdeleri.get("sozel", 0)
    if abs(sayisal - sozel) <= 10:
        yatkinlik = "Eşit Ağırlık"
    elif sayisal > sozel:
        yatkinlik = "Sayısal"
    else:
        yatkinlik = "Sözel"

    return {
        "boyut_puanlari": boyut_puanlari,
        "boyut_yuzdeleri": boyut_yuzdeleri,
        "sirali_boyutlar": sirali,
        "alan_yatkinligi": yatkinlik,
        "guclu_alanlar": [b for b, y in boyut_yuzdeleri.items() if y >= 70],
        "gelisim_alanlari": [b for b, y in boyut_yuzdeleri.items() if y < 50]
    }


def sonuc_goster(sonuclar):
    """Akademik analiz sonuçlarını göster"""
    st.markdown(f"### Alan Yatkınlığınız: **{sonuclar['alan_yatkinligi']}**")

    st.markdown("#### Akademik Profil")
    for boyut, yuzde in sonuclar["sirali_boyutlar"]:
        st.progress(yuzde / 100, text=f"{BOYUTLAR[boyut]['ad']}: %{yuzde}")

    if sonuclar["guclu_alanlar"]:
        st.markdown("#### Güçlü Alanlar")
        for b in sonuclar["guclu_alanlar"]:
            st.success(f"{BOYUTLAR[b]['ad']}")

    if sonuclar["gelisim_alanlari"]:
        st.markdown("#### Gelişim Alanları")
        for b in sonuclar["gelisim_alanlari"]:
            st.warning(f"{BOYUTLAR[b]['ad']}")
