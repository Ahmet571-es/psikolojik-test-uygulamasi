# -*- coding: utf-8 -*-
"""Eğitim Check-Up - Aile Bilgilendirme Modülü"""

import streamlit as st
import json
from datetime import datetime
from config import AILE_KONU_BASLIKLARI, TEST_KONU_ILISKISI, TEST_MODULLERI


def aktif_basliklari_belirle(yapilan_testler):
    """Yapılan testlere göre aktif/pasif başlıkları belirle"""
    aktif_basliklar = set()
    for test_tipi in yapilan_testler:
        ilgili = TEST_KONU_ILISKISI.get(test_tipi, [])
        aktif_basliklar.update(ilgili)

    # Genel Değerlendirme her zaman aktif
    aktif_basliklar.add("Genel Değerlendirme")

    return aktif_basliklar


def aile_bilgilendirme_goster(ogrenci_adi, analiz_sonuclari, yapilan_testler, ogrenci_id=None, ogretmen_id=None):
    """Aile bilgilendirme özeti oluşturma arayüzünü göster"""

    st.markdown("---")
    st.markdown("### Aile Bilgilendirme Özeti Oluştur")
    st.caption("AI analiz sonuçlarına dayanarak aileye yönelik özet rapor hazırlayın.")

    aktif_basliklar = aktif_basliklari_belirle(yapilan_testler)

    # Konu başlıkları seçimi
    st.markdown("#### Konu Başlıklarını Seçin")
    secilen_basliklar = []

    col1, col2 = st.columns(2)
    for i, baslik in enumerate(AILE_KONU_BASLIKLARI):
        aktif = baslik in aktif_basliklar
        with col1 if i % 2 == 0 else col2:
            if aktif:
                secildi = st.checkbox(baslik, key=f"aile_baslik_{i}", value=False)
                if secildi:
                    secilen_basliklar.append(baslik)
            else:
                st.checkbox(baslik, key=f"aile_baslik_{i}", value=False, disabled=True,
                           help="Bu başlık için ilgili test yapılmamış.")

    # Öğretmen notu
    st.markdown("#### Öğretmen Notu")
    ogretmen_notu = st.text_area(
        "Eklemek istediğiniz özel not veya konu başlığı...",
        placeholder="Örn: Öğrenci son dönemde derslerine karşı ilgisini kaybetti...",
        key="aile_ogretmen_notu"
    )

    # Özet oluştur butonu
    if st.button("Özet Oluştur", type="primary", key="aile_ozet_olustur",
                 disabled=len(secilen_basliklar) == 0):
        if not secilen_basliklar:
            st.error("Lütfen en az bir konu başlığı seçin.")
            return

        with st.spinner("Aile özeti hazırlanıyor..."):
            from ai_analiz import aile_ozeti_olustur
            ozet = aile_ozeti_olustur(
                ogrenci_adi=ogrenci_adi,
                analiz_sonuclari=analiz_sonuclari,
                secilen_basliklar=secilen_basliklar,
                ogretmen_notu=ogretmen_notu
            )

            if ozet:
                st.session_state["aile_ozet_metni"] = ozet
                st.session_state["aile_secilen_basliklar"] = secilen_basliklar
                st.session_state["aile_ogrenci_adi"] = ogrenci_adi
                st.session_state["aile_yapilan_testler"] = yapilan_testler
            else:
                st.error("Özet oluşturulamadı. Lütfen tekrar deneyin.")
                # Yeniden deneme butonu
                if st.button("Yeniden Dene", key="aile_yeniden_dene"):
                    st.rerun()
                return

    # Özet önizleme ve düzenleme
    if "aile_ozet_metni" in st.session_state and st.session_state["aile_ozet_metni"]:
        st.markdown("---")
        st.markdown("### Özet Önizleme")
        st.caption("Metni düzenleyebilirsiniz.")

        duzenlenmis_metin = st.text_area(
            "Aile Bilgilendirme Özeti",
            value=st.session_state["aile_ozet_metni"],
            height=400,
            key="aile_ozet_duzenle"
        )

        # Butonlar
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

        with col_btn1:
            # PDF İndir
            if st.button("PDF İndir", key="aile_pdf"):
                from aile_rapor_sablonu import aile_pdf_olustur
                ogretmen = st.session_state.get("ogretmen", {})
                pdf_data = aile_pdf_olustur(
                    ogrenci_adi=st.session_state.get("aile_ogrenci_adi", ogrenci_adi),
                    ozet_metni=duzenlenmis_metin,
                    ogretmen_adi=f"{ogretmen.get('ad', '')} {ogretmen.get('soyad', '')}".strip(),
                    secilen_basliklar=st.session_state.get("aile_secilen_basliklar", [])
                )
                if pdf_data:
                    st.download_button(
                        label="PDF Dosyasını İndir",
                        data=pdf_data,
                        file_name=f"veli_bilgilendirme_{ogrenci_adi}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="aile_pdf_download"
                    )

        with col_btn2:
            # DOCX İndir
            if st.button("DOCX İndir", key="aile_docx"):
                from aile_rapor_sablonu import aile_docx_olustur
                ogretmen = st.session_state.get("ogretmen", {})
                docx_data = aile_docx_olustur(
                    ogrenci_adi=st.session_state.get("aile_ogrenci_adi", ogrenci_adi),
                    ozet_metni=duzenlenmis_metin,
                    ogretmen_adi=f"{ogretmen.get('ad', '')} {ogretmen.get('soyad', '')}".strip(),
                    secilen_basliklar=st.session_state.get("aile_secilen_basliklar", [])
                )
                if docx_data:
                    st.download_button(
                        label="DOCX Dosyasını İndir",
                        data=docx_data,
                        file_name=f"veli_bilgilendirme_{ogrenci_adi}_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="aile_docx_download"
                    )

        with col_btn3:
            # Panoya kopyala
            if st.button("Kopyala", key="aile_kopyala"):
                st.code(duzenlenmis_metin, language=None)
                st.info("Metni yukarıdan seçip kopyalayabilirsiniz (Ctrl+C).")

        with col_btn4:
            # Yeniden oluştur
            if st.button("Yeniden Oluştur", key="aile_yeniden_olustur"):
                st.session_state["aile_ozet_metni"] = None
                st.rerun()

        # Veritabanına kaydet
        if duzenlenmis_metin != st.session_state.get("aile_ozet_metni", ""):
            st.session_state["aile_ozet_metni"] = duzenlenmis_metin

        # Supabase'e kaydet
        _kaydet_supabase(ogrenci_id, ogretmen_id, secilen_basliklar, duzenlenmis_metin, yapilan_testler)


def _kaydet_supabase(ogrenci_id, ogretmen_id, secilen_basliklar, ozet_metni, yapilan_testler):
    """Aile özetini Supabase'e kaydet"""
    if not ogrenci_id or not ogretmen_id:
        return

    kayit_key = f"aile_ozet_kaydedildi_{ogrenci_id}"
    if st.session_state.get(kayit_key):
        return

    try:
        from veritabani import aile_ozeti_kaydet
        sonuc = aile_ozeti_kaydet(
            ogrenci_id=ogrenci_id,
            ogretmen_id=ogretmen_id,
            secilen_basliklar=secilen_basliklar,
            ozet_metni=ozet_metni,
            test_tipleri=yapilan_testler
        )
        if sonuc:
            st.session_state[kayit_key] = True
    except Exception:
        pass  # Supabase bağlantısı yoksa sessizce geç


def aile_ozet_gecmisi(ogretmen_id=None, ogrenci_id=None):
    """Geçmiş aile özetlerini göster"""
    st.markdown("### Aile Bilgilendirme Geçmişi")

    from veritabani import aile_ozetleri_getir
    ozetler = aile_ozetleri_getir(ogrenci_id=ogrenci_id, ogretmen_id=ogretmen_id)

    if not ozetler:
        st.info("Henüz aile bilgilendirme özeti oluşturulmamış.")
        return

    for ozet in ozetler:
        tarih = ozet.get("olusturma_tarihi", "")
        with st.expander(f"Özet - {tarih[:10] if tarih else 'Tarih yok'}"):
            basliklar = ozet.get("secilen_basliklar", "[]")
            if isinstance(basliklar, str):
                basliklar = json.loads(basliklar)
            st.write(f"**Başlıklar:** {', '.join(basliklar)}")
            st.write(ozet.get("ozet_metni", ""))
