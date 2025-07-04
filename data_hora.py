import pandas as pd
import requests
import os
import argparse
from datetime import datetime
from pathlib import Path
import pytz
from dotenv import load_dotenv

load_dotenv()

# Definir argumentos de línea de comando
parser = argparse.ArgumentParser(description="Pipeline para datos de EUR/USD desde Twelve Data")
parser.add_argument(
    "--interval", 
    type=str, 
    default="15min", 
    help="Intervalo de tiempo para los datos (e.g., '1h', '15min')"
)
parser.add_argument(
    "--output", 
    type=str, 
    default="eurusd_intraday.csv", 
    help="Ruta y nombre de archivo para guardar los datos"
)
args = parser.parse_args()

API_KEY2 = os.getenv("AV_HOURLY_KEY")
symbol = "EUR/USD"
interval = args.interval
output_file = Path(args.output).resolve()

def get_twelve_data(symbol, interval):
    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=5000"
        f"&apikey={API_KEY2}"
    )
    try:
        response = requests.get(url).json()
        if 'values' in response:
            df = pd.DataFrame(response['values'])
            df['datetime'] = pd.to_datetime(df['datetime'])
            # Convertir de UTC a hora local (America/Bogota)
            df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert('America/Bogota').dt.tz_localize(None)
            df = df.sort_values('datetime')
            return df[['datetime', 'open', 'high', 'low', 'close']]
        else:
            print(f"⚠ Error en respuesta de Twelve Data:", response.get('message', 'No se encontró la clave "values".'))
            return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return pd.DataFrame()

df_nuevo = get_twelve_data(symbol, interval)

if not df_nuevo.empty:
    if output_file.exists():
        df_antiguo = pd.read_csv(output_file)
        df_antiguo['datetime'] = pd.to_datetime(df_antiguo['datetime'])
        
        df_combinado = pd.concat([df_antiguo, df_nuevo]).drop_duplicates(subset='datetime')
        df_combinado = df_combinado.sort_values('datetime')
    else:
        df_combinado = df_nuevo

    # Crear carpeta si no existe
    output_file.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().replace(second=0, microsecond=0)
    df_combinado = df_combinado[df_combinado['datetime'] <= now]
    df_combinado.to_csv(output_file, index=False)
    print(f"✅ Datos guardados: {len(df_combinado)} filas totales.")
    print(f"Archivo ubicado en: {os.path.abspath(output_file)}")
else:
    print("⚠ No se pudo obtener nuevos datos.")