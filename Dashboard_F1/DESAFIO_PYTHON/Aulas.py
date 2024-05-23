import pandas as pd
import streamlit as st
import plotly.express as px 

# Carregar os dados dos arquivos CSV
data = pd.read_csv('../DADOS_F1/driver_standings.csv', sep=',')
data_driver_standings = pd.read_csv('../DADOS_F1/driver_details.csv', sep=',')
data_constructor_standings = pd.read_csv('../DADOS_F1/constructor_standings.csv', sep=',')

# Configurar a página do Streamlit
st.set_page_config(page_title="TEMPORADAS F1")

# Obter os anos únicos disponíveis no dataset
anos = data['Year'].unique()

# Criar um seletor de temporada na barra lateral
temporada_escolhida = st.sidebar.selectbox("Temporada", anos)

# Criar um rádio botão para selecionar entre pilotos e construtoras
filtragem_PC = st.sidebar.radio('Selecione a filtragem', ("Pilotos", "Construtoras"))

# Função para filtrar os dados por ano
@st.cache_data   
def filtrar_ano(ano):
    return data.query(f'Year == {ano}')

# Filtrar os dados para o ano selecionado
tabela_ano = filtrar_ano(temporada_escolhida)

# Obter a lista de construtoras para o ano selecionado
construtoras = data_constructor_standings.query(f'Year == {temporada_escolhida}')['Team'].value_counts().index

# Criar um seletor de construtoras na barra lateral
construtora_selecionada = st.sidebar.selectbox("Construtora", construtoras)

# Função para filtrar construtoras por ano
@st.cache_data   
def filtrar_construtoras_ano(ano):
    return data_constructor_standings.query(f'Year == {ano}')

# Filtrar os dados de construtoras para o ano selecionado
construtora_ano = filtrar_construtoras_ano(temporada_escolhida)

# Obter a lista de pilotos para a construtora selecionada no ano escolhido
pilotos = tabela_ano.query(f'Car == "{construtora_selecionada}"')['Driver'].value_counts().index

# Criar um seletor de pilotos na barra lateral
piloto_selecionado = st.sidebar.selectbox("Piloto", pilotos)

# Função para filtrar piloto por ano e construtora
@st.cache_data   
def filtrar_piloto_ano_construtora(ano, construtora):
    return data_driver_standings.query(f'Year == {ano} and Car == "{construtora}"')

# Filtrar os dados do piloto para o ano e construtora selecionados
piloto_ano_construtora = filtrar_piloto_ano_construtora(temporada_escolhida, construtora_selecionada)

# Verificar e atualizar o estado da sessão para a construtora selecionada
if construtora_selecionada != st.session_state.get("selected_construtora"):
    st.session_state["selected_construtora"] = construtora_selecionada
    # Atualizar a lista de pilotos com base na nova construtora selecionada
    pilotos = tabela_ano.query(f'Car == "{construtora_selecionada}"')['Driver'].value_counts().index
    st.session_state["selected_piloto"] = pilotos[0] if len(pilotos) > 0 else None

# Criar os gráficos para a pontuação dos pilotos e construtoras na temporada
with st.container():
    if filtragem_PC == 'Construtoras':
        col1, col2 = st.columns(2)
        # Gráfico de barras da pontuação das construtoras
        fig_date = px.bar(construtora_ano, y='Team', x='PTS', title='Pontuação no campeonato', orientation="h", width=500, height=550)
        col2.plotly_chart(fig_date)
    elif filtragem_PC == 'Pilotos':
        col1, col2 = st.columns(2)
        # Gráfico de barras da pontuação dos pilotos
        fig_date = px.bar(tabela_ano, y='Driver', x='PTS', title='Pontuação no campeonato', orientation="h", width=500, height=550)
        col2.plotly_chart(fig_date)

# Criar um gráfico com a pontuação dos pilotos por corrida
with st.container():
    col1, col2 = st.columns(2)
    # Gráfico de linha com os pontos dos pilotos em cada corrida
    fig = px.line(piloto_ano_construtora, x="Grand Prix", y="PTS", title='Pontos do piloto', width=550, height=450)
    col1.plotly_chart(fig)
