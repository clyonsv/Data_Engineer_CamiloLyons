#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Configuración de las credenciales de Redshift
redshift_user = 'camilo_lyv_coderhouse'
redshift_password = 'cC03egF87w'
redshift_endpoint = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
redshift_db = 'data-engineer-database'
redshift_port = 5439

# Verificación de las credenciales de Redshift
try:
    engine = create_engine(f'redshift+psycopg2://{redshift_user}:{redshift_password}@{redshift_endpoint}:{redshift_port}/{redshift_db}')
    print("Conexión a Redshift establecida correctamente.")
except Exception as e:
    print("Error al establecer la conexión a Redshift:", str(e))

# Extraer datos de la API
url = "https://api-colombia.com/api/v1/Department"
try:
    response = requests.get(url)
    data = response.json()
    print("Datos extraídos de la API correctamente.")
except Exception as e:
    print("Error al extraer datos de la API:", str(e))
    data = None

# Convertir a DataFrame de pandas
try:
    df = pd.json_normalize(data)
    print("Datos convertidos a DataFrame correctamente.")
except Exception as e:
    print("Error al convertir datos a DataFrame:", str(e))
    df = None

# Limpieza de datos
if df is not None:
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

    # Cargar datos en Redshift
    try:
        df.to_sql('departamentos', engine, if_exists='replace', index=False)
        print("Datos cargados en la tabla 'departamentos' de Redshift correctamente.")
    except Exception as e:
        print("Error al cargar datos en Redshift:", str(e))

# Verificar los datos en la tabla en Redshift a través de una consulta SQL
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM departamentos LIMIT 5")
        print("Primeros 5 registros en la tabla 'departamentos' de Redshift:")
        for row in result:
            print(row)
except Exception as e:
    print("Error al verificar los datos en Redshift:", str(e))


# In[ ]:




