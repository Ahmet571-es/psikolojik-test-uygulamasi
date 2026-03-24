# -*- coding: utf-8 -*-
"""Eğitim Check-Up - Uygulama Yapılandırması"""

import os
from dotenv import load_dotenv

load_dotenv()

# Uygulama bilgileri
APP_NAME = "Eğitim Check-Up"
APP_VERSION = "1.0.0"
APP_ICON = "🎓"
APP_DESCRIPTION = "Eğitim Psikolojisi Değerlendirme Platformu"

# API Yapılandırması
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Supabase Yapılandırması
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Test Modülleri
TEST_MODULLERI = {
    "enneagram": {
        "ad": "Enneagram Kişilik Testi",
        "aciklama": "9 temel kişilik tipinden hangisine yakın olduğunuzu keşfedin.",
        "ikon": "🔷",
        "sure": "15 dk",
        "kategori": "Kişilik"
    },
    "vark": {
        "ad": "VARK Öğrenme Stilleri",
        "aciklama": "Görsel, İşitsel, Okuma/Yazma ve Kinestetik öğrenme tercihlerinizi belirleyin.",
        "ikon": "📚",
        "sure": "10 dk",
        "kategori": "Öğrenme"
    },
    "holland": {
        "ad": "Holland RIASEC Kariyer Envanteri",
        "aciklama": "6 kariyer tipine göre mesleki yöneliminizi keşfedin.",
        "ikon": "🧭",
        "sure": "12 dk",
        "kategori": "Kariyer"
    },
    "coklu_zeka": {
        "ad": "Çoklu Zekâ Testi (Gardner)",
        "aciklama": "8 farklı zekâ alanındaki güçlü ve gelişime açık yönlerinizi belirleyin.",
        "ikon": "🧠",
        "sure": "15 dk",
        "kategori": "Zekâ"
    },
    "beyin": {
        "ad": "Sağ-Sol Beyin Dominansı",
        "aciklama": "Beyin yarıküre baskınlığınızı ve düşünme stilinizi keşfedin.",
        "ikon": "🧩",
        "sure": "8 dk",
        "kategori": "Bilişsel"
    },
    "sinav_kaygisi": {
        "ad": "Sınav Kaygısı Ölçeği",
        "aciklama": "Sınav öncesi, sırası ve sonrasındaki kaygı düzeyinizi değerlendirin.",
        "ikon": "😰",
        "sure": "10 dk",
        "kategori": "Duygusal"
    },
    "calisma_davranisi": {
        "ad": "Çalışma Davranışı Değerlendirmesi",
        "aciklama": "Çalışma alışkanlıklarınızı ve verimlilik düzeyinizi analiz edin.",
        "ikon": "📋",
        "sure": "10 dk",
        "kategori": "Davranış"
    },
    "akademik_analiz": {
        "ad": "Akademik Başarı Analizi",
        "aciklama": "Ders bazında güçlü ve zayıf yönlerinizi, çalışma stratejilerinizi değerlendirin.",
        "ikon": "📊",
        "sure": "12 dk",
        "kategori": "Akademik"
    },
    "hizli_okuma": {
        "ad": "Hızlı Okuma Değerlendirmesi",
        "aciklama": "Okuma hızınızı ve okuduğunu anlama düzeyinizi ölçün.",
        "ikon": "📖",
        "sure": "15 dk",
        "kategori": "Beceri"
    },
    "dikkat": {
        "ad": "P2 Dikkat Testi",
        "aciklama": "Seçici dikkat, sürdürülebilir dikkat ve dikkat dağılma eğiliminizi ölçün.",
        "ikon": "🎯",
        "sure": "10 dk",
        "kategori": "Bilişsel"
    }
}

# Aile bilgilendirme konu başlıkları
AILE_KONU_BASLIKLARI = [
    "Genel Değerlendirme",
    "Öğrenme Stili ve Tercihleri",
    "Güçlü Yönler",
    "Gelişim Alanları",
    "Motivasyon ve İlgi Alanları",
    "Çalışma Alışkanlıkları",
    "Sınav Kaygısı Durumu",
    "Dikkat ve Odaklanma",
    "Sosyal-Duygusal Gelişim",
    "Kariyer Yönelimleri",
    "Evde Yapılabilecek Destekler",
    "Profesyonel Destek Önerileri"
]

# Test-Konu ilişkisi (hangi test hangi başlıkları destekler)
TEST_KONU_ILISKISI = {
    "enneagram": ["Genel Değerlendirme", "Güçlü Yönler", "Gelişim Alanları", "Sosyal-Duygusal Gelişim", "Profesyonel Destek Önerileri"],
    "vark": ["Genel Değerlendirme", "Öğrenme Stili ve Tercihleri", "Güçlü Yönler", "Çalışma Alışkanlıkları", "Evde Yapılabilecek Destekler"],
    "holland": ["Genel Değerlendirme", "Güçlü Yönler", "Motivasyon ve İlgi Alanları", "Kariyer Yönelimleri", "Evde Yapılabilecek Destekler"],
    "coklu_zeka": ["Genel Değerlendirme", "Güçlü Yönler", "Gelişim Alanları", "Öğrenme Stili ve Tercihleri", "Evde Yapılabilecek Destekler"],
    "beyin": ["Genel Değerlendirme", "Öğrenme Stili ve Tercihleri", "Güçlü Yönler", "Çalışma Alışkanlıkları"],
    "sinav_kaygisi": ["Genel Değerlendirme", "Sınav Kaygısı Durumu", "Gelişim Alanları", "Evde Yapılabilecek Destekler", "Profesyonel Destek Önerileri"],
    "calisma_davranisi": ["Genel Değerlendirme", "Çalışma Alışkanlıkları", "Gelişim Alanları", "Evde Yapılabilecek Destekler"],
    "akademik_analiz": ["Genel Değerlendirme", "Güçlü Yönler", "Gelişim Alanları", "Çalışma Alışkanlıkları", "Motivasyon ve İlgi Alanları"],
    "hizli_okuma": ["Genel Değerlendirme", "Güçlü Yönler", "Gelişim Alanları", "Dikkat ve Odaklanma", "Evde Yapılabilecek Destekler"],
    "dikkat": ["Genel Değerlendirme", "Dikkat ve Odaklanma", "Gelişim Alanları", "Evde Yapılabilecek Destekler", "Profesyonel Destek Önerileri"]
}

# PDF/DOCX Rapor ayarları
RAPOR_AYARLARI = {
    "font": "DejaVu Sans",
    "font_boyutu": 11,
    "baslik_boyutu": 16,
    "sayfa_kenar_boslugu": 20,
    "logo_yol": "",
}
