import sqlite3
import os

import pandas as pd

DB_NAME = "BehobiaBD.db"

def conexion_bd():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error conectando a la BD: {e}")
        return None

def crear_tablas(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Localidades (
            id_localidad INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE, 
            sexo TEXT,                     
            edad_min INTEGER,
            edad_max INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Resultados (
            id_resultado INTEGER PRIMARY KEY AUTOINCREMENT,      
            año INTEGER,               
            dorsal INTEGER,
                   
            nombre TEXT,
            apellido1 TEXT,
            apellido2 TEXT,
                   
            posicion INTEGER,
            estado_resultado TEXT,    
            punto_abandono TEXT,
            tiempo_oficial_s REAL,      
            ritmo_min_km REAL,          
            parcial_5k_s REAL,
            parcial_10k_s REAL,
            parcial_15k_s REAL,
            
            id_categoria INTEGER,
            id_localidad INTEGER,
            
            FOREIGN KEY (id_localidad) REFERENCES Localidades(id_localidad),
            FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
        )
    ''')
    
    print("Tablas creadas")
    conn.commit()



def cargar_categorias(conn):
    datos_categorias = [
        ('Junior F', 'F', 16, 19), ('Junior M', 'M', 16, 19),
        ('Promesa F', 'F', 20, 22), ('Promesa M', 'M', 20, 22),
        ('Senior F', 'F', 23, 39), ('Senior M', 'M', 23, 39),
        ('Veterana', 'F', 40, 50), ('Veterano', 'M', 40, 50), 
        ('Veterana Ii', 'F', 51, 60), ('Veterano Ii', 'M', 51, 60),
        ('Veterana Iii', 'F', 61, 70), ('Veterano Iii', 'M', 61, 70),
        ('Veterana Iv', 'F', 71, 99), ('Veterano Iv', 'M', 71, 99),
        ('Invidentes F', 'F', None, None), ('Invidentes M', 'M', None, None),
        ('Discapacitados', 'X', None, None), ('Apoyo Discapacitado', 'X', None, None)
    ]

    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR IGNORE INTO Categorias (nombre, sexo, edad_min, edad_max)
        VALUES (?, ?, ?, ?)
    ''', datos_categorias)
    
    conn.commit()




def cargar_localidades(conn, localidades):
    localidades_unicas = sorted(list(set([str(loc).strip() for loc in localidades if loc and str(loc).lower() != 'nan'])))
    datos_loc = [(loc,) for loc in localidades_unicas]
    cursor = conn.cursor()
    cursor.executemany('INSERT OR IGNORE INTO Localidades (nombre) VALUES (?)', datos_loc)
    conn.commit()
    cursor.execute("SELECT nombre, id_localidad FROM Localidades")
    return {fila[0].strip(): fila[1] for fila in cursor.fetchall()}





def cargar_datos_a_bd(conn, ruta):
    limpiar_bd(conn)
    cargar_categorias(conn)
    df = pd.read_csv(ruta)
    df['Localidad'] = df['Localidad'].astype(str).str.strip()
    df['Categoria'] = df['Categoria'].astype(str).str.strip()

    df = df.where(pd.notnull(df), None) 
    
    cursor = conn.cursor()
    localidades_unicas = df['Localidad'].unique()
    localidades_dict = cargar_localidades(conn, localidades_unicas)
    
    cursor.execute("SELECT nombre, id_categoria FROM Categorias")
    categorias_dict = {fila[0]: fila[1] for fila in cursor.fetchall()}

    datos=[]
    for i, (index, fila) in enumerate(df.iterrows()):
        id_loc = localidades_dict.get(str(fila['Localidad']).strip())
        id_cat = categorias_dict.get(str(fila['Categoria']).strip())
        registro = (
            fila['Año'],             
            fila['Dorsal'],         
            fila['Nombre'],          
            fila['Apellido1'],      
            fila['Apellido2'],            

            fila['Posicion'],       
            fila['Resultado'],       
            fila['Punto_Abandono'], 
            fila['Tiempo_Oficial_s'],
            fila['Ritmo (min/km)'], 
            fila['Parcial_5K_s'],   
            fila['Parcial_10K_s'],  
            fila['Parcial_15K_s'],

            id_cat,                
            id_loc              
        )
        datos.append(registro)
        if (i + 1) % 1000 == 0:
            print(f"Procesados {i + 1} registros")

    cursor.executemany('''
    INSERT or ignore INTO Resultados (
        año, dorsal, nombre, apellido1, apellido2,  posicion, estado_resultado, 
                        punto_abandono, tiempo_oficial_s, ritmo_min_km, parcial_5k_s, parcial_10k_s, parcial_15k_s,id_categoria, id_localidad
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', datos)

    conn.commit()

    print("Datos insertados")


def limpiar_bd(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Resultados')
    cursor.execute('DELETE FROM Localidades')
    cursor.execute('DELETE FROM Categorias')
    conn.commit()
    print("Base de datos limpiada")

def inicializar():
    if os.path.exists(DB_NAME):
        print(f"Base de datos '{DB_NAME}' existente")
        print("Conectando")
    else:
        print(f"Creando  base de datos '{DB_NAME}'")

    conexion = conexion_bd()
    
    if conexion:
        
        crear_tablas(conexion)

    return conexion 

    

if __name__ == "__main__":

    conn = inicializar()
    ruta_archivo = "behobia_maestro.csv"
    if os.path.exists(ruta_archivo):
        cargar_datos_a_bd(conn, ruta_archivo)
    else:
        print("Error en la ruta")

    conn.close()