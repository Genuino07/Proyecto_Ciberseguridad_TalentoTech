import pandas as pd
import sqlite3
import os

def crear_base_de_datos():
    # 1. Cargar los datos
    # Asegúrate de que el nombre del archivo coincida con el que subiste
    csv_path = 'data/Global_Cybersecurity_Threats_2015-2024.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: No se encontró el archivo en {csv_path}")
        return

    df = pd.read_csv(csv_path)

    # 2. Limpieza básica de nombres de columnas para SQL
    # "Financial Loss (in Million $)" -> "financial_loss_millions"
    df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('$', '').replace('__', '_').lower() for c in df.columns]
    
    # 3. Conectar a SQLite (se creará el archivo automáticamente)
    conn = sqlite3.connect('data/ciberseguridad.db')
    
    # 4. Guardar los datos en una tabla llamada 'amenazas'
    df.to_sql('amenazas', conn, if_exists='replace', index=False)
    
    print("✅ ¡Éxito! Base de datos 'ciberseguridad.db' creada en la carpeta data/")
    conn.close()

if __name__ == "__main__":
    crear_base_de_datos()