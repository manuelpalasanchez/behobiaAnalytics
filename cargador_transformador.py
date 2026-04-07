import pandas as pd
import os
import re

def hms_a_segundos(t_str):
    try:
        if pd.isna(t_str) or t_str == "" or t_str == "-" or t_str == "*":
            return None
        
        parts = list(map(int, re.findall(r'\d+', str(t_str))))
        if len(parts) == 3: return parts[0] * 3600 + parts[1] * 60 + parts[2]
        if len(parts) == 2: return parts[0] * 60 + parts[1]
        return None
    except:
        return None


def cargar_datos():
    ruta = "." 
    archivos = os.listdir(ruta)
    lista_dfs = []
    for archivo in archivos:
        if archivo.startswith("behobia_") and archivo.endswith("_final.csv"):
            temp_df = pd.read_csv(archivo)
            print(f"Cargado {archivo} con {len(temp_df)} registros.")
            lista_dfs.append(temp_df)

    df = pd.concat(lista_dfs, ignore_index=True)
    print(f"Total registros cargados: {len(df)}")
    return df

def limpiar_datos(df):
    df_copy= df.copy()
    df_copy['Posicion'] = pd.to_numeric(df_copy['Posicion'], errors='coerce').astype('Int64')
    df_copy['Nombre'] = df_copy['Nombre'].str.strip().str.title()
    apellidos = df_copy['Apellidos'].str.split()
    df_copy['Apellido1'] = apellidos.str[0].str.title()
    df_copy['Apellido2'] = apellidos.str[1:].str.join(' ').str.title()
    df_copy['Localidad'] = df_copy['Localidad'].str.strip().str.title()
    df_copy['Categoria'] = df_copy['Categoria'].str.strip().str.title()
    df_copy['Año'] = df_copy['Año'].astype('Int64')
    df_copy['Dorsal'] = df_copy['Dorsal'].astype('Int64')
    df_copy.drop(columns=['Apellidos'], inplace=True)

    columnas_tiempo = ['Tiempo_Oficial', 'Parcial_5K', 'Parcial_10K', 'Parcial_15K']
    for col in columnas_tiempo:
        df_copy[f'{col}_s'] = df_copy[col].apply(hms_a_segundos)

    return df_copy

    

def get_resultado(t_str, t_seg):
    if pd.isna(t_seg):
        if t_str == "*":
            return "Desc" 
        return "DNF"
    return "F"

def get_ritmo_min_km(t_seg):
    if pd.isna(t_seg) or t_seg == 0:
        return None
    return round((t_seg / 20) / 60, 2) # segundos / 20 km a minutos por km



def get_abandono(fila):
    if fila['Resultado'] != 'DNF':
        return ""
    if pd.isna(fila['Parcial_5K_s']):
        return "0-5"
    elif pd.isna(fila['Parcial_10K_s']):
        return "5-10"
    elif pd.isna(fila['Parcial_15K_s']):
        return "10-15"
    else:
        return "15-20"


def ordenar_columnas(df):
    df_copy = df.copy()
    columnas_ordenadas = [
        'ID', 'Año', 'Posicion', 'Dorsal', 
        'Nombre', 'Apellido1', 'Apellido2', 
         'Categoria', 'Localidad',
        'Resultado', 'Punto_Abandono',
        'Tiempo_Oficial_s', 'Ritmo (min/km)',
        'Parcial_5K_s', 'Parcial_10K_s', 'Parcial_15K_s']
    df_final = df_copy[columnas_ordenadas]
    return df_final


def decorar_datos(df):
    df_copy = df.copy()

    df_copy['Resultado'] = df_copy.apply(lambda fila: get_resultado(fila['Tiempo_Oficial'], fila['Tiempo_Oficial_s']), axis=1)
    df_copy['Ritmo (min/km)'] = df_copy['Tiempo_Oficial_s'].apply(get_ritmo_min_km)
    df_copy['ID'] = (df_copy['Año'].astype(str) + "_" + df_copy['Dorsal'].astype(str).str.zfill(5))


    df_copy['Punto_Abandono'] = ""
    mascara_dnf = df_copy['Resultado'] == 'DNF'
    df_copy.loc[mascara_dnf, 'Punto_Abandono'] = df_copy[mascara_dnf].apply(get_abandono, axis=1)

    columnas_tiempo = ['Tiempo_Oficial', 'Parcial_5K', 'Parcial_10K', 'Parcial_15K']
    df_copy.drop(columns=columnas_tiempo, inplace=True)

    df_copy = ordenar_columnas(df_copy)
    
    
    return df_copy




if __name__ == "__main__":
    df = cargar_datos()

    df_limpio = limpiar_datos(df)
    df_limpio_decorado = decorar_datos(df_limpio)

    print(sorted(df_limpio_decorado['Categoria'].unique()))

    df_limpio_decorado.to_csv("behobia_maestro.csv", index=False, encoding='utf-8-sig')

