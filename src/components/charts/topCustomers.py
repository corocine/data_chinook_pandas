import streamlit as st
import pandas as pd

def show_top_customers_ranking(df: pd.DataFrame):
    """
    Calcula e exibe um ranking com os 10 clientes que mais gastaram.
    """

    if df.empty:
        st.warning("Nenhum dado disponível para o período selecionado.")
        return

    df_faturas = df.drop_duplicates(subset=['InvoiceId'])
    revenue_by_customer = df_faturas.groupby('CustomerId')['invoiceTotal'].sum()


    tracks_by_customer = df.groupby('CustomerId')['InvoiceLineId'].count()


    df_ranking = pd.DataFrame({
        'ReceitaTotal': revenue_by_customer,
        'FaixasCompradas': tracks_by_customer
    }).reset_index()

    customer_info = df[['CustomerId', 'customerFirstName', 'customerLastName', 'customerCountry']].drop_duplicates()
    df_ranking = pd.merge(df_ranking, customer_info, on='CustomerId')

    df_ranking['NomeCompleto'] = df_ranking['customerFirstName'] + ' ' + df_ranking['customerLastName']

    top_10_customers = df_ranking.sort_values(by='ReceitaTotal', ascending=False).head(10)

    top_10_customers = top_10_customers[['NomeCompleto', 'customerCountry', 'ReceitaTotal', 'FaixasCompradas']]


    st.dataframe(
        top_10_customers,
        use_container_width=True,
        column_config={
            "NomeCompleto": st.column_config.TextColumn("Cliente"),
            "customerCountry": st.column_config.TextColumn("País"),
            "FaixasCompradas": st.column_config.NumberColumn(
                "Faixas Compradas",
                format="%d faixas"
            ),
            "ReceitaTotal": st.column_config.NumberColumn(
                "Receita Total ($)",
                width="small",
            )
        },
        hide_index=True 
    )

