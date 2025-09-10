import streamlit as st
import pandas as pd
import plotly.express as px



def show_employee_performance_scatter(df: pd.DataFrame):
    """
    Cria um gráfico de dispersão (bolhas) para analisar a performance dos
    vendedores (Receita Total vs. Ticket Médio) usando Plotly Express.
    """

    if df.empty:
        st.warning("Nenhum dado disponível.")
        return
    
    df_faturas = df.drop_duplicates(subset=['InvoiceId'])
    
    analysis_df = (
        df_faturas.groupby('employeeFirstName')
        .agg(
            ReceitaTotal=('invoiceTotal', 'sum'),
            TicketMedio=('invoiceTotal', 'mean')
        )
        .reset_index()
    )

    fig = px.scatter(
        data_frame=analysis_df,
        x='ReceitaTotal',
        y='TicketMedio',
        size='ReceitaTotal',   
        color='employeeFirstName',
        text='employeeFirstName', 
        title='Receita Total vs. Ticket Médio por Vendedor',
        labels={
            'ReceitaTotal': 'Receita Total Gerada ($)',
            'TicketMedio': 'Ticket Médio por Venda ($)',
            'employeeFirstName': 'Vendedor'
        },
        hover_name='employeeFirstName',
        hover_data={
            'ReceitaTotal': ':$.,2f', 
            'TicketMedio': ':$.,2f',  
            'employeeFirstName': False 
        }
    )

    fig.update_traces(
        textposition='top center',
        hovertemplate=(
            "<b>Receita Total:</b> $ %{x}<br>"
            "<b>Ticket Medio:</b> %{y:.2f}<br>"
            "<extra></extra>" 
        )
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        title_xanchor="center",
        legend_title_text='Vendedor'
    )
    
    st.plotly_chart(fig, use_container_width=True)
