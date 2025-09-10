import streamlit as st


def create_sidebar_filters(df):
    """
    Cria e exibe os filtros na sidebar a partir do DataFrame principal.

    Args:
        df (pd.DataFrame): O DataFrame carregado com os dados do Parquet.
    
    Returns:
        tuple: Uma tupla contendo as seleções do usuário para cada filtro.
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

    min_date = df['InvoiceDate'].min().to_pydatetime()
    max_date = df['InvoiceDate'].max().to_pydatetime()

    selected_date_range = st.sidebar.date_input(
        "Selecione o Período:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
    else:
        start_date, end_date = min_date, max_date
        
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
