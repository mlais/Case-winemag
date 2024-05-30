import pandas as pd
import streamlit as st
import plotly.express as px
import re

# Carregar o dataset
df = pd.read_csv('winemag-data-130k-v2.csv')

# Função para extrair o ano do título ou descrição
def extract_year(title):
    match = re.search(r'\b(19|20)\d{2}\b', title)
    return int(match.group(0)) if match else None

# Aplicar a função para extrair o ano
df['year'] = df['title'].apply(extract_year)

# Remover linhas com ano ou preço ausentes
df = df.dropna(subset=['year', 'price'])

# Título da aplicação
st.title("Comparação de Preços de Vinhos por Variedade e Ano")

# Seleção de Ano
years = sorted(df['year'].dropna().unique())
selected_year = st.selectbox('Selecione o Ano', years)

# Seleção de Variedades
varieties = df['variety'].unique()
selected_varieties = st.multiselect('Selecione as Variedades', varieties, default=['Chardonnay', 'Pinot Noir'])

# Filtrar o dataframe com base no ano e nas variedades selecionadas
filtered_df = df[(df['year'] == selected_year) & (df['variety'].isin(selected_varieties))]

# Criar o box plot para visualização no Streamlit
fig = px.box(filtered_df, x='variety', y='price', color='variety', 
             title=f'Comparação de Preços para {selected_year}',
             labels={'price': 'Preço', 'variety': 'Variedade'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

