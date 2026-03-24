# -*- coding: utf-8 -*-
"""Enneagram Kişilik Testi Modülü"""

import streamlit as st

TEST_ADI = "Enneagram Kişilik Testi"
TEST_ACIKLAMA = "9 temel kişilik tipinden hangisine yakın olduğunuzu keşfedin."

# Enneagram tipleri
TIPLER = {
    1: {"ad": "Reformcu (Tip 1)", "aciklama": "Mükemmeliyetçi, ilkeli, düzenli ve sorumluluk sahibi."},
    2: {"ad": "Yardımsever (Tip 2)", "aciklama": "Şefkatli, cömert, sahiplenici ve insanları memnun etmeye yönelik."},
    3: {"ad": "Başarıcı (Tip 3)", "aciklama": "Uyumlu, hırslı, imaj odaklı ve başarıya yönelik."},
    4: {"ad": "Bireyci (Tip 4)", "aciklama": "Duygusal, yaratıcı, içe dönük ve özgünlük arayan."},
    5: {"ad": "Araştırmacı (Tip 5)", "aciklama": "Analitik, yenilikçi, ketum ve bilgi odaklı."},
    6: {"ad": "Sadık (Tip 6)", "aciklama": "Güvenilir, tedbirli, şüpheci ve güvenlik arayan."},
    7: {"ad": "Maceracı (Tip 7)", "aciklama": "Meşgul, iyimser, dağınık ve deneyim arayan."},
    8: {"ad": "Meydan Okuyan (Tip 8)", "aciklama": "Güçlü, dominant, kararlı ve koruyucu."},
    9: {"ad": "Barışçıl (Tip 9)", "aciklama": "Uyumlu, güven veren, sakin ve çatışmadan kaçınan."}
}

# Her soru bir tip ile ilişkili (tip numarası)
SORULAR = [
    {"id": 1, "metin": "Her şeyin doğru ve düzgün yapılması gerektiğini düşünürüm.", "tip": 1},
    {"id": 2, "metin": "Hata yaptığımda kendimi çok kötü hissederim.", "tip": 1},
    {"id": 3, "metin": "Kurallar ve düzen benim için çok önemlidir.", "tip": 1},
    {"id": 4, "metin": "Başkalarına yardım etmek beni mutlu eder.", "tip": 2},
    {"id": 5, "metin": "İnsanların ihtiyaçlarını hemen fark ederim.", "tip": 2},
    {"id": 6, "metin": "Sevdiklerim için her şeyi yaparım.", "tip": 2},
    {"id": 7, "metin": "Başarılı olmak benim için çok önemlidir.", "tip": 3},
    {"id": 8, "metin": "İnsanların beni beğenmesini isterim.", "tip": 3},
    {"id": 9, "metin": "Hedeflerime ulaşmak için çok çalışırım.", "tip": 3},
    {"id": 10, "metin": "Kendimi diğer insanlardan farklı hissederim.", "tip": 4},
    {"id": 11, "metin": "Duygularım çok yoğun olabilir.", "tip": 4},
    {"id": 12, "metin": "Sanat ve yaratıcılık benim için önemlidir.", "tip": 4},
    {"id": 13, "metin": "Yalnız kalmayı ve düşünmeyi severim.", "tip": 5},
    {"id": 14, "metin": "Bir konuyu araştırırken saatlerimi harcayabilirim.", "tip": 5},
    {"id": 15, "metin": "Duygularımı göstermek bana zor gelir.", "tip": 5},
    {"id": 16, "metin": "Güvenilir insanları bulmak zordur.", "tip": 6},
    {"id": 17, "metin": "Olası tehlikelere karşı hep hazırlıklı olmaya çalışırım.", "tip": 6},
    {"id": 18, "metin": "Bir karar vermeden önce çok düşünürüm.", "tip": 6},
    {"id": 19, "metin": "Yeni deneyimler yaşamayı çok severim.", "tip": 7},
    {"id": 20, "metin": "Sıkılmaktan nefret ederim, hep bir şeyler yapmak isterim.", "tip": 7},
    {"id": 21, "metin": "Hayata iyimser bakarım, her şeyin bir çözümü vardır.", "tip": 7},
    {"id": 22, "metin": "Güçlü olmak ve kontrolü elde tutmak benim için önemlidir.", "tip": 8},
    {"id": 23, "metin": "Haksızlığa uğradığımda çok sinirlenirim.", "tip": 8},
    {"id": 24, "metin": "Kararlarımı hızlı veririm ve arkasında dururum.", "tip": 8},
    {"id": 25, "metin": "Huzurlu bir ortam benim için çok önemlidir.", "tip": 9},
    {"id": 26, "metin": "Tartışmalardan kaçınmayı tercih ederim.", "tip": 9},
    {"id": 27, "metin": "Başkalarının isteklerine kolayca uyum sağlarım.", "tip": 9},
    # Ek sorular - daha derin ölçüm
    {"id": 28, "metin": "İşlerimi zamanında ve eksiksiz bitirmem gerektiğini düşünürüm.", "tip": 1},
    {"id": 29, "metin": "Birisi üzgün olduğunda hemen yanına gitmek isterim.", "tip": 2},
    {"id": 30, "metin": "Bir yarışmada veya sınavda birinci olmak çok hoşuma gider.", "tip": 3},
    {"id": 31, "metin": "Kimsenin anlamadığı derin duygular yaşarım.", "tip": 4},
    {"id": 32, "metin": "Kitap okumak veya belgesel izlemek en sevdiğim aktivitedir.", "tip": 5},
    {"id": 33, "metin": "Arkadaşlarıma çok sadığımdır, onlara ihanet etmem.", "tip": 6},
    {"id": 34, "metin": "Plan yapmak yerine anı yaşamayı tercih ederim.", "tip": 7},
    {"id": 35, "metin": "Zayıf insanları korumak gerektiğini düşünürüm.", "tip": 8},
    {"id": 36, "metin": "Rahatlamak ve sakin bir hayat sürmek benim için ideal.", "tip": 9},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Enneagram puanlarını hesapla"""
    tip_puanlari = {i: 0 for i in range(1, 10)}
    tip_soru_sayisi = {i: 0 for i in range(1, 10)}

    for soru in SORULAR:
        soru_id = soru["id"]
        tip = soru["tip"]
        if soru_id in cevaplar:
            tip_puanlari[tip] += cevaplar[soru_id]
            tip_soru_sayisi[tip] += 1

    # Yüzdelik hesapla
    tip_yuzdeleri = {}
    for tip in range(1, 10):
        if tip_soru_sayisi[tip] > 0:
            max_puan = tip_soru_sayisi[tip] * 5
            tip_yuzdeleri[tip] = round((tip_puanlari[tip] / max_puan) * 100, 1)
        else:
            tip_yuzdeleri[tip] = 0

    # En yüksek 3 tip
    sirali = sorted(tip_yuzdeleri.items(), key=lambda x: x[1], reverse=True)
    ana_tip = sirali[0][0]
    kanat1 = sirali[1][0]
    kanat2 = sirali[2][0]

    return {
        "tip_puanlari": tip_puanlari,
        "tip_yuzdeleri": tip_yuzdeleri,
        "ana_tip": ana_tip,
        "ana_tip_ad": TIPLER[ana_tip]["ad"],
        "ana_tip_aciklama": TIPLER[ana_tip]["aciklama"],
        "kanat1": kanat1,
        "kanat2": kanat2,
        "sirali_tipler": sirali
    }


def sonuc_goster(sonuclar):
    """Enneagram sonuçlarını göster"""
    st.markdown(f"### Ana Tipiniz: {sonuclar['ana_tip_ad']}")
    st.info(sonuclar["ana_tip_aciklama"])

    st.markdown("#### Tip Dağılımı")
    for tip_no, yuzde in sonuclar["sirali_tipler"]:
        tip_bilgi = TIPLER[tip_no]
        st.progress(yuzde / 100, text=f"{tip_bilgi['ad']}: %{yuzde}")

    st.markdown("#### Kanat Tipleri")
    st.write(f"- Birincil kanat: **{TIPLER[sonuclar['kanat1']]['ad']}**")
    st.write(f"- İkincil kanat: **{TIPLER[sonuclar['kanat2']]['ad']}**")
