# -*- coding: utf-8 -*-
"""Çoklu Zekâ Testi (Gardner) Modülü"""

import streamlit as st

TEST_ADI = "Çoklu Zekâ Testi (Gardner)"
TEST_ACIKLAMA = "8 farklı zekâ alanındaki güçlü ve gelişime açık yönlerinizi belirleyin."

ZEKA_TURLERI = {
    "sozel": {"ad": "Sözel-Dilsel Zekâ", "aciklama": "Kelimelerle düşünme, okuma, yazma ve konuşma becerisi."},
    "mantiksal": {"ad": "Mantıksal-Matematiksel Zekâ", "aciklama": "Sayılar, mantık ve soyut düşünme becerisi."},
    "gorsel": {"ad": "Görsel-Uzamsal Zekâ", "aciklama": "Resimlerle düşünme, hayal gücü ve mekânsal algı."},
    "bedensel": {"ad": "Bedensel-Kinestetik Zekâ", "aciklama": "Vücut kullanarak öğrenme ve ifade etme becerisi."},
    "muziksel": {"ad": "Müziksel-Ritmik Zekâ", "aciklama": "Ritim, melodi ve seslerle düşünme becerisi."},
    "sosyal": {"ad": "Sosyal (Kişilerarası) Zekâ", "aciklama": "İnsanları anlama, iletişim ve empati becerisi."},
    "icisel": {"ad": "İçsel (Öze Dönük) Zekâ", "aciklama": "Kendini tanıma, duygusal farkındalık ve öz-yönetim."},
    "dogasal": {"ad": "Doğa Zekâsı", "aciklama": "Doğayı gözlemleme, sınıflandırma ve doğal dünyayı anlama."}
}

SORULAR = [
    {"id": 1, "metin": "Kitap okumak en sevdiğim aktivitelerden biridir.", "zeka": "sozel"},
    {"id": 2, "metin": "Yeni kelimeler öğrenmeyi ve kullanmayı severim.", "zeka": "sozel"},
    {"id": 3, "metin": "Düşüncelerimi yazıyla ifade etmekte iyiyimdir.", "zeka": "sozel"},
    {"id": 4, "metin": "Kelime oyunları ve bulmacalar ilgimi çeker.", "zeka": "sozel"},
    {"id": 5, "metin": "Matematik problemlerini çözmekten keyif alırım.", "zeka": "mantiksal"},
    {"id": 6, "metin": "Mantık bulmacaları ve strateji oyunları severim.", "zeka": "mantiksal"},
    {"id": 7, "metin": "Olaylar arasında neden-sonuç ilişkisi kurmakta iyiyimdir.", "zeka": "mantiksal"},
    {"id": 8, "metin": "Sayılarla ve istatistiklerle ilgilenmek hoşuma gider.", "zeka": "mantiksal"},
    {"id": 9, "metin": "Zihnimde kolayca resimler ve görüntüler oluşturabilirim.", "zeka": "gorsel"},
    {"id": 10, "metin": "Harita okumak ve yön bulmak benim için kolaydır.", "zeka": "gorsel"},
    {"id": 11, "metin": "Resim yapmak, çizmek veya tasarım yapmak hoşuma gider.", "zeka": "gorsel"},
    {"id": 12, "metin": "Renklere ve görsel detaylara dikkat ederim.", "zeka": "gorsel"},
    {"id": 13, "metin": "Spor yapmak ve fiziksel aktiviteler beni enerjik yapar.", "zeka": "bedensel"},
    {"id": 14, "metin": "El işi, maket yapma gibi aktivitelerden keyif alırım.", "zeka": "bedensel"},
    {"id": 15, "metin": "Dans etmek veya beden diliyle ifade olmakta iyiyimdir.", "zeka": "bedensel"},
    {"id": 16, "metin": "Uzun süre hareketsiz oturmak bana zor gelir.", "zeka": "bedensel"},
    {"id": 17, "metin": "Müzik dinlemek ruh halimi çok etkiler.", "zeka": "muziksel"},
    {"id": 18, "metin": "Bir müzik aletini çalmak isterim veya çalıyorum.", "zeka": "muziksel"},
    {"id": 19, "metin": "Ritimleri ve melodileri kolayca yakalarım.", "zeka": "muziksel"},
    {"id": 20, "metin": "Çalışırken müzik dinlemek beni daha verimli yapar.", "zeka": "muziksel"},
    {"id": 21, "metin": "Arkadaş edinmek benim için kolaydır.", "zeka": "sosyal"},
    {"id": 22, "metin": "Grup çalışmalarında liderlik etmeyi severim.", "zeka": "sosyal"},
    {"id": 23, "metin": "İnsanların duygularını kolayca anlarım.", "zeka": "sosyal"},
    {"id": 24, "metin": "Arkadaşlarım sorunlarını benimle paylaşır.", "zeka": "sosyal"},
    {"id": 25, "metin": "Kendi duygularımı tanımakta iyiyimdir.", "zeka": "icisel"},
    {"id": 26, "metin": "Yalnız çalışmayı tercih ederim.", "zeka": "icisel"},
    {"id": 27, "metin": "Güçlü ve zayıf yönlerimi bilirim.", "zeka": "icisel"},
    {"id": 28, "metin": "Günlük tutmak veya kendi kendime düşünmek hoşuma gider.", "zeka": "icisel"},
    {"id": 29, "metin": "Doğada vakit geçirmek beni mutlu eder.", "zeka": "dogasal"},
    {"id": 30, "metin": "Bitki ve hayvanlarla ilgilenmekten keyif alırım.", "zeka": "dogasal"},
    {"id": 31, "metin": "Doğa olaylarını gözlemlemek ilgimi çeker.", "zeka": "dogasal"},
    {"id": 32, "metin": "Çevre sorunları beni endişelendirir.", "zeka": "dogasal"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Çoklu zekâ puanlarını hesapla"""
    zeka_puanlari = {z: 0 for z in ZEKA_TURLERI}
    zeka_soru_sayisi = {z: 0 for z in ZEKA_TURLERI}

    for soru in SORULAR:
        soru_id = soru["id"]
        zeka = soru["zeka"]
        if soru_id in cevaplar:
            zeka_puanlari[zeka] += cevaplar[soru_id]
            zeka_soru_sayisi[zeka] += 1

    zeka_yuzdeleri = {}
    for zeka in ZEKA_TURLERI:
        if zeka_soru_sayisi[zeka] > 0:
            max_puan = zeka_soru_sayisi[zeka] * 5
            zeka_yuzdeleri[zeka] = round((zeka_puanlari[zeka] / max_puan) * 100, 1)
        else:
            zeka_yuzdeleri[zeka] = 0

    sirali = sorted(zeka_yuzdeleri.items(), key=lambda x: x[1], reverse=True)
    guclu_alanlar = [s for s in sirali if s[1] >= 70]
    gelisim_alanlari = [s for s in sirali if s[1] < 50]

    return {
        "zeka_puanlari": zeka_puanlari,
        "zeka_yuzdeleri": zeka_yuzdeleri,
        "baskin_zeka": sirali[0][0],
        "baskin_zeka_ad": ZEKA_TURLERI[sirali[0][0]]["ad"],
        "guclu_alanlar": guclu_alanlar,
        "gelisim_alanlari": gelisim_alanlari,
        "sirali_zekalar": sirali
    }


def sonuc_goster(sonuclar):
    """Çoklu zekâ sonuçlarını göster"""
    st.markdown(f"### Baskın Zekâ Alanınız: {sonuclar['baskin_zeka_ad']}")
    st.info(ZEKA_TURLERI[sonuclar["baskin_zeka"]]["aciklama"])

    if sonuclar["guclu_alanlar"]:
        st.markdown("#### Güçlü Alanlarınız")
        for zeka, yuzde in sonuclar["guclu_alanlar"]:
            st.success(f"{ZEKA_TURLERI[zeka]['ad']}: %{yuzde}")

    st.markdown("#### Zekâ Dağılımı")
    for zeka, yuzde in sonuclar["sirali_zekalar"]:
        st.progress(yuzde / 100, text=f"{ZEKA_TURLERI[zeka]['ad']}: %{yuzde}")
