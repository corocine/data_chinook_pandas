import pandas as pd
import plotly.express as px
import streamlit as st

def show_media_type_revenue_pie_chart(df: pd.DataFrame):
    """
    Cria e exibe um gráfico de pizza (rosca) da proporção da receita
    por tipo de mídia.
    """
    if df.empty:
        st.warning("Nenhum dado disponível para o período selecionado.")
        return
    
    df_faturas = df.drop_duplicates(subset=['InvoiceId'])

    total_vendido_por_tipo = df_faturas.groupby('mediaTypeName')['invoiceTotal'].sum()

    porcentagem_vendido_por_tipo = round((total_vendido_por_tipo / total_vendido_por_tipo.sum()) * 100, 2)

    vendas_por_tipo_midia = pd.DataFrame({
        'total_vendido': total_vendido_por_tipo,
        'porcentagem_vendido': porcentagem_vendido_por_tipo
    }).reset_index().sort_values(by='total_vendido', ascending=False)
    
    df_faturas = df.drop_duplicates(subset=['InvoiceId'])
    total_vendido_por_tipo = df_faturas.groupby('mediaTypeName')['invoiceTotal'].sum()
    
    vendas_por_tipo_midia = total_vendido_por_tipo.reset_index()
    vendas_por_tipo_midia.columns = ['mediaTypeName', 'total_vendido']

    fig_pie = px.pie(
        data_frame=vendas_por_tipo_midia,
        names='mediaTypeName',          
        values='total_vendido',           
        title='Proporção da Receita por Tipo de Mídia',
        hole=0.4,                        
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent', 
        hovertemplate="<b>%{label}</b><br>Receita: $ %{value:,.2f}<br>Proporção: %{percent}<extra></extra>"
    )

    fig_pie.update_layout(
        title_x=0.5,
        title_xanchor="center",
        legend_title_text='Tipos de Mídia'
    )

    st.plotly_chart(fig_pie, use_container_width=True)
