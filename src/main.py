from pathlib import Path
import streamlit as st
import pandas as pd
from components.filters.sidebar import create_sidebar_filters
from components.metrics import show_metrics
from components.charts.annual_revenue import show_annual_revenue
from components.charts.genre_most_sales import show_genre_sales_bar_chart
from components.charts.customers_country import show_side_by_side_charts
from components.charts.media_types_revenue import  show_media_type_revenue_pie_chart
from components.charts.customers_preferences import show_artist_affinity_treemap
from components.charts.employees import show_employee_performance_scatter
from components.charts.topCustomers import show_top_customers_ranking

def main():
    """
    Main function that orchestrates the creation and display of the dashboard.
    """
    
    st.set_page_config(
        page_title=' Vendas Chinook',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.markdown("<h1 style='text-align: center; padding-bottom: 50px;;'>Análise  de Vendas - Loja de Músicas Chinook</h1>", unsafe_allow_html=True)

    @st.cache_data
    def load_parquet():
        """
        Lê os dados processados do arquivo Parquet.
        Retorna um DataFrame ou None se o arquivo não for encontrado.
        """
        SCRIPT_DIR = Path(__file__).parent
        BASE_DIR = SCRIPT_DIR.parent.parent
        PARQUET_PATH = BASE_DIR / 'data' / "chinook_processed.parquet"
        
        try:
            df = pd.read_parquet(PARQUET_PATH)
            return df
        except FileNotFoundError:
            st.error(f"ERRO: Arquivo Parquet não encontrado em: {PARQUET_PATH}")
            st.info("Por favor, execute o script de preparação para gerar o arquivo Parquet primeiro.")
            return None

    df = load_parquet()

    if df is None:
        st.info("Nenhum dado disponível para exibição.")
        st.stop()

    df_filtred = create_sidebar_filters(df)
    
    if df_filtred.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")

    show_metrics(df_filtred)
 
    st.markdown("<h2 style='text-align: center; padding-bottom: 50px;;'>Qual a origem da receita?</h2>", unsafe_allow_html=True)
    
    show_annual_revenue(df_filtred)
    
    show_genre_sales_bar_chart(df_filtred)
    
    show_side_by_side_charts(df_filtred)
    
    col1, col2 = st.columns(2)
    with col1:
        show_media_type_revenue_pie_chart(df_filtred)
    with col2:
        show_employee_performance_scatter(df_filtred)
        
        
    st.markdown("<h2 style='text-align: center; padding-bottom: 50px;;'>Padrões de consumo dos clientes</h2>", unsafe_allow_html=True)
        
    show_artist_affinity_treemap(df_filtred)

    st.markdown("<h2 style='text-align: center; padding-bottom: 50px;;'>Top 10 Clientes por Faturamento</h2>", unsafe_allow_html=True)
    show_top_customers_ranking(df_filtred)


if __name__ == "__main__":
    main()
    
    