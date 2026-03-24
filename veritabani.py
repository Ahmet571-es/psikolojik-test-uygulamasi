# -*- coding: utf-8 -*-
"""Eğitim Check-Up - Supabase Veritabanı İşlemleri"""

import streamlit as st
from datetime import datetime
import json
import time

# Supabase bağlantı yönetimi
_supabase_client = None
MAX_RETRY = 3
RETRY_DELAY = 2


def _get_supabase_config():
    """Supabase yapılandırmasını al"""
    url = ""
    key = ""
    if "SUPABASE_URL" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    else:
        from config import SUPABASE_URL, SUPABASE_KEY
        url = SUPABASE_URL
        key = SUPABASE_KEY
    return url, key


def get_supabase():
    """Supabase istemcisini al (bağlantı havuzu ile)"""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url, key = _get_supabase_config()
    if not url or not key:
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")
        return None


def _execute_with_retry(operation, max_retries=MAX_RETRY):
    """Veritabanı işlemini yeniden deneme mekanizmasıyla çalıştır"""
    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            raise e
    return None


# --- Öğrenci İşlemleri ---

def ogrenci_kaydet(ad, soyad, sinif, okul, ogretmen_id=None):
    """Yeni öğrenci kaydı oluştur"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        veri = {
            "ad": ad,
            "soyad": soyad,
            "sinif": sinif,
            "okul": okul,
            "ogretmen_id": ogretmen_id,
            "kayit_tarihi": datetime.now().isoformat()
        }
        result = sb.table("ogrenciler").insert(veri).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


def ogrenci_getir(ogrenci_id):
    """Öğrenci bilgilerini getir"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        result = sb.table("ogrenciler").select("*").eq("id", ogrenci_id).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


def ogretmenin_ogrencileri(ogretmen_id):
    """Öğretmene ait öğrencileri listele"""
    sb = get_supabase()
    if not sb:
        return []

    def _op():
        result = sb.table("ogrenciler").select("*").eq("ogretmen_id", ogretmen_id).order("ad").execute()
        return result.data if result.data else []

    return _execute_with_retry(_op)


# --- Test Sonuçları İşlemleri ---

def test_sonucu_kaydet(ogrenci_id, test_tipi, cevaplar, puanlar, sonuc_ozeti):
    """Test sonucunu kaydet"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        veri = {
            "ogrenci_id": ogrenci_id,
            "test_tipi": test_tipi,
            "cevaplar": json.dumps(cevaplar, ensure_ascii=False),
            "puanlar": json.dumps(puanlar, ensure_ascii=False),
            "sonuc_ozeti": json.dumps(sonuc_ozeti, ensure_ascii=False),
            "tarih": datetime.now().isoformat()
        }
        result = sb.table("test_sonuclari").insert(veri).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


def ogrenci_test_sonuclari(ogrenci_id, test_tipi=None):
    """Öğrencinin test sonuçlarını getir"""
    sb = get_supabase()
    if not sb:
        return []

    def _op():
        query = sb.table("test_sonuclari").select("*").eq("ogrenci_id", ogrenci_id)
        if test_tipi:
            query = query.eq("test_tipi", test_tipi)
        result = query.order("tarih", desc=True).execute()
        return result.data if result.data else []

    return _execute_with_retry(_op)


def tum_test_sonuclari(ogretmen_id):
    """Öğretmenin tüm öğrencilerinin test sonuçlarını getir"""
    sb = get_supabase()
    if not sb:
        return []

    def _op():
        result = sb.table("test_sonuclari").select(
            "*, ogrenciler!inner(ad, soyad, sinif, okul, ogretmen_id)"
        ).eq("ogrenciler.ogretmen_id", ogretmen_id).order("tarih", desc=True).execute()
        return result.data if result.data else []

    return _execute_with_retry(_op)


# --- Öğretmen İşlemleri ---

def ogretmen_giris(kullanici_adi, sifre):
    """Öğretmen girişi doğrula"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        result = sb.table("ogretmenler").select("*").eq(
            "kullanici_adi", kullanici_adi
        ).eq("sifre_hash", _hash_sifre(sifre)).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


def _hash_sifre(sifre):
    """Şifre hash'leme"""
    import hashlib
    return hashlib.sha256(sifre.encode("utf-8")).hexdigest()


# --- AI Analiz İşlemleri ---

def ai_analiz_kaydet(ogrenci_id, ogretmen_id, test_tipleri, analiz_metni, analiz_tipi="tekli"):
    """AI analiz sonucunu kaydet"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        veri = {
            "ogrenci_id": ogrenci_id,
            "ogretmen_id": ogretmen_id,
            "test_tipleri": json.dumps(test_tipleri, ensure_ascii=False),
            "analiz_metni": analiz_metni,
            "analiz_tipi": analiz_tipi,
            "tarih": datetime.now().isoformat()
        }
        result = sb.table("ai_analizler").insert(veri).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


# --- Aile Bilgilendirme İşlemleri ---

def aile_ozeti_kaydet(ogrenci_id, ogretmen_id, secilen_basliklar, ozet_metni, test_tipleri):
    """Aile bilgilendirme özetini kaydet"""
    sb = get_supabase()
    if not sb:
        return None

    def _op():
        veri = {
            "ogrenci_id": ogrenci_id,
            "ogretmen_id": ogretmen_id,
            "secilen_basliklar": json.dumps(secilen_basliklar, ensure_ascii=False),
            "ozet_metni": ozet_metni,
            "test_tipleri": json.dumps(test_tipleri, ensure_ascii=False),
            "olusturma_tarihi": datetime.now().isoformat()
        }
        result = sb.table("aile_ozetleri").insert(veri).execute()
        return result.data[0] if result.data else None

    return _execute_with_retry(_op)


def aile_ozetleri_getir(ogrenci_id=None, ogretmen_id=None):
    """Aile bilgilendirme özetlerini getir"""
    sb = get_supabase()
    if not sb:
        return []

    def _op():
        query = sb.table("aile_ozetleri").select("*")
        if ogrenci_id:
            query = query.eq("ogrenci_id", ogrenci_id)
        if ogretmen_id:
            query = query.eq("ogretmen_id", ogretmen_id)
        result = query.order("olusturma_tarihi", desc=True).execute()
        return result.data if result.data else []

    return _execute_with_retry(_op)


# --- Otomatik Tablo Oluşturma ---

_TABLO_SQLLERI = [
    # 1. ogretmenler
    """
    CREATE TABLE IF NOT EXISTS ogretmenler (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        ad TEXT NOT NULL,
        soyad TEXT NOT NULL,
        kullanici_adi TEXT UNIQUE NOT NULL,
        sifre_hash TEXT NOT NULL,
        okul TEXT,
        kayit_tarihi TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    # 2. ogrenciler
    """
    CREATE TABLE IF NOT EXISTS ogrenciler (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        ad TEXT NOT NULL,
        soyad TEXT NOT NULL,
        sinif TEXT,
        okul TEXT,
        ogretmen_id UUID REFERENCES ogretmenler(id),
        kayit_tarihi TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    # 3. test_sonuclari
    """
    CREATE TABLE IF NOT EXISTS test_sonuclari (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
        test_tipi TEXT NOT NULL,
        cevaplar JSONB,
        puanlar JSONB,
        sonuc_ozeti JSONB,
        tarih TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    # 4. ai_analizler
    """
    CREATE TABLE IF NOT EXISTS ai_analizler (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
        ogretmen_id UUID REFERENCES ogretmenler(id),
        test_tipleri JSONB,
        analiz_metni TEXT,
        analiz_tipi TEXT DEFAULT 'tekli',
        tarih TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    # 5. aile_ozetleri
    """
    CREATE TABLE IF NOT EXISTS aile_ozetleri (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
        ogretmen_id UUID REFERENCES ogretmenler(id),
        secilen_basliklar JSONB,
        ozet_metni TEXT,
        test_tipleri JSONB,
        olusturma_tarihi TIMESTAMPTZ DEFAULT NOW()
    );
    """,
]

_INDEKS_SQLLERI = [
    "CREATE INDEX IF NOT EXISTS idx_ogrenciler_ogretmen ON ogrenciler(ogretmen_id);",
    "CREATE INDEX IF NOT EXISTS idx_test_sonuclari_ogrenci ON test_sonuclari(ogrenci_id);",
    "CREATE INDEX IF NOT EXISTS idx_test_sonuclari_tip ON test_sonuclari(test_tipi);",
    "CREATE INDEX IF NOT EXISTS idx_ai_analizler_ogrenci ON ai_analizler(ogrenci_id);",
    "CREATE INDEX IF NOT EXISTS idx_aile_ozetleri_ogrenci ON aile_ozetleri(ogrenci_id);",
    "CREATE INDEX IF NOT EXISTS idx_aile_ozetleri_ogretmen ON aile_ozetleri(ogretmen_id);",
]

_DEMO_OGRETMEN_SQL = """
    INSERT INTO ogretmenler (ad, soyad, kullanici_adi, sifre_hash, okul)
    VALUES ('Demo', 'Öğretmen', 'demo', '{hash}', 'Demo Okul')
    ON CONFLICT (kullanici_adi) DO NOTHING;
"""


def _get_database_url():
    """PostgreSQL bağlantı string'ini al"""
    if "DATABASE_URL" in st.secrets:
        return st.secrets["DATABASE_URL"]
    from config import DATABASE_URL
    return DATABASE_URL


def tablolari_olustur():
    """Veritabanı tablolarını otomatik oluştur. İlk çalıştırmada çağrılır."""
    db_url = _get_database_url()
    if not db_url:
        return False, "DATABASE_URL tanımlı değil. .env veya Streamlit secrets'a ekleyin."

    try:
        import psycopg2
    except ImportError:
        return False, "psycopg2 paketi yüklü değil. requirements.txt'e 'psycopg2-binary' ekleyin."

    conn = None
    try:
        conn = psycopg2.connect(db_url, connect_timeout=10)
        conn.autocommit = True
        cur = conn.cursor()

        olusturulan = []
        for sql in _TABLO_SQLLERI:
            cur.execute(sql)
            # Tablo adını SQL'den çıkar
            tablo_adi = sql.split("EXISTS")[1].split("(")[0].strip()
            olusturulan.append(tablo_adi)

        # İndeksler
        for sql in _INDEKS_SQLLERI:
            cur.execute(sql)

        # Demo öğretmen
        demo_hash = _hash_sifre("demo123")
        cur.execute(_DEMO_OGRETMEN_SQL.format(hash=demo_hash))

        cur.close()
        conn.close()
        return True, f"Tablolar oluşturuldu: {', '.join(olusturulan)}"

    except Exception as e:
        if conn:
            conn.close()
        return False, f"Veritabanı hatası: {e}"


def tablolar_mevcut_mu():
    """Tabloların zaten var olup olmadığını kontrol et"""
    db_url = _get_database_url()
    if not db_url:
        return None  # Kontrol edilemedi

    try:
        import psycopg2
        conn = psycopg2.connect(db_url, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('ogretmenler', 'ogrenciler', 'test_sonuclari', 'ai_analizler', 'aile_ozetleri')
        """)
        mevcut = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return mevcut
    except Exception:
        return None
