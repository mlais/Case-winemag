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
df = df.dropna(subset=['year', 'price', 'country'])

# Mapeamento dos nomes dos países para português
country_translation = {
    'US': 'Estados Unidos',
    'France': 'França',
    'Italy': 'Itália',
    'Spain': 'Espanha',
    'Argentina': 'Argentina',
    'Chile': 'Chile',
    'Australia': 'Austrália',
    'Portugal': 'Portugal',
    'New Zealand': 'Nova Zelândia',
    'South Africa': 'África do Sul',
    'Germany': 'Alemanha',
    'Austria': 'Áustria',
    'Canada': 'Canadá',
    'Greece': 'Grécia',
    'Israel': 'Israel',
    'Hungary': 'Hungria',
    'Romania': 'Romênia',
    'Slovenia': 'Eslovênia',
    'Uruguay': 'Uruguai',
    'Croatia': 'Croácia',
    'Georgia': 'Geórgia',
    'Mexico': 'México',
    'Brazil': 'Brasil',
    'Turkey': 'Turquia',
    'Lebanon': 'Líbano',
    'Morocco': 'Marrocos',
    'England': 'Inglaterra',
    'Moldova': 'Moldávia',
    'Luxembourg': 'Luxemburgo',
    'Bulgaria': 'Bulgária',
    'Peru': 'Peru',
    'India': 'Índia',
    'Ukraine': 'Ucrânia',
    'Czech Republic': 'República Tcheca',
    'Switzerland': 'Suíça',
    'Macedonia': 'Macedônia',
    'Serbia': 'Sérvia',
    'Bosnia and Herzegovina': 'Bósnia e Herzegovina',
    'Cyprus': 'Chipre',
    'Slovakia': 'Eslováquia',
    'China': 'China',
    'Armenia': 'Armênia',
    'Malta': 'Malta',
    'Japan': 'Japão',
    'Montenegro': 'Montenegro',
    'Lithuania': 'Lituânia',
    'Thailand': 'Tailândia',
    'Mexico': 'México',
}

# Traduzir os nomes dos países no dataframe
df['country_pt'] = df['country'].map(country_translation)

# Título da aplicação
st.title("Comparação de Preços de Vinhos por Variedade, Ano e País")

# Seleção de País
countries_pt = sorted(df['country_pt'].dropna().unique())
selected_country_pt = st.selectbox('Selecione o País', countries_pt)

# Mapear o nome do país de volta para o original em inglês
selected_country = {v: k for k, v in country_translation.items()}[selected_country_pt] # type: ignore

# Filtrar o dataframe com base no país selecionado
df_filtered = df[df['country'] == selected_country]

# Seleção de Ano
years = sorted(df_filtered['year'].dropna().unique())
selected_year = st.selectbox('Selecione o Ano', years)

# Seleção de Variedades
varieties = df_filtered['variety'].unique()
selected_varieties = st.multiselect('Selecione as Variedades', varieties, default=['Chardonnay', 'Pinot Noir'])

# Filtrar o dataframe com base no ano e nas variedades selecionadas
filtered_df = df_filtered[(df_filtered['year'] == selected_year) & (df_filtered['variety'].isin(selected_varieties))]

# Criar o box plot
fig = px.box(filtered_df, x='variety', y='price', color='variety', 
             title=f'Comparação de Preços para {selected_year} no {selected_country_pt}',
             labels={'price': 'Preço', 'variety': 'Variedade'})

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)