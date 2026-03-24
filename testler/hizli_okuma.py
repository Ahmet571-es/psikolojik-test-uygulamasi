# -*- coding: utf-8 -*-
"""Hızlı Okuma Değerlendirmesi Modülü"""

import streamlit as st
import time

TEST_ADI = "Hızlı Okuma Değerlendirmesi"
TEST_ACIKLAMA = "Okuma hızınızı ve okuduğunu anlama düzeyinizi ölçün."

# Okuma metinleri (kelime sayısı belirtilmiş)
OKUMA_METNI = {
    "baslik": "Arıların Dünyası",
    "metin": """Arılar, doğanın en çalışkan ve düzenli canlılarından biridir. Bir arı kolonisi, kraliçe arı, işçi arılar ve erkek arılardan oluşur. Kraliçe arı, koloninin tek üreme yeteneğine sahip dişisidir ve günde yaklaşık iki bin yumurta bırakabilir. İşçi arılar ise koloninin tüm işlerini yapar: yiyecek toplar, petek yapar, yavruları besler ve kovana bekçilik eder.

Arılar, çiçeklerden nektar ve polen toplarken bitkilerinin tozlaşmasına yardımcı olur. Bu süreç, tarım için hayati önem taşır. Dünya üzerindeki besin maddelerinin yaklaşık üçte birinin üretimi, arıların tozlaşma faaliyetine bağlıdır. Elmadan çileğe, bademden kahveye kadar pek çok ürün arılara borçludur.

Bal arıları, topladıkları nektarı bala dönüştürür. Nektar, arının midesindeki enzimlerle işlenir ve peteklere depolanır. Arılar kanatlarını çırparak balın suyunu buharlaştırır. Bu süreç sonunda tanıdığımız altın sarısı bal ortaya çıkar. Bir kilogram bal üretmek için arıların yaklaşık dört milyon çiçeği ziyaret etmesi gerekir.

Arılar, dans ederek birbirleriyle iletişim kurar. Keşifçi arı, zengin bir çiçek kaynağı bulduğunda kovana döner ve özel bir dans yapar. Bu dans, diğer arılara çiçeklerin yönünü ve uzaklığını bildirir. Yuvarlak dans yakın mesafeyi, kuyruk sallama dansı ise uzak mesafeyi ifade eder.

Ne yazık ki arı popülasyonları dünya genelinde azalmaktadır. Tarım ilaçları, habitat kaybı ve iklim değişikliği arıları tehdit eden başlıca faktörlerdir. Bilim insanları, arıların korunması için sürdürülebilir tarım yöntemlerinin benimsenmesi gerektiğini vurgulamaktadır. Her birimiz bahçemize arı dostu bitkiler dikerek bu küçük ama önemli canlılara yardımcı olabiliriz.""",
    "kelime_sayisi": 230,
}

# Anlama soruları
ANLAMA_SORULARI = [
    {
        "id": 1,
        "metin": "Kraliçe arı günde yaklaşık kaç yumurta bırakabilir?",
        "secenekler": ["Beş yüz", "Bin", "İki bin", "Beş bin"],
        "dogru": "İki bin"
    },
    {
        "id": 2,
        "metin": "Dünya besin maddelerinin yaklaşık ne kadarı arıların tozlaşmasına bağlıdır?",
        "secenekler": ["Dörtte biri", "Üçte biri", "Yarısı", "Beşte biri"],
        "dogru": "Üçte biri"
    },
    {
        "id": 3,
        "metin": "Bir kilogram bal için yaklaşık kaç çiçek ziyaret edilmelidir?",
        "secenekler": ["Bir milyon", "İki milyon", "Dört milyon", "On milyon"],
        "dogru": "Dört milyon"
    },
    {
        "id": 4,
        "metin": "Arılar birbirleriyle nasıl iletişim kurar?",
        "secenekler": ["Ses çıkararak", "Koku yayarak", "Dans ederek", "Renk değiştirerek"],
        "dogru": "Dans ederek"
    },
    {
        "id": 5,
        "metin": "Aşağıdakilerden hangisi arı popülasyonlarını tehdit eden faktörlerden biri DEĞİLDİR?",
        "secenekler": ["Tarım ilaçları", "Habitat kaybı", "Aşırı bal üretimi", "İklim değişikliği"],
        "dogru": "Aşırı bal üretimi"
    },
    {
        "id": 6,
        "metin": "Kuyruk sallama dansı ne anlama gelir?",
        "secenekler": ["Tehlike var", "Yakın mesafe", "Uzak mesafe", "Yiyecek bitti"],
        "dogru": "Uzak mesafe"
    },
    {
        "id": 7,
        "metin": "Nektar nasıl bala dönüşür?",
        "secenekler": [
            "Güneşte kurutularak",
            "Enzimlerle işlenip kanat çırparak suyu buharlaştırılarak",
            "Toprak altında bekletilerek",
            "Diğer böceklerle karıştırılarak"
        ],
        "dogru": "Enzimlerle işlenip kanat çırparak suyu buharlaştırılarak"
    },
    {
        "id": 8,
        "metin": "İşçi arıların görevlerinden hangisi metinde GEÇMEMİŞTİR?",
        "secenekler": ["Yiyecek toplamak", "Petek yapmak", "Kraliçe seçmek", "Kovana bekçilik etmek"],
        "dogru": "Kraliçe seçmek"
    },
]

# Okuma hızı seviyeleri (kelime/dakika)
HIZ_SEVIYELERI = {
    (0, 100): {"seviye": "Yavaş", "aciklama": "Okuma hızınız ortalamanın altında. Düzenli okuma pratiği ile geliştirebilirsiniz."},
    (100, 180): {"seviye": "Normal", "aciklama": "Okuma hızınız yaş grubunuz için normal seviyede."},
    (180, 300): {"seviye": "İyi", "aciklama": "Okuma hızınız ortalamanın üzerinde. İyi bir okuma becerisi gösteriyorsunuz."},
    (300, 10000): {"seviye": "Çok İyi", "aciklama": "Okuma hızınız oldukça yüksek. Hızlı okuma becerisi gelişmiş."}
}


def hesapla(okuma_suresi_saniye, anlama_cevaplari):
    """Hızlı okuma sonuçlarını hesapla"""
    # Okuma hızı (kelime/dakika)
    okuma_suresi_dakika = okuma_suresi_saniye / 60
    kelime_dakika = round(OKUMA_METNI["kelime_sayisi"] / max(okuma_suresi_dakika, 0.1), 1)

    # Anlama yüzdesi
    dogru_sayisi = 0
    for soru in ANLAMA_SORULARI:
        if soru["id"] in anlama_cevaplari:
            if anlama_cevaplari[soru["id"]] == soru["dogru"]:
                dogru_sayisi += 1

    anlama_yuzdesi = round((dogru_sayisi / len(ANLAMA_SORULARI)) * 100, 1)

    # Etkili okuma hızı (hız x anlama oranı)
    etkili_hiz = round(kelime_dakika * (anlama_yuzdesi / 100), 1)

    # Hız seviyesi
    hiz_seviyesi = "Normal"
    hiz_aciklama = ""
    for aralik, bilgi in HIZ_SEVIYELERI.items():
        if aralik[0] <= kelime_dakika < aralik[1]:
            hiz_seviyesi = bilgi["seviye"]
            hiz_aciklama = bilgi["aciklama"]
            break

    return {
        "okuma_suresi_saniye": round(okuma_suresi_saniye, 1),
        "kelime_dakika": kelime_dakika,
        "dogru_sayisi": dogru_sayisi,
        "toplam_soru": len(ANLAMA_SORULARI),
        "anlama_yuzdesi": anlama_yuzdesi,
        "etkili_hiz": etkili_hiz,
        "hiz_seviyesi": hiz_seviyesi,
        "hiz_aciklama": hiz_aciklama
    }


def sonuc_goster(sonuclar):
    """Hızlı okuma sonuçlarını göster"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Okuma Hızı", f"{sonuclar['kelime_dakika']} kelime/dk")
    with col2:
        st.metric("Anlama Oranı", f"%{sonuclar['anlama_yuzdesi']}")
    with col3:
        st.metric("Etkili Hız", f"{sonuclar['etkili_hiz']} kelime/dk")

    st.markdown(f"### Hız Seviyeniz: **{sonuclar['hiz_seviyesi']}**")
    st.info(sonuclar["hiz_aciklama"])

    st.markdown(f"**Doğru Cevap:** {sonuclar['dogru_sayisi']}/{sonuclar['toplam_soru']}")
    st.markdown(f"**Okuma Süresi:** {sonuclar['okuma_suresi_saniye']} saniye")
