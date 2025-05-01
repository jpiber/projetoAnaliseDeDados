import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Obtendo o caminho absoluto do diretório do projeto
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = PROJECT_DIR / 'data'
REPORTS_DIR = PROJECT_DIR / 'reports' / 'figures'

def plot_correlation_matrix(df, title='Matriz de Correlação'):
    """
    Cria uma matriz de correlação heatmap.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title(title)
    plt.tight_layout()
    return plt.gcf()

def plot_scatter_with_regression(df, x_col, y_col, title='Gráfico de Dispersão com Regressão'):
    """
    Cria um gráfico de dispersão com linha de regressão.
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()
    return plt.gcf()

def plot_bar_chart(df, x_col, y_col, title='Gráfico de Barras'):
    """
    Cria um gráfico de barras.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()

def plot_time_series(df, x_col, y_col, title='Série Temporal'):
    """
    Cria um gráfico de série temporal.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df[x_col], df[y_col])
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True)
    plt.tight_layout()
    return plt.gcf()

def save_plot(fig, filename):
    """
    Salva o gráfico em um arquivo.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(REPORTS_DIR / filename)
    plt.close()

def create_all_visualizations(df):
    """
    Cria e salva todas as visualizações para o DataFrame.
    """
    # Matriz de correlação
    corr_fig = plot_correlation_matrix(df)
    save_plot(corr_fig, 'correlation_matrix.png')
    
    # Gráficos de dispersão para pares de variáveis importantes
    scatter_fig = plot_scatter_with_regression(df, 'pib_per_capita', 'idh')
    save_plot(scatter_fig, 'pib_vs_idh.png')
    
    # Gráfico de barras para PIB per capita
    bar_fig = plot_bar_chart(df, 'municipio', 'pib_per_capita')
    save_plot(bar_fig, 'pib_per_capita.png')
    
    print('Visualizações criadas e salvas com sucesso!')

def plot_covid_evolution(df, title='Evolução da COVID-19 no Brasil'):
    """
    Cria um gráfico de linha mostrando a evolução dos casos e óbitos.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['confirmed'], label='Casos', marker='o')
    plt.plot(df['date'], df['deaths'], label='Óbitos', marker='o')
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Número')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()

def plot_covid_by_state(df, title='Casos de COVID-19 por Estado'):
    """
    Cria um gráfico de barras mostrando os casos por estado.
    """
    # Pegando os dados mais recentes por estado
    latest_date = df['date'].max()
    df_latest = df[df['date'] == latest_date]
    
    plt.figure(figsize=(15, 8))
    sns.barplot(data=df_latest, x='state', y='confirmed', palette='viridis')
    plt.title(title)
    plt.xlabel('Estado')
    plt.ylabel('Número de Casos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()

def plot_covid_heatmap(df, title='Mapa de Calor da COVID-19 no Brasil'):
    """
    Cria um mapa de calor dos casos por estado.
    """
    # Pegando os dados mais recentes por estado
    latest_date = df['date'].max()
    df_latest = df[df['date'] == latest_date]
    
    fig = px.choropleth_mapbox(
        df_latest,
        geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson',
        locations='state',
        featureidkey='properties.sigla',
        color='confirmed',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        zoom=3,
        center={'lat': -15.7801, 'lon': -47.9292},
        opacity=0.5,
        title=title
    )
    return fig

def create_covid_visualizations(df_brasil, df_estados):
    """
    Cria e salva todas as visualizações para os dados da COVID-19.
    """
    print(f"Salvando visualizações em: {REPORTS_DIR}")
    
    # Evolução temporal
    evolution_fig = plot_covid_evolution(df_brasil)
    save_plot(evolution_fig, 'covid_evolution.png')
    print("- Gráfico de evolução temporal salvo")
    
    # Casos por estado
    state_fig = plot_covid_by_state(df_estados)
    save_plot(state_fig, 'covid_by_state.png')
    print("- Gráfico de casos por estado salvo")
    
    # Mapa de calor
    heatmap_fig = plot_covid_heatmap(df_estados)
    heatmap_fig.write_html(str(REPORTS_DIR / 'covid_heatmap.html'))
    print("- Mapa de calor interativo salvo")
    
    print('\nVisualizações da COVID-19 criadas e salvas com sucesso!')

if __name__ == '__main__':
    print(f"Carregando dados de: {DATA_DIR}")
    
    # Carregando dados
    df_brasil = pd.read_csv(DATA_DIR / 'covid_brasil.csv')
    df_estados = pd.read_csv(DATA_DIR / 'covid_estados.csv')
    
    # Convertendo datas
    df_brasil['date'] = pd.to_datetime(df_brasil['date'])
    df_estados['date'] = pd.to_datetime(df_estados['date'])
    
    # Criando visualizações
    create_covid_visualizations(df_brasil, df_estados) 