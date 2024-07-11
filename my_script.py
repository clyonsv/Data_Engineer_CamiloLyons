import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Configuración de las credenciales de Redshift
REDSHIFT_USER = 'camilo_lyv_coderhouse'
REDSHIFT_PASSWORD = 'cC03egF87w'
REDSHIFT_ENDPOINT = 'redshift'
REDSHIFT_DB = 'data-engineer-database'
REDSHIFT_PORT = 5432

def get_redshift_engine():
    """Establece la conexión a Redshift y retorna el engine."""
    try:
        engine = create_engine(f'redshift+psycopg2://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_ENDPOINT}:{REDSHIFT_PORT}/{REDSHIFT_DB}')
        print("Conexión a Redshift establecida correctamente.")
        return engine
    except Exception as e:
        print("Error al establecer la conexión a Redshift:", str(e))
        return None

def extract_data_from_api(url):
    """Extrae datos de la API y retorna el JSON."""
    try:
        response = requests.get(url)
        data = response.json()
        print("Datos extraídos de la API correctamente.")
        return data
    except Exception as e:
        print("Error al extraer datos de la API:", str(e))
        return None

def transform_data_to_dataframe(data):
    """Transforma los datos extraídos a un DataFrame de pandas."""
    try:
        df = pd.json_normalize(data)
        print("Datos convertidos a DataFrame correctamente.")
        return df
    except Exception as e:
        print("Error al convertir datos a DataFrame:", str(e))
        return None

def clean_data(df):
    """Limpia los datos del DataFrame."""
    # Eliminar la columna 'description'
    df = df.drop(columns=['description'])

    # Verificar nulos y celdas vacías
    print("Verificación de valores nulos:")
    print(df.isnull().sum())

    print("Verificación de celdas vacías:")
    print((df == '').sum())

    # Rellenar o eliminar valores nulos
    df = df.fillna('N/A')

    # Eliminar filas completamente vacías (si las hay)
    df = df.dropna(how='all')

    # Verificar duplicados
    print("Verificación de valores duplicados:")
    print(df.duplicated().sum())

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Información final del DataFrame
    print("Información del DataFrame después de la limpieza:")
    print(df.info())
    print(df.head())

    return df

def load_data_to_redshift(df, engine):
    """Carga los datos en Redshift."""
    try:
        df.to_sql('departamentos', engine, if_exists='replace', index=False)
        print("Datos cargados en la tabla 'departamentos' de Redshift correctamente.")
    except Exception as e:
        print("Error al cargar datos en Redshift:", str(e))

def verify_data_in_redshift(engine):
    """Verifica los datos en la tabla en Redshift a través de una consulta SQL."""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT * FROM departamentos LIMIT 5")
            print("Primeros 5 registros en la tabla 'departamentos' de Redshift:")
            for row in result:
                print(row)
    except Exception as e:
        print("Error al verificar los datos en Redshift:", str(e))

def main():
    engine = get_redshift_engine()
    if not engine:
        return

    url = "https://api-colombia.com/api/v1/Department"
    data = extract_data_from_api(url)
    if not data:
        return

    df = transform_data_to_dataframe(data)
    if df is None:
        return

    df = clean_data(df)

    load_data_to_redshift(df, engine)

    verify_data_in_redshift(engine)

if __name__ == "__main__":
    main()
