# -*- coding: utf-8 -*-
"""Eğitim Check-Up - Öğretmen Paneli Modülü"""

import streamlit as st
import json
import io
from datetime import datetime
from config import TEST_MODULLERI


def ogretmen_giris_formu():
    """Öğretmen giriş formunu göster"""
    st.markdown("### Öğretmen Girişi")

    with st.form("ogretmen_giris"):
        kullanici_adi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        giris_btn = st.form_submit_button("Giriş Yap", type="primary")

        if giris_btn:
            if not kullanici_adi or not sifre:
                st.error("Kullanıcı adı ve şifre gereklidir.")
                return False

            from veritabani import ogretmen_giris
            ogretmen = ogretmen_giris(kullanici_adi, sifre)

            if ogretmen:
                st.session_state["ogretmen"] = ogretmen
                st.session_state["ogretmen_giris"] = True
                st.success(f"Hoş geldiniz, {ogretmen.get('ad', '')} {ogretmen.get('soyad', '')}!")
                st.rerun()
                return True
            else:
                # Demo mod: Supabase yoksa demo giriş
                if kullanici_adi == "demo" and sifre == "demo123":
                    st.session_state["ogretmen"] = {
                        "id": "demo",
                        "ad": "Demo",
                        "soyad": "Öğretmen",
                        "kullanici_adi": "demo",
                        "okul": "Demo Okul"
                    }
                    st.session_state["ogretmen_giris"] = True
                    st.success("Demo modda giriş yapıldı.")
                    st.rerun()
                    return True
                st.error("Kullanıcı adı veya şifre hatalı.")
                return False
    return False


def ogrenci_yonetimi():
    """Öğrenci ekleme ve listeleme"""
    st.markdown("### Öğrenci Yönetimi")

    tab_liste, tab_ekle = st.tabs(["Öğrenci Listesi", "Yeni Öğrenci Ekle"])

    with tab_ekle:
        with st.form("ogrenci_ekle"):
            col1, col2 = st.columns(2)
            with col1:
                ad = st.text_input("Ad")
                sinif = st.text_input("Sınıf (örn: 9-A)")
            with col2:
                soyad = st.text_input("Soyad")
                okul = st.text_input("Okul")

            if st.form_submit_button("Öğrenci Ekle", type="primary"):
                if not ad or not soyad:
                    st.error("Ad ve soyad zorunludur.")
                else:
                    from veritabani import ogrenci_kaydet
                    ogretmen = st.session_state.get("ogretmen", {})
                    sonuc = ogrenci_kaydet(ad, soyad, sinif, okul, ogretmen.get("id"))
                    if sonuc:
                        st.success(f"{ad} {soyad} başarıyla eklendi.")
                        # Session state'e de ekle
                        if "ogrenciler" not in st.session_state:
                            st.session_state["ogrenciler"] = []
                        st.session_state["ogrenciler"].append({
                            "id": sonuc.get("id", len(st.session_state["ogrenciler"]) + 1),
                            "ad": ad, "soyad": soyad, "sinif": sinif, "okul": okul
                        })
                    else:
                        # Supabase yoksa lokalde kaydet
                        if "ogrenciler" not in st.session_state:
                            st.session_state["ogrenciler"] = []
                        st.session_state["ogrenciler"].append({
                            "id": len(st.session_state["ogrenciler"]) + 1,
                            "ad": ad, "soyad": soyad, "sinif": sinif, "okul": okul
                        })
                        st.success(f"{ad} {soyad} başarıyla eklendi (yerel).")

    with tab_liste:
        ogrenciler = st.session_state.get("ogrenciler", [])
        if not ogrenciler:
            # Veritabanından çek
            from veritabani import ogretmenin_ogrencileri
            ogretmen = st.session_state.get("ogretmen", {})
            db_ogrenciler = ogretmenin_ogrencileri(ogretmen.get("id", ""))
            if db_ogrenciler:
                ogrenciler = db_ogrenciler
                st.session_state["ogrenciler"] = ogrenciler

        if not ogrenciler:
            st.info("Henüz öğrenci eklenmemiş.")
        else:
            # Filtreleme
            filtre_sinif = st.selectbox(
                "Sınıfa göre filtrele",
                ["Tümü"] + list(set(o.get("sinif", "") for o in ogrenciler if o.get("sinif")))
            )

            for ogrenci in ogrenciler:
                if filtre_sinif != "Tümü" and ogrenci.get("sinif") != filtre_sinif:
                    continue
                with st.expander(f"{ogrenci['ad']} {ogrenci['soyad']} - {ogrenci.get('sinif', '')}"):
                    st.write(f"**Okul:** {ogrenci.get('okul', '-')}")
                    st.write(f"**Sınıf:** {ogrenci.get('sinif', '-')}")

                    if st.button(f"Testleri Gör", key=f"test_{ogrenci.get('id', '')}"):
                        st.session_state["secili_ogrenci"] = ogrenci
                        st.session_state["sayfa"] = "ogrenci_detay"
                        st.rerun()


def toplu_export():
    """Toplu Excel ve ZIP export"""
    st.markdown("### Toplu Veri İndirme")

    ogrenciler = st.session_state.get("ogrenciler", [])
    test_sonuclari = st.session_state.get("tum_test_sonuclari", {})

    if not ogrenciler:
        st.info("Dışa aktarılacak öğrenci verisi bulunamadı.")
        return

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Excel İndir", type="primary"):
            excel_data = _excel_olustur(ogrenciler, test_sonuclari)
            if excel_data:
                st.download_button(
                    label="Excel Dosyasını İndir",
                    data=excel_data,
                    file_name=f"egitim_checkup_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    with col2:
        if st.button("ZIP İndir (Tüm Raporlar)"):
            zip_data = _zip_olustur(ogrenciler, test_sonuclari)
            if zip_data:
                st.download_button(
                    label="ZIP Dosyasını İndir",
                    data=zip_data,
                    file_name=f"egitim_checkup_raporlar_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip"
                )


def _excel_olustur(ogrenciler, test_sonuclari):
    """Toplu Excel dosyası oluştur"""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Öğrenci Listesi"

        # Başlık stili
        baslik_font = Font(bold=True, size=12, color="FFFFFF")
        baslik_fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid")

        # Başlıklar
        basliklar = ["Ad", "Soyad", "Sınıf", "Okul", "Yapılan Testler", "Son Test Tarihi"]
        for col, baslik in enumerate(basliklar, 1):
            cell = ws.cell(row=1, column=col, value=baslik)
            cell.font = baslik_font
            cell.fill = baslik_fill
            cell.alignment = Alignment(horizontal="center")

        # Veriler
        for row, ogrenci in enumerate(ogrenciler, 2):
            ws.cell(row=row, column=1, value=ogrenci.get("ad", ""))
            ws.cell(row=row, column=2, value=ogrenci.get("soyad", ""))
            ws.cell(row=row, column=3, value=ogrenci.get("sinif", ""))
            ws.cell(row=row, column=4, value=ogrenci.get("okul", ""))

            ogrenci_id = str(ogrenci.get("id", ""))
            testler = test_sonuclari.get(ogrenci_id, {})
            ws.cell(row=row, column=5, value=", ".join(testler.keys()) if testler else "-")
            ws.cell(row=row, column=6, value=datetime.now().strftime("%d.%m.%Y"))

        # Sütun genişlikleri
        for col in range(1, 7):
            ws.column_dimensions[chr(64 + col)].width = 18

        # Test sonuçları sayfası
        if test_sonuclari:
            ws2 = wb.create_sheet("Test Sonuçları")
            satir = 1
            for ogrenci_id, testler in test_sonuclari.items():
                for test_adi, sonuc in testler.items():
                    if satir == 1:
                        ws2.cell(row=1, column=1, value="Öğrenci ID")
                        ws2.cell(row=1, column=2, value="Test")
                        ws2.cell(row=1, column=3, value="Sonuç")
                        satir = 2

                    ws2.cell(row=satir, column=1, value=str(ogrenci_id))
                    ws2.cell(row=satir, column=2, value=test_adi)
                    ws2.cell(row=satir, column=3, value=json.dumps(sonuc, ensure_ascii=False))
                    satir += 1

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        st.error(f"Excel oluşturma hatası: {e}")
        return None


def _zip_olustur(ogrenciler, test_sonuclari):
    """Toplu ZIP dosyası oluştur"""
    try:
        import zipfile
        from rapor_olusturucu import pdf_olustur

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for ogrenci in ogrenciler:
                ogrenci_id = str(ogrenci.get("id", ""))
                ogrenci_adi = f"{ogrenci.get('ad', '')} {ogrenci.get('soyad', '')}"
                testler = test_sonuclari.get(ogrenci_id, {})

                for test_adi, sonuc in testler.items():
                    pdf_bytes = pdf_olustur(ogrenci_adi, test_adi, sonuc)
                    dosya_adi = f"{ogrenci_adi}_{test_adi}.pdf".replace(" ", "_")
                    zf.writestr(dosya_adi, pdf_bytes)

            if not test_sonuclari:
                zf.writestr("bilgi.txt", "Henüz test sonucu bulunmamaktadır.")

        zip_buf.seek(0)
        return zip_buf.getvalue()
    except Exception as e:
        st.error(f"ZIP oluşturma hatası: {e}")
        return None
