import requests
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta
import time

def download_covid_data():
    """
    Baixa os dados da COVID-19 do Brasil usando a API do OpenDataSUS
    """
    # Criando diretório de dados se não existir
    data_dir = Path('../../data')
    data_dir.mkdir(exist_ok=True)
    
    # Gerando datas para os últimos 30 dias
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        print("Baixando dados da COVID-19...")
        
        # URL da API do OpenDataSUS
        url = f"https://opendatasus.saude.gov.br/api/3/action/datastore_search"
        params = {
            'resource_id': '9bf20f69-f614-40e7-b285-9576f63b5904',
            'limit': 1000
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'result' in data and 'records' in data['result']:
            # Convertendo para DataFrame
            df = pd.DataFrame(data['result']['records'])
            
            # Limpando e formatando dados
            df['data'] = pd.to_datetime(df['data'])
            df = df.rename(columns={
                'data': 'date',
                'estado': 'state',
                'casosAcumulado': 'confirmed',
                'obitosAcumulado': 'deaths'
            })
            
            # Criando dados agregados do Brasil
            df_brasil = df.groupby('date').agg({
                'confirmed': 'sum',
                'deaths': 'sum'
            }).reset_index()
            
            # Dados por estado
            df_estados = df.copy()
            
            # Salvando dados
            df_brasil.to_csv(data_dir / 'covid_brasil.csv', index=False)
            df_estados.to_csv(data_dir / 'covid_estados.csv', index=False)
            
            print("Dados baixados e salvos com sucesso!")
            print(f"Total de registros: {len(df)}")
            print(f"Período: de {df['date'].min()} até {df['date'].max()}")
            
            return df_brasil, df_estados
        else:
            print("Erro: Estrutura de dados inesperada na resposta da API")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar dados: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

if __name__ == '__main__':
    # Tentar até 3 vezes em caso de erro
    for attempt in range(3):
        result = download_covid_data()
        if result is not None:
            break
        print(f"Tentativa {attempt + 1} falhou. Aguardando 5 segundos...")
        time.sleep(5) 