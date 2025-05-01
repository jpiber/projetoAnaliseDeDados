import pandas as pd
import requests
from pathlib import Path

def baixar_dados_covid():
    print("Baixando dados reais da COVID-19...")
    
    # URL dos dados oficiais (usando o dataset do Wesley Cota)
    url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    
    try:
        # Criando diretório de dados se não existir
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        # Baixando e lendo os dados
        df = pd.read_csv(url)
        
        # Processando dados do Brasil (total)
        df_brasil = df[df['state'] == 'TOTAL'].copy()
        df_brasil = df_brasil[['date', 'totalCases', 'deaths']]
        df_brasil.columns = ['date', 'confirmed', 'deaths']
        
        # Processando dados dos estados (último dia)
        df_estados = df[df['state'] != 'TOTAL'].copy()
        df_estados = df_estados[['date', 'state', 'totalCases', 'deaths']]
        df_estados.columns = ['date', 'state', 'confirmed', 'deaths']
        
        # Salvando os dados
        df_brasil.to_csv(data_dir / 'covid_brasil.csv', index=False)
        df_estados.to_csv(data_dir / 'covid_estados.csv', index=False)
        
        print("Dados baixados com sucesso!")
        print(f"\nPeríodo dos dados: de {df_brasil['date'].min()} até {df_brasil['date'].max()}")
        print(f"Total de estados: {len(df_estados['state'].unique())}")
        
    except Exception as e:
        print(f"Erro ao baixar os dados: {e}")
        return None

if __name__ == '__main__':
    baixar_dados_covid() 