import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def criar_visualizacoes():
    print("=== Análise de Dados COVID-19 ===")
    print("\nCarregando dados...")
    
    # Configurando diretórios
    data_dir = Path('data')
    reports_dir = Path('reports/figures')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Carregando dados
    df_brasil = pd.read_csv(data_dir / 'covid_brasil.csv')
    df_estados = pd.read_csv(data_dir / 'covid_estados.csv')
    
    # Convertendo datas
    df_brasil['date'] = pd.to_datetime(df_brasil['date'])
    df_estados['date'] = pd.to_datetime(df_estados['date'])
    
    print("Dados carregados com sucesso!")
    print(f"Período analisado: {df_brasil['date'].min().date()} até {df_brasil['date'].max().date()}")
    
    print("\nGerando gráficos...")
    
    # 1. Evolução temporal
    print("\n1. Criando gráfico de evolução temporal...")
    plt.figure(figsize=(15, 8))
    plt.plot(df_brasil['date'], df_brasil['confirmed'], label='Casos', color='blue')
    plt.plot(df_brasil['date'], df_brasil['deaths'], label='Óbitos', color='red')
    plt.title('Evolução da COVID-19 no Brasil', fontsize=14)
    plt.xlabel('Data')
    plt.ylabel('Número')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(reports_dir / 'evolucao_covid.png')
    plt.close()
    
    # 2. Casos por estado
    print("2. Criando gráfico de casos por estado...")
    ultima_data = df_estados['date'].max()
    dados_recentes = df_estados[df_estados['date'] == ultima_data]
    
    plt.figure(figsize=(15, 8))
    sns.barplot(data=dados_recentes, x='state', y='confirmed', color='skyblue')
    plt.title('Casos de COVID-19 por Estado', fontsize=14)
    plt.xlabel('Estado')
    plt.ylabel('Número de Casos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(reports_dir / 'casos_por_estado.png')
    plt.close()
    
    print("\nVisualizações criadas com sucesso!")
    print("\nVocê pode encontrar os gráficos em:")
    print(f"1. Evolução temporal: {reports_dir / 'evolucao_covid.png'}")
    print(f"2. Casos por estado: {reports_dir / 'casos_por_estado.png'}")

if __name__ == '__main__':
    criar_visualizacoes() 