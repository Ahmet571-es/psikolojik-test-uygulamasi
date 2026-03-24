# -*- coding: utf-8 -*-
"""Holland RIASEC Kariyer Envanteri Modülü"""

import streamlit as st

TEST_ADI = "Holland RIASEC Kariyer Envanteri"
TEST_ACIKLAMA = "6 kariyer tipine göre mesleki yöneliminizi keşfedin."

TIPLER = {
    "R": {"ad": "Gerçekçi (Realistic)", "aciklama": "Pratik, el becerisi gerektiren işleri sever. Somut ve fiziksel aktiviteleri tercih eder.", "meslekler": "Mühendis, Teknisyen, Pilot, Çiftçi, Sporcu"},
    "I": {"ad": "Araştırmacı (Investigative)", "aciklama": "Düşünmeyi, analiz etmeyi ve araştırmayı sever. Bilimsel konulara ilgilidir.", "meslekler": "Bilim İnsanı, Doktor, Araştırmacı, Programcı, Analist"},
    "A": {"ad": "Sanatçı (Artistic)", "aciklama": "Yaratıcı, özgün ve bağımsız çalışmayı sever. Sanatsal ifadeyi önemser.", "meslekler": "Sanatçı, Yazar, Müzisyen, Tasarımcı, Mimar"},
    "S": {"ad": "Sosyal (Social)", "aciklama": "İnsanlara yardım etmeyi, öğretmeyi ve danışmanlık yapmayı sever.", "meslekler": "Öğretmen, Psikolog, Sosyal Hizmet, Hemşire, Danışman"},
    "E": {"ad": "Girişimci (Enterprising)", "aciklama": "Liderlik etmeyi, ikna etmeyi ve yönetmeyi sever. Risk almayı göze alır.", "meslekler": "Yönetici, Avukat, Politikacı, Satıcı, Girişimci"},
    "C": {"ad": "Gelenekçi (Conventional)", "aciklama": "Düzenli, sistematik ve detay odaklı çalışmayı sever.", "meslekler": "Muhasebeci, Bankacı, Sekreter, Kütüphaneci, İstatistikçi"}
}

SORULAR = [
    {"id": 1, "metin": "Bir makineyi tamir etmek hoşuma gider.", "tip": "R"},
    {"id": 2, "metin": "Açık havada ve doğada çalışmayı severim.", "tip": "R"},
    {"id": 3, "metin": "Ellerimle bir şeyler yapmaktan keyif alırım.", "tip": "R"},
    {"id": 4, "metin": "Spor yapmak veya fiziksel aktiviteler beni mutlu eder.", "tip": "R"},
    {"id": 5, "metin": "Araç gereç kullanmayı ve tamir etmeyi severim.", "tip": "R"},
    {"id": 6, "metin": "Bilimsel deneylere ilgi duyarım.", "tip": "I"},
    {"id": 7, "metin": "Bir problemi analiz etmek beni heyecanlandırır.", "tip": "I"},
    {"id": 8, "metin": "Matematiksel problemleri çözmekten keyif alırım.", "tip": "I"},
    {"id": 9, "metin": "Bir konuyu derinlemesine araştırmak hoşuma gider.", "tip": "I"},
    {"id": 10, "metin": "Bilgisayar veya teknoloji ile uğraşmayı severim.", "tip": "I"},
    {"id": 11, "metin": "Resim yapmak veya müzik çalmak beni mutlu eder.", "tip": "A"},
    {"id": 12, "metin": "Yaratıcı projeler üzerinde çalışmaktan keyif alırım.", "tip": "A"},
    {"id": 13, "metin": "Hikâye, şiir veya günlük yazmayı severim.", "tip": "A"},
    {"id": 14, "metin": "Özgür ve bağımsız çalışmayı tercih ederim.", "tip": "A"},
    {"id": 15, "metin": "Hayal gücümü kullanmayı severim.", "tip": "A"},
    {"id": 16, "metin": "Arkadaşlarıma bir konuyu anlatmaktan keyif alırım.", "tip": "S"},
    {"id": 17, "metin": "İnsanlara yardım etmek beni tatmin eder.", "tip": "S"},
    {"id": 18, "metin": "Grup çalışması yapmayı severim.", "tip": "S"},
    {"id": 19, "metin": "İnsanların sorunlarını dinlemekten sıkılmam.", "tip": "S"},
    {"id": 20, "metin": "Gönüllü çalışmalara katılmak isterim.", "tip": "S"},
    {"id": 21, "metin": "Bir grubu yönetmek ve organize etmek hoşuma gider.", "tip": "E"},
    {"id": 22, "metin": "İnsanları ikna etmekte başarılıyımdır.", "tip": "E"},
    {"id": 23, "metin": "Rekabetçi ortamlarda daha iyi çalışırım.", "tip": "E"},
    {"id": 24, "metin": "Kendi işimi kurmak isterdim.", "tip": "E"},
    {"id": 25, "metin": "Liderlik yapmaktan keyif alırım.", "tip": "E"},
    {"id": 26, "metin": "Düzenli ve planlı çalışmayı severim.", "tip": "C"},
    {"id": 27, "metin": "Detaylara dikkat etmek benim güçlü yönümdür.", "tip": "C"},
    {"id": 28, "metin": "Verileri organize etmek ve sınıflandırmak hoşuma gider.", "tip": "C"},
    {"id": 29, "metin": "Kuralları takip etmek beni rahatlatır.", "tip": "C"},
    {"id": 30, "metin": "Sayılarla ve tablolarla çalışmayı severim.", "tip": "C"},
]

SECENEKLER = {
    1: "Hiç Katılmıyorum",
    2: "Katılmıyorum",
    3: "Kararsızım",
    4: "Katılıyorum",
    5: "Tamamen Katılıyorum"
}


def hesapla(cevaplar):
    """Holland RIASEC puanlarını hesapla"""
    tip_puanlari = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    tip_soru_sayisi = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    for soru in SORULAR:
        soru_id = soru["id"]
        tip = soru["tip"]
        if soru_id in cevaplar:
            tip_puanlari[tip] += cevaplar[soru_id]
            tip_soru_sayisi[tip] += 1

    tip_yuzdeleri = {}
    for tip in tip_puanlari:
        if tip_soru_sayisi[tip] > 0:
            max_puan = tip_soru_sayisi[tip] * 5
            tip_yuzdeleri[tip] = round((tip_puanlari[tip] / max_puan) * 100, 1)
        else:
            tip_yuzdeleri[tip] = 0

    sirali = sorted(tip_yuzdeleri.items(), key=lambda x: x[1], reverse=True)
    holland_kodu = "".join([t[0] for t in sirali[:3]])

    return {
        "tip_puanlari": tip_puanlari,
        "tip_yuzdeleri": tip_yuzdeleri,
        "holland_kodu": holland_kodu,
        "baskin_tip": sirali[0][0],
        "baskin_tip_ad": TIPLER[sirali[0][0]]["ad"],
        "baskin_tip_aciklama": TIPLER[sirali[0][0]]["aciklama"],
        "baskin_tip_meslekler": TIPLER[sirali[0][0]]["meslekler"],
        "sirali_tipler": sirali
    }


def sonuc_goster(sonuclar):
    """Holland sonuçlarını göster"""
    st.markdown(f"### Holland Kodunuz: **{sonuclar['holland_kodu']}**")
    st.markdown(f"### Baskın Tipiniz: {sonuclar['baskin_tip_ad']}")
    st.info(sonuclar["baskin_tip_aciklama"])
    st.markdown(f"**Uygun Meslekler:** {sonuclar['baskin_tip_meslekler']}")

    st.markdown("#### RIASEC Dağılımı")
    for tip, yuzde in sonuclar["sirali_tipler"]:
        st.progress(yuzde / 100, text=f"{TIPLER[tip]['ad']}: %{yuzde}")
