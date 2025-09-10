import plotly.express as px
import streamlit as st
from ..colors.colors import  PRIMARY_COLOR
import streamlit as st
import pandas as pd
import plotly.express as px


def show_side_by_side_charts(df: pd.DataFrame):
    """
    Exibe dois gráficos de barras lado a lado com customizações.
    """
    # Verificação de segurança para o DataFrame de entrada
    if df.empty:
        st.warning("Nenhum dado para exibir os gráficos lado a lado.")
        return

    df_faturas = df.drop_duplicates(subset=['InvoiceId'])
    
    top5_countries = df_faturas['customerCountry'].value_counts().nlargest(5).index.tolist()
    
    df_top5 = df_faturas[df_faturas['customerCountry'].isin(top5_countries)]
    
    analysis = df_top5.groupby('customerCountry').agg(
        media_gasto_cliente=('invoiceTotal', 'mean'),
        total_clientes=('CustomerId', 'nunique')
    ).reset_index()
    
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            analysis.sort_values('total_clientes', ascending=False),
            x='customerCountry', y='total_clientes',
            title='Top 5 Países por Número de Clientes',
            text='total_clientes'
        )
        
        fig1.update_traces(
            marker_color=PRIMARY_COLOR, 
            hovertemplate="<b>País:</b> %{x}<br><b>Total de Clientes:</b> %{y}<extra></extra>" 
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            title_x=0.5,
            title_xanchor="center",
            xaxis_title="País",
            yaxis_title="Número de Clientes"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            analysis.sort_values('media_gasto_cliente', ascending=False),
            x='customerCountry', y='media_gasto_cliente',
            title='Gasto Médio por Venda (Top 5 Países)',
            text='media_gasto_cliente'
        )
        
        fig2.update_traces(
            marker_color=PRIMARY_COLOR, 
            texttemplate='US$ %{y:,.2f}',
            hovertemplate="<b>País:</b> %{x}<br><b>Gasto Médio:</b> $ %{y:,.2f}<extra></extra>" 
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            title_x=0.5,
            title_xanchor="center",
            xaxis_title="País",
            yaxis_title="Gasto Médio ($)"
        )
        st.plotly_chart(fig2, use_container_width=True)