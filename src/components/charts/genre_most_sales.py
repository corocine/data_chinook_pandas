import streamlit as st
import pandas as pd
import plotly.express as px
from ..colors.colors import SECONDARY_COLOR

def show_genre_sales_bar_chart(df: pd.DataFrame):
    """
    Cria um gráfico de BARRAS VERTICAL dos top 10 gêneros mais vendidos,
    mostrando a receita no hover.
    """
    if df.empty:
        st.warning("Nenhum dado disponível.")
        return

    df_invoices = df.drop_duplicates(subset=['InvoiceId'])
    revenue_by_genre = df_invoices.groupby('genreName')['invoiceTotal'].sum()
    

    genre_counts = df['genreName'].value_counts()

    analysis_df = pd.DataFrame({
        'quantidade_de_faixas': genre_counts,
        'receita_total': revenue_by_genre
    })

    top_10_genres = analysis_df.nlargest(10, 'quantidade_de_faixas').reset_index()

    fig_bar_genre = px.bar(
        data_frame=top_10_genres,
        x='genreName',
        y='quantidade_de_faixas',
        title='Top 10 Gêneros por Faixas Vendidas',
        text='quantidade_de_faixas',
        hover_data=['receita_total'] 
    )

    fig_bar_genre.update_traces(
        marker_color=SECONDARY_COLOR, 
        texttemplate='%{y}',
        textposition='outside',
        cliponaxis=False,

        hovertemplate=(
            "<b>Gênero:</b> %{x}<br>"
            "<b>Faixas Vendidas:</b> %{y}<br>"
            "<b>Receita Gerada:</b> $ %{customdata[0]:,.2f}" 
            "<extra></extra>"
        )
    )
    
    fig_bar_genre.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        title_xanchor="center",
        xaxis_title="Gênero Musical",                
        yaxis_title="Quantidade de Faixas Vendidas", 
        xaxis={'categoryorder':'total descending'},
        xaxis_tickangle=-45 
    )
    
    st.plotly_chart(fig_bar_genre, use_container_width=True)
