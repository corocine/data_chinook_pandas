import streamlit as st
import pandas as pd

def show_metrics(df):
    """
    Calcula métricas chave a partir do DataFrame fornecido.

    Args:
        df (pd.DataFrame): O DataFrame carregado com os dados do Parquet.
    
    Returns:
        dict: Um dicionário contendo as métricas calculadas.
    """
    df_faturas_unicas = df.drop_duplicates(subset=['InvoiceId'])

    total_revenue = round(df_faturas_unicas['invoiceTotal'].sum(), 2)
    num_sales = df_faturas_unicas['InvoiceId'].nunique()
    avg_sale_value = round(total_revenue / num_sales, 2) if num_sales > 0 else 0
    total_customers = df['CustomerId'].nunique()
    total_tracks_sold = (df['InvoiceLineId'].count())
    country_count = df['customerCountry'].nunique()
    date_min = df['InvoiceDate'].min().to_pydatetime().date()
    date_max = df['InvoiceDate'].max().to_pydatetime().date()
    

    col1, col2, col3, col7 = st.columns(4)

    with col1:
        st.metric('Receita total', f'$ {total_revenue:,.2f}')
    with col2:
        st.metric('Total de vendas', num_sales)
    with col3:
        st.metric('Ticket médio', f'$ {avg_sale_value:,.2f}')
    with col7:
        st.metric('Período inicial', f'{date_min}')

    col4, col5, col6, col8 = st.columns(4)
    
    with col4:
        st.metric('Clientes', total_customers)
    with col5:
        st.metric('Total de músicas vendidas', f'{total_tracks_sold:,}')
    with col6:
        st.metric('Países atendidos', country_count)
    with col8:
        st.metric('Período final', f'{date_max}')
    
    st.markdown('---')
    