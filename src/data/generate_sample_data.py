import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """
    Gera dados de exemplo da COVID-19 para demonstração.
    """
    # Obtendo o caminho absoluto do diretório do projeto
    PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    DATA_DIR = PROJECT_DIR / 'data'
    
    print(f"Criando diretório de dados em: {DATA_DIR}")
    
    # Criando diretório de dados se não existir
    DATA_DIR.mkdir(exist_ok=True)
    
    # Gerando datas para os últimos 30 dias
    end_date = datetime.now()
    dates = [end_date - timedelta(days=x) for x in range(30)]
    dates.reverse()
    
    # Estados brasileiros
    estados = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    print("Gerando dados de exemplo...")
    
    # Gerando dados para cada estado
    data = []
    for date in dates:
        for estado in estados:
            # Gerando números aleatórios realistas
            casos = np.random.randint(1000, 100000)
            obitos = int(casos * np.random.uniform(0.01, 0.05))
            
            data.append({
                'date': date,
                'state': estado,
                'confirmed': casos,
                'deaths': obitos
            })
    
    # Criando DataFrame
    df = pd.DataFrame(data)
    
    # Criando dados agregados do Brasil
    df_brasil = df.groupby('date').agg({
        'confirmed': 'sum',
        'deaths': 'sum'
    }).reset_index()
    
    # Salvando dados
    brasil_file = DATA_DIR / 'covid_brasil.csv'
    estados_file = DATA_DIR / 'covid_estados.csv'
    
    df_brasil.to_csv(brasil_file, index=False)
    df.to_csv(estados_file, index=False)
    
    print("\nDados salvos em:")
    print(f"- Dados do Brasil: {brasil_file}")
    print(f"- Dados dos Estados: {estados_file}")
    
    print("\nEstatísticas:")
    print(f"Total de registros: {len(df)}")
    print(f"Período: de {df['date'].min()} até {df['date'].max()}")
    
    return df_brasil, df

if __name__ == '__main__':
    generate_sample_data() 