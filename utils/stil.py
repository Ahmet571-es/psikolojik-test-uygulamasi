# -*- coding: utf-8 -*-
"""Eğitim Check-Up - UI Stilleri ve Yardımcı Fonksiyonlar"""

import streamlit as st


def uygula_genel_stil():
    """Uygulamanın genel CSS stillerini uygula"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1e293b;
        }

        .main-header {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #1E293B, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .sub-header {
            font-size: 1.1rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 300;
        }

        .test-card {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #3B82F6;
            margin-bottom: 1rem;
            transition: transform 0.2s;
        }

        .test-card:hover {
            transform: translateY(-2px);
        }

        .question-card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #3B82F6;
            margin-bottom: 1.5rem;
        }

        .sonuc-kutusu {
            background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #93C5FD;
            margin-bottom: 1rem;
        }

        .rapor-bolumu {
            background: #F8FAFC;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }

        .istatistik-kutusu {
            background: white;
            padding: 1.2rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            border: 1px solid #E2E8F0;
        }

        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        div.stButton > button:hover {
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)


def baslik_goster(baslik, alt_baslik=""):
    """Ana başlık göster"""
    st.markdown(f'<div class="main-header">{baslik}</div>', unsafe_allow_html=True)
    if alt_baslik:
        st.markdown(f'<div class="sub-header">{alt_baslik}</div>', unsafe_allow_html=True)


def bilgi_karti(baslik, deger, ikon="", renk="#3B82F6"):
    """İstatistik bilgi kartı göster"""
    st.markdown(f"""
    <div class="istatistik-kutusu">
        <div style="font-size: 2rem;">{ikon}</div>
        <div style="font-size: 1.8rem; font-weight: 700; color: {renk};">{deger}</div>
        <div style="font-size: 0.9rem; color: #64748B;">{baslik}</div>
    </div>
    """, unsafe_allow_html=True)


def sonuc_kutusu(icerik):
    """Sonuç gösterim kutusu"""
    st.markdown(f'<div class="sonuc-kutusu">{icerik}</div>', unsafe_allow_html=True)
