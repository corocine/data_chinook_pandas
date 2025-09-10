import streamlit as st
import pandas as pd
import plotly.express as px

def get_artist_affinity(df: pd.DataFrame, primary_genre: str):
    """
    Encontra os artistas mais comprados por clientes de um gênero principal.
    """
    
    primary_buyers_ids = df[df['genreName'] == primary_genre]['CustomerId'].unique()
    
    purchases_by_primary_buyers = df[df['CustomerId'].isin(primary_buyers_ids)]
    
    artists_in_primary_genre = set(df[df['genreName'] == primary_genre]['artistName'].unique())
    
    affinity_counts = purchases_by_primary_buyers[
        ~purchases_by_primary_buyers['artistName'].isin(artists_in_primary_genre)
    ]['artistName'].value_counts().reset_index()
    
    affinity_counts.columns = ['ArtistaCompradoJunto', 'QuantidadeDeFaixas']
    
    return affinity_counts.nlargest(15, 'QuantidadeDeFaixas')

def show_artist_affinity_treemap(df: pd.DataFrame):
    """
    Cria um componente interativo para analisar a afinidade entre Gênero e Artista,
    com formatação customizada.
    """
    
    primary_genre_options = df['genreName'].value_counts().nlargest(10).index.tolist()
    
    
    selected_genre = st.selectbox(
        "Defina um genêro ",
        options=primary_genre_options,
        key='artist_affinity_selectbox',
        width=250
        
    )

    if selected_genre:
        affinity_df = get_artist_affinity(df, selected_genre)

        if affinity_df.empty:
            st.warning(f"Não foram encontrados outros artistas comprados pelos clientes de {selected_genre}.")
        else:
            fig = px.treemap(
                affinity_df,
                path=[px.Constant(f""), 'ArtistaCompradoJunto'],
                values='QuantidadeDeFaixas',
                title=f"Top 15 artistas mais comprados por clientes que compraram: '{selected_genre}'",
                color='QuantidadeDeFaixas',
                color_continuous_scale=px.colors.sequential.Blues
            )

            fig.update_traces(
                texttemplate="<b>%{label}</b><br>%{value} faixas",
                hovertemplate="<b>%{label}</b><br>Faixas Compradas: %{value}<extra></extra>"
            )
            
            fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), title_x=0.5, title_xanchor="center")
            
            st.plotly_chart(fig, use_container_width=True)