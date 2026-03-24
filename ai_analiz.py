# -*- coding: utf-8 -*-
"""Eğitim Check-Up - Claude API ile AI Analiz Modülü"""

import streamlit as st
import json
import os

# Maksimum token limiti
MAX_TOKEN = 4096
API_TIMEOUT = 60


def _get_api_key():
    """Anthropic API anahtarını al"""
    if "ANTHROPIC_API_KEY" in st.secrets:
        return st.secrets["ANTHROPIC_API_KEY"]
    from config import ANTHROPIC_API_KEY
    return ANTHROPIC_API_KEY


def _get_client():
    """Anthropic istemcisini oluştur"""
    api_key = _get_api_key()
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key, timeout=API_TIMEOUT)
    except Exception as e:
        st.error(f"API bağlantı hatası: {e}")
        return None


def tekli_analiz(ogrenci_adi, test_adi, sonuclar):
    """Tek bir test için AI analizi yap"""
    client = _get_client()
    if not client:
        st.error("Claude API bağlantısı kurulamadı. API anahtarını kontrol edin.")
        return None

    sonuc_metin = json.dumps(sonuclar, ensure_ascii=False, indent=2)

    sistem_prompt = """Sen deneyimli bir eğitim psikoloğusun. Görevin, öğrencinin test sonuçlarını
analiz ederek kapsamlı ve anlaşılır bir değerlendirme raporu hazırlamak.

YAZIM KURALLARI:
- Yalın, sade ve akıcı Türkçe kullan
- Teknik terimleri parantez içinde açıkla
- Destekleyici ve umut verici bir ton kullan
- Somut, uygulanabilir öneriler ver
- Öğrencinin adını kullan
- Olumsuzlukları "gelişim alanı" olarak çerçevele

RAPOR YAPISI:
1. Genel Değerlendirme (2-3 cümle özet)
2. Güçlü Yönler (en az 3 madde)
3. Gelişim Alanları (en az 2 madde, yapıcı dille)
4. Öğrenme Önerileri (somut, uygulanabilir 3-5 öneri)
5. Aile ve Öğretmen İçin Notlar (2-3 öneri)"""

    kullanici_prompt = f"""Öğrenci: {ogrenci_adi}
Test: {test_adi}
Sonuçlar:
{sonuc_metin}

Lütfen bu sonuçlara dayanarak kapsamlı bir değerlendirme raporu hazırla."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=MAX_TOKEN,
            messages=[
                {"role": "user", "content": kullanici_prompt}
            ],
            system=sistem_prompt
        )
        return response.content[0].text
    except Exception as e:
        hata_mesaji = str(e)
        if "rate_limit" in hata_mesaji.lower():
            st.error("API istek limiti aşıldı. Lütfen birkaç dakika bekleyip tekrar deneyin.")
        elif "authentication" in hata_mesaji.lower() or "api_key" in hata_mesaji.lower():
            st.error("API anahtarı geçersiz. Lütfen ayarları kontrol edin.")
        elif "timeout" in hata_mesaji.lower():
            st.error("API yanıt süresi aşıldı. Lütfen tekrar deneyin.")
        else:
            st.error(f"AI analiz hatası: {hata_mesaji}")
        return None


def coklu_analiz(ogrenci_adi, test_sonuclari):
    """Birden fazla test için birleşik AI analizi yap"""
    client = _get_client()
    if not client:
        st.error("Claude API bağlantısı kurulamadı. API anahtarını kontrol edin.")
        return None

    testler_metin = ""
    for test_adi, sonuclar in test_sonuclari.items():
        testler_metin += f"\n--- {test_adi} ---\n"
        testler_metin += json.dumps(sonuclar, ensure_ascii=False, indent=2)
        testler_metin += "\n"

    sistem_prompt = """Sen deneyimli bir eğitim psikoloğusun. Görevin, öğrencinin birden fazla
test sonucunu birlikte değerlendirerek bütüncül bir analiz raporu hazırlamak.

YAZIM KURALLARI:
- Yalın, sade ve akıcı Türkçe kullan
- Testler arası bağlantıları kur
- Destekleyici ve umut verici bir ton kullan
- Somut, uygulanabilir öneriler ver
- Öğrencinin adını kullan
- Olumsuzlukları "gelişim alanı" olarak çerçevele
- Çelişkili sonuçları açıkla

RAPOR YAPISI:
1. Bütüncül Değerlendirme (3-4 cümle genel profil)
2. Testler Arası İlişkiler (hangi sonuçlar birbirini destekliyor/çelişiyor)
3. Güçlü Yönler Profili (testlerden derlenen güçlü yönler)
4. Gelişim Haritası (öncelikli gelişim alanları)
5. Kişiselleştirilmiş Öğrenme Stratejileri (5-7 somut öneri)
6. Kariyer ve Yönelim Önerileri (testler ışığında)
7. Aile ve Öğretmen İçin Öneriler (3-5 madde)"""

    kullanici_prompt = f"""Öğrenci: {ogrenci_adi}

Yapılan Testler ve Sonuçları:
{testler_metin}

Lütfen tüm test sonuçlarını birlikte değerlendirerek bütüncül bir analiz raporu hazırla."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=MAX_TOKEN,
            messages=[
                {"role": "user", "content": kullanici_prompt}
            ],
            system=sistem_prompt
        )
        return response.content[0].text
    except Exception as e:
        hata_mesaji = str(e)
        if "rate_limit" in hata_mesaji.lower():
            st.error("API istek limiti aşıldı. Lütfen birkaç dakika bekleyip tekrar deneyin.")
        elif "timeout" in hata_mesaji.lower():
            st.error("API yanıt süresi aşıldı. Lütfen tekrar deneyin.")
        else:
            st.error(f"AI analiz hatası: {hata_mesaji}")
        return None


def aile_ozeti_olustur(ogrenci_adi, analiz_sonuclari, secilen_basliklar, ogretmen_notu=""):
    """Aile bilgilendirme özeti oluştur"""
    client = _get_client()
    if not client:
        st.error("Claude API bağlantısı kurulamadı. API anahtarını kontrol edin.")
        return None

    sistem_prompt = """Sen deneyimli bir eğitim psikoloğusun. Aşağıdaki test sonuçlarına
dayanarak, öğretmenin seçtiği konu başlıkları için AİLEYE YÖNELİK bir bilgilendirme özeti hazırla.

YAZIM KURALLARI:
- Yalın, sade ve akıcı Türkçe kullan
- Teknik terim kullanma, kullanırsan parantez içinde açıkla
- Aileyi yargılamayan, destekleyici ve umut verici bir ton kullan
- Her başlık 3-5 cümle olsun — kısa ve öz
- Somut, uygulanabilir tavsiyeler ver
- "Çocuğunuz" yerine öğrencinin adını kullan
- Olumsuzlukları "gelişim alanı" olarak çerçevele
- Her başlığın sonunda 1-2 pratik öneri ekle"""

    basliklar_metin = "\n".join(f"- {b}" for b in secilen_basliklar)

    kullanici_prompt = f"""ÖĞRENCİ: {ogrenci_adi}

TEST SONUÇLARI VE ANALİZ:
{analiz_sonuclari}

SEÇİLEN KONU BAŞLIKLARI:
{basliklar_metin}

ÖĞRETMEN NOTU:
{ogretmen_notu if ogretmen_notu else 'Yok'}

Lütfen yukarıdaki bilgilere dayanarak, seçilen her konu başlığı için aileye yönelik bilgilendirme özeti hazırla."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=MAX_TOKEN,
            messages=[
                {"role": "user", "content": kullanici_prompt}
            ],
            system=sistem_prompt
        )
        return response.content[0].text
    except Exception as e:
        hata_mesaji = str(e)
        if "rate_limit" in hata_mesaji.lower():
            st.error("API istek limiti aşıldı. Lütfen birkaç dakika bekleyip tekrar deneyin.")
        elif "timeout" in hata_mesaji.lower():
            st.error("API yanıt süresi aşıldı. Lütfen tekrar deneyin.")
        else:
            st.error(f"AI analiz hatası: {hata_mesaji}")
        return None
