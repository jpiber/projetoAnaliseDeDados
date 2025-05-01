import pandas as pd
import requests
import os
from pathlib import Path

def download_ibge_data():
    """
    Função para baixar dados do IBGE.
    Retorna um DataFrame com os dados processados.
    """
    # URLs dos dados do IBGE (exemplos)
    urls = {
        'populacao': 'https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2021/variaveis/93?localidades=N1[all]',
        'pib': 'https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2020/variaveis/37?localidades=N1[all]'
    }
    
    # Criando diretório para dados se não existir
    data_dir = Path('../../data')
    data_dir.mkdir(exist_ok=True)
    
    # Baixando e processando dados
    dfs = {}
    for nome, url in urls.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Processando dados (ajuste conforme a estrutura real dos dados)
                df = pd.DataFrame(data)
                dfs[nome] = df
                # Salvando dados
                df.to_csv(data_dir / f'{nome}.csv', index=False)
                print(f'Dados de {nome} baixados e salvos com sucesso!')
            else:
                print(f'Erro ao baixar dados de {nome}: {response.status_code}')
        except Exception as e:
            print(f'Erro ao processar dados de {nome}: {str(e)}')
    
    return dfs

def process_data():
    """
    Função para processar os dados baixados.
    Retorna um DataFrame consolidado.
    """
    data_dir = Path('../../data')
    
    try:
        # Carregando dados salvos
        populacao = pd.read_csv(data_dir / 'populacao.csv')
        pib = pd.read_csv(data_dir / 'pib.csv')
        
        # Processando e consolidando dados
        # (Ajuste conforme a estrutura real dos dados)
        df_consolidado = pd.merge(populacao, pib, on='codigo', how='outer')
        
        # Salvando dados consolidados
        df_consolidado.to_csv(data_dir / 'dados_consolidados.csv', index=False)
        print('Dados processados e salvos com sucesso!')
        
        return df_consolidado
    
    except Exception as e:
        print(f'Erro ao processar dados: {str(e)}')
        return None

if __name__ == '__main__':
    # Baixando dados
    dfs = download_ibge_data()
    
    # Processando dados
    df_consolidado = process_data()
    
    if df_consolidado is not None:
        print('\\nPrimeiras linhas dos dados consolidados:')
        print(df_consolidado.head()) 