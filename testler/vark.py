# -*- coding: utf-8 -*-
"""VARK Öğrenme Stilleri Testi Modülü"""

import streamlit as st

TEST_ADI = "VARK Öğrenme Stilleri"
TEST_ACIKLAMA = "Görsel, İşitsel, Okuma/Yazma ve Kinestetik öğrenme tercihlerinizi belirleyin."

STILLER = {
    "V": {"ad": "Görsel (Visual)", "aciklama": "Şema, grafik, harita ve görsel materyallerle en iyi öğrenir."},
    "A": {"ad": "İşitsel (Aural)", "aciklama": "Dinleyerek, tartışarak ve sesli tekrar yaparak en iyi öğrenir."},
    "R": {"ad": "Okuma/Yazma (Read/Write)", "aciklama": "Okuyarak, not alarak ve yazarak en iyi öğrenir."},
    "K": {"ad": "Kinestetik (Kinesthetic)", "aciklama": "Yaparak, deneyerek ve hareket ederek en iyi öğrenir."}
}

SORULAR = [
    {
        "id": 1,
        "metin": "Yeni bir cihazı kullanmayı öğrenirken ne yaparsın?",
        "secenekler": [
            {"metin": "Kullanım kılavuzundaki resimlere ve şemalara bakarım.", "stil": "V"},
            {"metin": "Birinden bana anlatmasını isterim.", "stil": "A"},
            {"metin": "Kullanım kılavuzunu baştan sona okurum.", "stil": "R"},
            {"metin": "Hemen denemeye başlarım, kurcalayarak öğrenirim.", "stil": "K"}
        ]
    },
    {
        "id": 2,
        "metin": "Bir şehirde yol tarifi alırken hangisini tercih edersin?",
        "secenekler": [
            {"metin": "Harita veya navigasyon uygulaması kullanırım.", "stil": "V"},
            {"metin": "Birinin sözlü olarak tarif etmesini isterim.", "stil": "A"},
            {"metin": "Yol tarifini yazılı olarak almayı tercih ederim.", "stil": "R"},
            {"metin": "Bir kere gidersem yolu hatırlarım.", "stil": "K"}
        ]
    },
    {
        "id": 3,
        "metin": "Sınıfta en iyi nasıl öğrenirsin?",
        "secenekler": [
            {"metin": "Tahtadaki şekiller ve grafiklerden.", "stil": "V"},
            {"metin": "Öğretmeni dinleyerek.", "stil": "A"},
            {"metin": "Ders kitabını okuyarak ve not alarak.", "stil": "R"},
            {"metin": "Deney yaparak veya uygulama ile.", "stil": "K"}
        ]
    },
    {
        "id": 4,
        "metin": "Sınava nasıl çalışırsın?",
        "secenekler": [
            {"metin": "Renkli kalemlerle şema ve zihin haritası çizerim.", "stil": "V"},
            {"metin": "Konuları sesli olarak tekrar ederim veya birine anlatırım.", "stil": "A"},
            {"metin": "Notlarımı ve kitabı tekrar tekrar okurum.", "stil": "R"},
            {"metin": "Pratik sorular çözerim, örnekleri elle yazarım.", "stil": "K"}
        ]
    },
    {
        "id": 5,
        "metin": "Bir sunum hazırlarken ne yaparsın?",
        "secenekler": [
            {"metin": "Görseller, grafikler ve resimler eklerim.", "stil": "V"},
            {"metin": "İçeriği sesli prova ederim.", "stil": "A"},
            {"metin": "Metni detaylı yazarım ve düzenlerim.", "stil": "R"},
            {"metin": "Canlandırma veya gösterim yapmayı planlarsam.", "stil": "K"}
        ]
    },
    {
        "id": 6,
        "metin": "Yeni bir yemek tarifini öğrenirken ne yaparsın?",
        "secenekler": [
            {"metin": "Tarif videosunu izlerim.", "stil": "V"},
            {"metin": "Birinin tarifi anlatmasını dinlerim.", "stil": "A"},
            {"metin": "Tarifi okur ve adımları not alırım.", "stil": "R"},
            {"metin": "Hemen mutfağa girip deneyerek öğrenirim.", "stil": "K"}
        ]
    },
    {
        "id": 7,
        "metin": "Yeni bir oyun öğrenirken ne yaparsın?",
        "secenekler": [
            {"metin": "Kuralların görsel olarak gösterilmesini isterim.", "stil": "V"},
            {"metin": "Birinin bana kuralları anlatmasını isterim.", "stil": "A"},
            {"metin": "Kural kitapçığını okurum.", "stil": "R"},
            {"metin": "Oynayarak öğrenirim.", "stil": "K"}
        ]
    },
    {
        "id": 8,
        "metin": "Bir şeyi hatırlamak istediğinde ne yaparsın?",
        "secenekler": [
            {"metin": "Zihinde canlandırırım, resim gibi hatırlarım.", "stil": "V"},
            {"metin": "Kendi kendime söylerim veya bir melodiyle bağlarım.", "stil": "A"},
            {"metin": "Yazarak ve listeleyerek hatırlarım.", "stil": "R"},
            {"metin": "Yaparak veya hareket ederek hatırlarım.", "stil": "K"}
        ]
    },
    {
        "id": 9,
        "metin": "Bir müzede en çok ne ilgini çeker?",
        "secenekler": [
            {"metin": "Sergideki görseller ve tasarımlar.", "stil": "V"},
            {"metin": "Rehberin anlattıkları veya sesli rehber.", "stil": "A"},
            {"metin": "Bilgi panoları ve açıklama metinleri.", "stil": "R"},
            {"metin": "Dokunabileceğim veya deneyimleyebileceğim alanlar.", "stil": "K"}
        ]
    },
    {
        "id": 10,
        "metin": "Bir problemi çözerken genellikle ne yaparsın?",
        "secenekler": [
            {"metin": "Diyagram veya şekil çizerim.", "stil": "V"},
            {"metin": "Birine anlatarak düşünürüm.", "stil": "A"},
            {"metin": "Sorunu yazıya dökerim ve analiz ederim.", "stil": "R"},
            {"metin": "Farklı çözümleri deneyerek bulurum.", "stil": "K"}
        ]
    },
    {
        "id": 11,
        "metin": "Ders çalışırken hangi ortamı tercih edersin?",
        "secenekler": [
            {"metin": "Renkli ve düzenli notların olduğu masam.", "stil": "V"},
            {"metin": "Müzik çalabildiğim veya sesli çalışabildiğim yer.", "stil": "A"},
            {"metin": "Sessiz bir kütüphane veya okuma köşesi.", "stil": "R"},
            {"metin": "Hareket edebildiğim, rahat bir alan.", "stil": "K"}
        ]
    },
    {
        "id": 12,
        "metin": "Öğretmenin en çok hangi yöntemi kullandığında daha iyi anlarsın?",
        "secenekler": [
            {"metin": "Tahtada gösterdiğinde.", "stil": "V"},
            {"metin": "Sözlü olarak açıkladığında.", "stil": "A"},
            {"metin": "Kitaptan okuduğumuzda.", "stil": "R"},
            {"metin": "Bize uygulama yaptırdığında.", "stil": "K"}
        ]
    },
    {
        "id": 13,
        "metin": "Tatilde bir yer hakkında bilgi edinirken ne yaparsın?",
        "secenekler": [
            {"metin": "Fotoğraflarına ve videolarına bakarım.", "stil": "V"},
            {"metin": "Gidenlerden dinlerim.", "stil": "A"},
            {"metin": "Blog yazıları ve gezi rehberlerini okurum.", "stil": "R"},
            {"metin": "Oraya gitmeden bilemem, deneyimlemem lazım.", "stil": "K"}
        ]
    },
    {
        "id": 14,
        "metin": "Arkadaşlarına bir şeyi anlatırken genellikle ne yaparsın?",
        "secenekler": [
            {"metin": "Çizerek veya göstererek anlatırım.", "stil": "V"},
            {"metin": "Detaylı olarak sözel anlatırım.", "stil": "A"},
            {"metin": "Mesaj veya yazılı olarak anlatırım.", "stil": "R"},
            {"metin": "Canlandırarak veya taklit ederek gösteririm.", "stil": "K"}
        ]
    },
    {
        "id": 15,
        "metin": "Bir filmi veya diziyi değerlendirirken neye dikkat edersin?",
        "secenekler": [
            {"metin": "Görsel efektlere ve sinematografiye.", "stil": "V"},
            {"metin": "Diyaloglara ve müziğine.", "stil": "A"},
            {"metin": "Hikâyenin mantığına ve senaryoya.", "stil": "R"},
            {"metin": "Bende bıraktığı hisse ve etkiye.", "stil": "K"}
        ]
    },
    {
        "id": 16,
        "metin": "Bir proje hazırlarken ne yaparsın?",
        "secenekler": [
            {"metin": "Poster veya infografik hazırlarım.", "stil": "V"},
            {"metin": "Sözlü sunum hazırlarım.", "stil": "A"},
            {"metin": "Rapor veya makale yazarım.", "stil": "R"},
            {"metin": "Model veya maket yaparım.", "stil": "K"}
        ]
    },
]


def hesapla(cevaplar):
    """VARK puanlarını hesapla"""
    stil_puanlari = {"V": 0, "A": 0, "R": 0, "K": 0}

    for soru in SORULAR:
        soru_id = soru["id"]
        if soru_id in cevaplar:
            secilen_stil = cevaplar[soru_id]
            if secilen_stil in stil_puanlari:
                stil_puanlari[secilen_stil] += 1

    toplam = sum(stil_puanlari.values())
    stil_yuzdeleri = {}
    for stil, puan in stil_puanlari.items():
        stil_yuzdeleri[stil] = round((puan / max(toplam, 1)) * 100, 1)

    # Baskın stil belirleme
    sirali = sorted(stil_yuzdeleri.items(), key=lambda x: x[1], reverse=True)
    baskin_stil = sirali[0][0]

    # Multimodal kontrol
    multimodal = False
    if len(sirali) >= 2 and abs(sirali[0][1] - sirali[1][1]) <= 10:
        multimodal = True

    return {
        "stil_puanlari": stil_puanlari,
        "stil_yuzdeleri": stil_yuzdeleri,
        "baskin_stil": baskin_stil,
        "baskin_stil_ad": STILLER[baskin_stil]["ad"],
        "baskin_stil_aciklama": STILLER[baskin_stil]["aciklama"],
        "multimodal": multimodal,
        "sirali_stiller": sirali
    }


def sonuc_goster(sonuclar):
    """VARK sonuçlarını göster"""
    if sonuclar["multimodal"]:
        st.success("Çoklu Öğrenme Stili (Multimodal) tespit edildi!")

    st.markdown(f"### Baskın Öğrenme Stiliniz: {sonuclar['baskin_stil_ad']}")
    st.info(sonuclar["baskin_stil_aciklama"])

    st.markdown("#### Öğrenme Stili Dağılımı")
    for stil, yuzde in sonuclar["sirali_stiller"]:
        st.progress(yuzde / 100, text=f"{STILLER[stil]['ad']}: %{yuzde}")
