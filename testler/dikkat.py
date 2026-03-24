# -*- coding: utf-8 -*-
"""P2 Dikkat Testi Modülü"""

import streamlit as st
import random
import time

TEST_ADI = "P2 Dikkat Testi"
TEST_ACIKLAMA = "Seçici dikkat, sürdürülebilir dikkat ve dikkat dağılma eğiliminizi ölçün."

# P2 testi: Hedef harfleri bulma görevi
# d harflerini bul (p harflerini değil), üstünde/altında 2 işaret olan d'ler hedef
STIMULUSLAR = []

def _stimulus_olustur(satir_sayisi=14, satir_uzunluk=20):
    """P2 test stimuluslarını oluştur"""
    harfler = ["d", "p"]
    isaretler_listesi = ["'", "''", ".", "..", "'.", ".'"]

    satirlar = []
    for _ in range(satir_sayisi):
        satir = []
        for _ in range(satir_uzunluk):
            harf = random.choice(harfler)
            isaret = random.choice(isaretler_listesi)
            # Hedef: d harfi ve toplamda 2 işareti olan
            toplam_isaret = isaret.count("'") + isaret.count(".")
            hedef = (harf == "d" and toplam_isaret == 2)
            satir.append({
                "harf": harf,
                "isaret": isaret,
                "gosterim": f"{harf}{isaret}",
                "hedef": hedef
            })
        satirlar.append(satir)
    return satirlar


def hesapla(yanitlar, sure_saniye, satirlar):
    """P2 dikkat testi puanlarını hesapla"""
    toplam_hedef = 0
    dogru_isaretleme = 0
    yanlis_isaretleme = 0
    kacirilan = 0

    for satir_idx, satir in enumerate(satirlar):
        for stim_idx, stim in enumerate(satir):
            anahtar = f"{satir_idx}_{stim_idx}"
            isaretlendi = anahtar in yanitlar and yanitlar[anahtar]

            if stim["hedef"]:
                toplam_hedef += 1
                if isaretlendi:
                    dogru_isaretleme += 1
                else:
                    kacirilan += 1
            else:
                if isaretlendi:
                    yanlis_isaretleme += 1

    # Puanlama
    toplam_islenen = dogru_isaretleme + yanlis_isaretleme + kacirilan
    konsantrasyon_puani = dogru_isaretleme - yanlis_isaretleme
    hata_yuzdesi = round(((yanlis_isaretleme + kacirilan) / max(toplam_hedef + yanlis_isaretleme, 1)) * 100, 1)
    dikkat_yuzdesi = round((dogru_isaretleme / max(toplam_hedef, 1)) * 100, 1)

    # Seviye belirleme
    if dikkat_yuzdesi >= 80:
        seviye = "Çok İyi"
        aciklama = "Seçici dikkat becerileriniz oldukça güçlü."
    elif dikkat_yuzdesi >= 60:
        seviye = "İyi"
        aciklama = "Dikkat becerileriniz iyi düzeyde."
    elif dikkat_yuzdesi >= 40:
        seviye = "Orta"
        aciklama = "Dikkat becerileriniz geliştirilmeye açık."
    else:
        seviye = "Geliştirilmeli"
        aciklama = "Dikkat becerilerinizin desteklenmesi önerilir."

    return {
        "toplam_hedef": toplam_hedef,
        "dogru_isaretleme": dogru_isaretleme,
        "yanlis_isaretleme": yanlis_isaretleme,
        "kacirilan": kacirilan,
        "konsantrasyon_puani": konsantrasyon_puani,
        "hata_yuzdesi": hata_yuzdesi,
        "dikkat_yuzdesi": dikkat_yuzdesi,
        "sure_saniye": round(sure_saniye, 1),
        "seviye": seviye,
        "aciklama": aciklama
    }


def sonuc_goster(sonuclar):
    """P2 dikkat testi sonuçlarını göster"""
    st.markdown(f"### Dikkat Seviyeniz: **{sonuclar['seviye']}**")
    st.info(sonuclar["aciklama"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Doğru", f"{sonuclar['dogru_isaretleme']}/{sonuclar['toplam_hedef']}")
    with col2:
        st.metric("Yanlış", str(sonuclar["yanlis_isaretleme"]))
    with col3:
        st.metric("Kaçırılan", str(sonuclar["kacirilan"]))
    with col4:
        st.metric("Süre", f"{sonuclar['sure_saniye']}s")

    st.progress(sonuclar["dikkat_yuzdesi"] / 100, text=f"Dikkat Doğruluğu: %{sonuclar['dikkat_yuzdesi']}")

    st.markdown(f"**Konsantrasyon Puanı:** {sonuclar['konsantrasyon_puani']}")
    st.markdown(f"**Hata Oranı:** %{sonuclar['hata_yuzdesi']}")
