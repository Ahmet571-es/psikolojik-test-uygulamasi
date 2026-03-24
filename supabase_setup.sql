-- ============================================
-- Eğitim Check-Up - Supabase Tablo Kurulumu
-- ============================================
-- Bu SQL'i Supabase Dashboard > SQL Editor'da çalıştırın.
-- https://supabase.com/dashboard/project/hebahuvzxoiaemtgcxir/sql

-- 1. Öğretmenler tablosu
CREATE TABLE IF NOT EXISTS ogretmenler (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    kullanici_adi TEXT UNIQUE NOT NULL,
    sifre_hash TEXT NOT NULL,
    okul TEXT,
    kayit_tarihi TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Öğrenciler tablosu
CREATE TABLE IF NOT EXISTS ogrenciler (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    sinif TEXT,
    okul TEXT,
    ogretmen_id UUID REFERENCES ogretmenler(id),
    kayit_tarihi TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Test sonuçları tablosu
CREATE TABLE IF NOT EXISTS test_sonuclari (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
    test_tipi TEXT NOT NULL,
    cevaplar JSONB,
    puanlar JSONB,
    sonuc_ozeti JSONB,
    tarih TIMESTAMPTZ DEFAULT NOW()
);

-- 4. AI analiz sonuçları tablosu
CREATE TABLE IF NOT EXISTS ai_analizler (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
    ogretmen_id UUID REFERENCES ogretmenler(id),
    test_tipleri JSONB,
    analiz_metni TEXT,
    analiz_tipi TEXT DEFAULT 'tekli',
    tarih TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Aile bilgilendirme özetleri tablosu
CREATE TABLE IF NOT EXISTS aile_ozetleri (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ogrenci_id UUID REFERENCES ogrenciler(id) ON DELETE CASCADE,
    ogretmen_id UUID REFERENCES ogretmenler(id),
    secilen_basliklar JSONB,
    ozet_metni TEXT,
    test_tipleri JSONB,
    olusturma_tarihi TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Demo öğretmen hesabı (kullanıcı: demo, şifre: demo123)
INSERT INTO ogretmenler (ad, soyad, kullanici_adi, sifre_hash, okul)
VALUES (
    'Demo',
    'Öğretmen',
    'demo',
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
    'Demo Okul'
) ON CONFLICT (kullanici_adi) DO NOTHING;

-- 7. Row Level Security (RLS) - Temel güvenlik
ALTER TABLE ogretmenler ENABLE ROW LEVEL SECURITY;
ALTER TABLE ogrenciler ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_sonuclari ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_analizler ENABLE ROW LEVEL SECURITY;
ALTER TABLE aile_ozetleri ENABLE ROW LEVEL SECURITY;

-- Servis rolü için tam erişim (Streamlit backend)
CREATE POLICY IF NOT EXISTS "Servis tam erişim - ogretmenler" ON ogretmenler
    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "Servis tam erişim - ogrenciler" ON ogrenciler
    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "Servis tam erişim - test_sonuclari" ON test_sonuclari
    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "Servis tam erişim - ai_analizler" ON ai_analizler
    FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY IF NOT EXISTS "Servis tam erişim - aile_ozetleri" ON aile_ozetleri
    FOR ALL USING (true) WITH CHECK (true);

-- İndeksler (performans)
CREATE INDEX IF NOT EXISTS idx_ogrenciler_ogretmen ON ogrenciler(ogretmen_id);
CREATE INDEX IF NOT EXISTS idx_test_sonuclari_ogrenci ON test_sonuclari(ogrenci_id);
CREATE INDEX IF NOT EXISTS idx_test_sonuclari_tip ON test_sonuclari(test_tipi);
CREATE INDEX IF NOT EXISTS idx_ai_analizler_ogrenci ON ai_analizler(ogrenci_id);
CREATE INDEX IF NOT EXISTS idx_aile_ozetleri_ogrenci ON aile_ozetleri(ogrenci_id);
CREATE INDEX IF NOT EXISTS idx_aile_ozetleri_ogretmen ON aile_ozetleri(ogretmen_id);
