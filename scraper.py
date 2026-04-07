import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_behobia_year(year, sleep=1.2):
    all_results = []
    base_url = "https://clasificacion.behobia-sansebastian.com/oficial.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\nIniciando scraping Behobia {year}")
    p = 0
    

    while True:
        params = {
            "lang": "es",
            "accion": "buscar",
            "tipo": "1",
            "ano": year,
            "paginacion": p * 20,
            "siguiente": "1"
        }
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            consecutive_errors = 0
            
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            
            if not table:
                print(f"Fin de resultados en página {p+1}")
                break

            rows = table.find_all("tr")
            before = len(all_results)

            for row in rows:
                cells = row.find_all("td")
                if len(cells) > 8:
                    celda_pos = cells[1]
                    toggle = celda_pos.find("span", class_="footable-toggle")
                    if toggle:
                        toggle.decompose()
                    posicion = celda_pos.get_text(strip=True)

                    try:
                        nombre = row.find("span", class_="name").get_text(strip=True)
                        apellido = row.find("span", class_="surname").get_text(strip=True)
                    except Exception as e:
                        print(f"Error al extraer nombre o apellido en página {p+1}: {e}")
                        nombre, apellido = "Desc", "Desc"
                    tiempo_final = cells[3].get_text(strip=True)
                    parcial_5k = cells[4].get_text(strip=True)
                    parcial_10k = cells[5].get_text(strip=True)
                    parcial_15k = cells[6].get_text(strip=True)
                    dorsal = cells[7].get_text(strip=True)
                    categoria = cells[8].get_text(strip=True)
                    localidad = cells[10].get_text(strip=True) if len(cells) > 10 else "N/A"

                    all_results.append({
                        "Posicion": posicion,
                        "Dorsal": dorsal,
                        "Nombre": nombre,
                        "Apellidos": apellido,
                        "Tiempo_Oficial": tiempo_final,
                        "Parcial_5K": parcial_5k,
                        "Parcial_10K": parcial_10k,
                        "Parcial_15K": parcial_15k,
                        "Categoria": categoria,
                        "Localidad": localidad,
                        "Año": year
                    })
            if len(all_results) == before:
                print(f"Página {p+1} sin nuevos resultados.")
                break
            if (p + 1) % 50 == 0:
                pd.DataFrame(all_results).to_csv(f"behobia_{year}_incremental.csv", index=False, encoding="utf-8-sig")
                print(f"Guardado backup parcial en página {p+1}")

            print(f"Página {p+1} OK ({len(all_results)} total)")
            p += 1
            time.sleep(sleep)

        except Exception as e:
            consecutive_errors += 1
            print(f"Error en página {p+1}: {e}")
            if consecutive_errors >= 5:
                print("Demasiados errores consecutivos, deteniendo scraping.")
                break
            continue

    return pd.DataFrame(all_results)


if __name__ == "__main__":
    AÑOS = [2025, 2024, 2023, 2022, 2021]

    for year in AÑOS:
        df = scrape_behobia_year(year)
        if not df.empty:
            filename = f"behobia_{year}_final.csv"
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"\nFINALIZADO {year} → {len(df)} registros en {filename}")
            if os.path.exists(f"behobia_{year}_incremental.csv"):
                os.remove(f"behobia_{year}_incremental.csv")
        else:
            print(f"El año {year} terminó sin datos.")