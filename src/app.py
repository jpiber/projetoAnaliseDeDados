import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import json
from urllib.request import urlopen

# Configurando a página
st.set_page_config(
    page_title="COVID-19 Brasil - Análise e Educação",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            color: #2c3e50;
            margin-top: 2rem;
        }
        .info-box {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>COVID-19 no Brasil: Análise e Conscientização</h1>", unsafe_allow_html=True)

# Barra lateral com informações educativas
with st.sidebar:
    st.header("Sobre a COVID-19")
    st.info("""
    A COVID-19 é uma doença causada pelo coronavírus SARS-CoV-2.
    
    **Principais sintomas:**
    - Febre
    - Tosse
    - Fadiga
    - Perda de olfato/paladar
    - Dor de garganta
    - Dificuldade para respirar
    
    **Prevenção:**
    - Use máscara em locais fechados
    - Lave as mãos frequentemente
    - Mantenha distanciamento social
    - Mantenha ambientes ventilados
    - Tome todas as doses da vacina
    - Evite aglomerações
    """)
    
    st.header("Fontes de Dados")
    st.markdown("""
    - [Ministério da Saúde](https://www.gov.br/saude/pt-br)
    - [Secretarias Estaduais de Saúde](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/s/ses)
    - [Brasil.io](https://brasil.io/covid19/)
    - [CONASS](https://www.conass.org.br/painelconasscovid19/)
    """)
    
    st.header("Links Úteis")
    st.markdown("""
    - [Plataforma IntegraSUS](https://integrasus.saude.ce.gov.br/)
    - [Coronavírus Brasil](https://covid.saude.gov.br/)
    - [Disque Saúde 136](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/disque-saude-136)
    """)

# Função para carregar os dados com tratamento de erro
@st.cache_data
def carregar_dados():
    try:
        # Obtendo o caminho absoluto do diretório atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Subindo um nível para chegar na raiz do projeto
        root_dir = os.path.dirname(current_dir)
        # Caminho para o diretório de dados
        data_dir = os.path.join(root_dir, 'data')
        
        # Carregando os dados
        df_brasil = pd.read_csv(os.path.join(data_dir, 'covid_brasil.csv'))
        df_estados = pd.read_csv(os.path.join(data_dir, 'covid_estados.csv'))
        
        # Convertendo datas
        df_brasil['date'] = pd.to_datetime(df_brasil['date'])
        df_estados['date'] = pd.to_datetime(df_estados['date'])
        
        return df_brasil, df_estados
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None, None

# Carregando os dados
df_brasil, df_estados = carregar_dados()

if df_brasil is None or df_estados is None:
    st.error("Não foi possível carregar os dados. Por favor, verifique se os arquivos de dados existem.")
    st.stop()

# Seção 1: Visão Geral
st.markdown("<h2 class='section-header'>Visão Geral da Pandemia</h2>", unsafe_allow_html=True)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_casos = df_brasil['confirmed'].iloc[-1]
    st.metric("Total de Casos", f"{total_casos:,.0f}")

with col2:
    total_obitos = df_brasil['deaths'].iloc[-1]
    st.metric("Total de Óbitos", f"{total_obitos:,.0f}")

with col3:
    letalidade = (total_obitos / total_casos) * 100
    st.metric("Taxa de Letalidade", f"{letalidade:.2f}%")

with col4:
    casos_por_100k = (total_casos / 214300000) * 100000  # População aproximada do Brasil
    st.metric("Casos por 100 mil hab.", f"{casos_por_100k:.2f}")

# Seção 2: Evolução Temporal
st.markdown("<h2 class='section-header'>Evolução Temporal</h2>", unsafe_allow_html=True)

# Seletor de período
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data Inicial", df_brasil['date'].min())
with col2:
    end_date = st.date_input("Data Final", df_brasil['date'].max())

# Filtrando dados pelo período selecionado
mask = (df_brasil['date'].dt.date >= start_date) & (df_brasil['date'].dt.date <= end_date)
df_filtered = df_brasil.loc[mask]

# Gráfico de evolução
fig_evolucao = go.Figure()

fig_evolucao.add_trace(go.Scatter(
    x=df_filtered['date'],
    y=df_filtered['confirmed'],
    name='Casos',
    line=dict(color='blue', width=2)
))

fig_evolucao.add_trace(go.Scatter(
    x=df_filtered['date'],
    y=df_filtered['deaths'],
    name='Óbitos',
    line=dict(color='red', width=2)
))

fig_evolucao.update_layout(
    title='Evolução de Casos e Óbitos',
    xaxis_title='Data',
    yaxis_title='Número',
    hovermode='x unified'
)

st.plotly_chart(fig_evolucao, use_container_width=True)

# Seção 3: Análise Regional
st.markdown("<h2 class='section-header'>Análise Regional</h2>", unsafe_allow_html=True)

# Preparando os dados
ultima_data = df_estados['date'].max()
dados_recentes = df_estados[df_estados['date'] == ultima_data].sort_values('confirmed', ascending=True)

# Criando o gráfico de barras horizontal
fig = go.Figure()

fig.add_trace(go.Bar(
    y=dados_recentes['state'],
    x=dados_recentes['confirmed'],
    orientation='h',
    text=dados_recentes['confirmed'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    hovertemplate="<b>%{y}</b><br>" +
                  "Casos: %{x:,.0f}<br>" +
                  "<extra></extra>",
    marker=dict(
        color=dados_recentes['confirmed'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title="Número de Casos",
            tickformat=",d"
        )
    )
))

fig.update_layout(
    title='Distribuição de Casos por Estado',
    xaxis_title='Número de Casos',
    yaxis_title='Estado',
    height=800,
    margin=dict(l=0, r=100, t=30, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    showlegend=False
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

st.plotly_chart(fig, use_container_width=True)

# Adicionando uma tabela com os dados
st.markdown("<h3 class='section-header'>Detalhamento por Estado</h3>", unsafe_allow_html=True)

# Preparando os dados para a tabela
tabela_dados = dados_recentes[['state', 'confirmed', 'deaths']].copy()
tabela_dados['letalidade'] = (tabela_dados['deaths'] / tabela_dados['confirmed'] * 100).round(2)
tabela_dados = tabela_dados.sort_values('confirmed', ascending=False)

# Renomeando as colunas
tabela_dados.columns = ['Estado', 'Casos Confirmados', 'Óbitos', 'Taxa de Letalidade (%)']

# Formatando os números
tabela_dados['Casos Confirmados'] = tabela_dados['Casos Confirmados'].apply(lambda x: f'{x:,.0f}')
tabela_dados['Óbitos'] = tabela_dados['Óbitos'].apply(lambda x: f'{x:,.0f}')
tabela_dados['Taxa de Letalidade (%)'] = tabela_dados['Taxa de Letalidade (%)'].apply(lambda x: f'{x:.2f}%')

st.dataframe(tabela_dados, use_container_width=True)

# Seção 4: Comparativo entre Estados
st.markdown("<h2 class='section-header'>Comparativo entre Estados</h2>", unsafe_allow_html=True)

# Seletor de métrica
metrica = st.selectbox(
    "Selecione a métrica para comparação:",
    ["Casos Confirmados", "Óbitos", "Taxa de Letalidade"]
)

if metrica == "Taxa de Letalidade":
    dados_recentes['letalidade'] = (dados_recentes['deaths'] / dados_recentes['confirmed']) * 100
    y_col = 'letalidade'
    titulo = 'Taxa de Letalidade por Estado (%)'
elif metrica == "Óbitos":
    y_col = 'deaths'
    titulo = 'Óbitos por Estado'
else:
    y_col = 'confirmed'
    titulo = 'Casos Confirmados por Estado'

fig_estados = px.bar(
    dados_recentes,
    x='state',
    y=y_col,
    title=titulo,
    labels={'state': 'Estado', y_col: metrica},
    color=y_col,
    color_continuous_scale='Viridis'
)

st.plotly_chart(fig_estados, use_container_width=True)

# Seção 5: Informações Importantes
st.markdown("<h2 class='section-header'>Informações Importantes</h2>", unsafe_allow_html=True)

with st.expander("Como se Prevenir"):
    st.markdown("""
    ### Medidas de Prevenção
    1. **Use máscara** em locais fechados ou com aglomeração
    2. **Higienize as mãos** frequentemente com água e sabão ou álcool em gel
    3. **Mantenha o distanciamento social** de pelo menos 1 metro
    4. **Evite tocar** olhos, nariz e boca sem higienizar as mãos
    5. **Cubra nariz e boca** ao tossir ou espirrar
    6. **Mantenha os ambientes ventilados**
    7. **Não compartilhe objetos** de uso pessoal
    8. **Evite aglomerações**
    9. **Fique em casa** se estiver com sintomas
    10. **Mantenha a vacinação em dia**
    """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desenvolvido para fins educacionais e de conscientização</p>
    <p>Dados atualizados em: {}</p>
    <p>Fonte: Ministério da Saúde e Secretarias Estaduais de Saúde</p>
    <p>Para mais informações, acesse: <a href="https://covid.saude.gov.br/" target="_blank">covid.saude.gov.br</a></p>
</div>
""".format(df_brasil['date'].max().strftime('%d/%m/%Y')), unsafe_allow_html=True) 