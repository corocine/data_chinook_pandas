import streamlit as st
import pandas as pd
from datetime import datetime

def create_sidebar_filters(df):
    """
    Cria e exibe os filtros na sidebar a partir do DataFrame principal.

    Args:
        df (pd.DataFrame): O DataFrame carregado com os dados do Parquet.
    
    Returns:
        pd.DataFrame: Um novo DataFrame filtrado de acordo com as seleções do usuário.
    """
    st.sidebar.markdown("<h1 style='text-align: center;'> Preferências </h1>", unsafe_allow_html=True)

    countries = sorted(df['customerCountry'].unique().tolist())
    genres = sorted(df['genreName'].unique().tolist())
    media_types = sorted(df['mediaTypeName'].unique().tolist())

    selected_countries = st.sidebar.multiselect(
        "Selecione os Países:",
        options=countries,
        default=[]
    )

    selected_genres = st.sidebar.multiselect(
        "Selecione os Gêneros Musicais:",
        options=genres,
        default=[]
    )

    selected_media_types = st.sidebar.multiselect(
        "Selecione os Tipos de Mídia:",
        options=media_types,
        default=[]
    )

    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()

    selected_date_range = st.sidebar.date_input(
        "Selecione o Período:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    
    start_date = min_date
    end_date = max_date
    
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range

    df_filtered = df.copy()
    df_filtered = df_filtered[
        (df_filtered['InvoiceDate'].dt.date >= start_date) &
        (df_filtered['InvoiceDate'].dt.date <= end_date)
    ]
    
    if selected_countries:
        df_filtered = df_filtered[df_filtered['customerCountry'].isin(selected_countries)]
    
    if selected_genres:
        df_filtered = df_filtered[df_filtered['genreName'].isin(selected_genres)]

    if selected_media_types:
        df_filtered = df_filtered[df_filtered['mediaTypeName'].isin(selected_media_types)]
    
    return df_filtered