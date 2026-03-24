# -*- coding: utf-8 -*-
"""Çalışma Davranışı Değerlendirmesi Modülü"""

import streamlit as st

TEST_ADI = "Çalışma Davranışı Değerlendirmesi"
TEST_ACIKLAMA = "Çalışma alışkanlıklarınızı ve verimlilik düzeyinizi analiz edin."

BOYUTLAR = {
    "planlama": {"ad": "Planlama ve Organizasyon", "aciklama": "Çalışmayı planlama ve zamanı yönetme becerisi."},
    "motivasyon": {"ad": "Motivasyon", "aciklama": "İç motivasyon, hedef belirleme ve kararlılık."},
    "konsantrasyon": {"ad": "Konsantrasyon", "aciklama": "Dikkat toplama ve odaklanma becerisi."},
    "strateji": {"ad": "Çalışma Stratejisi", "aciklama": "Etkili öğrenme yöntemlerini kullanma becerisi."},
    "ortam": {"ad": "Çalışma Ortamı", "aciklama": "Uygun çalışma ortamı oluşturma ve sürdürme."}
}

SORULAR = [
    {"id": 1, "metin": "Her gün belirli saatlerde ders çalışırım.", "boyut": "planlama"},
    {"id": 2, "metin": "Haftalık çalışma programım vardır.", "boyut": "planlama"},
    {"id": 3, "metin": "Sınavlara en az bir hafta önceden başlarım.", "boyut": "planlama"},
    {"id": 4, "metin": "Ödevlerimi zamanında teslim ederim.", "boyut": "planlama"},
    {"id": 5, "metin": "Hedeflerimi belirler ve takip ederim.", "boyut": "planlama"},
    {"id": 6, "metin": "Ders çalışmayı isteyerek yaparım.", "boyut": "motivasyon"},
    {"id": 7, "metin": "Başarılı olmak beni motive eder.", "boyut": "motivasyon"},
    {"id": 8, "metin": "Zor konuları öğrenmek beni heyecanlandırır.", "boyut": "motivasyon"},
    {"id": 9, "metin": "Hedeflerime ulaşmak için çaba gösteririm.", "boyut": "motivasyon"},
    {"id": 10, "metin": "Başarısız olsam bile tekrar denerim.", "boyut": "motivasyon"},
    {"id": 11, "metin": "Ders çalışırken dikkatimi kolayca toplarım.", "boyut": "konsantrasyon"},
    {"id": 12, "metin": "Uzun süre odaklanabilirim.", "boyut": "konsantrasyon"},
    {"id": 13, "metin": "Çalışırken telefonuma bakmam.", "boyut": "konsantrasyon"},
    {"id": 14, "metin": "Gürültülü ortamda bile çalışabilirim.", "boyut": "konsantrasyon"},
    {"id": 15, "metin": "Ders çalışırken hayal kurmam.", "boyut": "konsantrasyon"},
    {"id": 16, "metin": "Not alarak çalışırım.", "boyut": "strateji"},
    {"id": 17, "metin": "Konuyu anladıktan sonra tekrar ederim.", "boyut": "strateji"},
    {"id": 18, "metin": "Özet çıkararak çalışırım.", "boyut": "strateji"},
    {"id": 19, "metin": "Konuları birbirine bağlayarak çalışırım.", "boyut": "strateji"},
    {"id": 20, "metin": "Farklı kaynaklardan çalışırım.", "boyut": "strateji"},
    {"id": 21, "metin": "Sessiz bir ortamda çalışırım.", "boyut": "ortam"},
    {"id": 22, "metin": "Çalışma masam düzenlidir.", "boyut": "ortam"},
    {"id": 23, "metin": "Yeterli aydınlatma olan bir yerde çalışırım.", "boyut": "ortam"},
    {"id": 24, "metin": "Çalışma materyallerimi düzenli tutarım.", "boyut": "ortam"},
    {"id": 25, "metin": "Çalışma sırasında molalar veririm.", "boyut": "ortam"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Çalışma davranışı puanlarını hesapla"""
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

    guclu = [b for b, y in boyut_yuzdeleri.items() if y >= 70]
    gelisim = [b for b, y in boyut_yuzdeleri.items() if y < 50]

    return {
        "boyut_puanlari": boyut_puanlari,
        "boyut_yuzdeleri": boyut_yuzdeleri,
        "toplam_yuzde": toplam_yuzde,
        "guclu_alanlar": guclu,
        "gelisim_alanlari": gelisim
    }


def sonuc_goster(sonuclar):
    """Çalışma davranışı sonuçlarını göster"""
    st.markdown(f"### Genel Çalışma Verimliliği: %{sonuclar['toplam_yuzde']}")
    st.progress(sonuclar["toplam_yuzde"] / 100)

    if sonuclar["guclu_alanlar"]:
        st.markdown("#### Güçlü Alanlar")
        for b in sonuclar["guclu_alanlar"]:
            st.success(f"{BOYUTLAR[b]['ad']}: %{sonuclar['boyut_yuzdeleri'][b]}")

    if sonuclar["gelisim_alanlari"]:
        st.markdown("#### Gelişim Alanları")
        for b in sonuclar["gelisim_alanlari"]:
            st.warning(f"{BOYUTLAR[b]['ad']}: %{sonuclar['boyut_yuzdeleri'][b]}")

    st.markdown("#### Boyut Dağılımı")
    for boyut, yuzde in sonuclar["boyut_yuzdeleri"].items():
        st.progress(yuzde / 100, text=f"{BOYUTLAR[boyut]['ad']}: %{yuzde}")
