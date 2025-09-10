import streamlit as st
import pandas as pd
import plotly.express as px
from ..colors.colors import PRIMARY_COLOR


def show_annual_revenue(df: pd.DataFrame):
    
    if df.empty:
        st.warning("Nenhum dado disponível para o período selecionado.")
        return

    df_invoices = df.drop_duplicates(subset=['InvoiceId'])

    annual_revenue = (
        df_invoices.groupby(df_invoices['InvoiceDate'].dt.year)['invoiceTotal']
        .sum()
        .reset_index()
        .rename(columns={'InvoiceDate': 'Ano', 'invoiceTotal': 'Receita'})
        .sort_values(by='Ano', ascending=True)
    )
    
    fig_annual_revenue = px.line(
        data_frame=annual_revenue,
        x='Ano',
        y='Receita',
        title='Evolução da Receita Anual',
        labels={'Receita': 'Receita ($)', 'Ano': 'Ano'},
        markers=True,
    )

    fig_annual_revenue.update_traces(
        line=dict(color=PRIMARY_COLOR, width=3),
        hovertemplate="<b>Ano:</b> %{x}<br><b>Receita:</b> $ %{y:,.2f}<extra></extra>"
    )

    fig_annual_revenue.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        title_xanchor="center",
        yaxis=(dict(showgrid=True, gridcolor='#333')),
        xaxis=(dict(showgrid=False, type='category')) 
    )

    st.plotly_chart(fig_annual_revenue, use_container_width=True)