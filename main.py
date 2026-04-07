from scraper import scrape_behobia_year
from cargador_transformador import cargar_datos, limpiar_datos, decorar_datos

AÑOS = [2025, 2024, 2023, 2022, 2021]

for year in AÑOS:
    df = scrape_behobia_year(year)
    if not df.empty:
        df.to_csv(f"behobia_{year}_final.csv", index=False, encoding="utf-8-sig")

df = cargar_datos()
df_limpio = decorar_datos(limpiar_datos(df))
df_limpio.to_csv("behobia_maestro.csv", index=False, encoding="utf-8-sig")
print(f"Pipeline completado: {len(df_limpio)} registros en behobia_maestro.csv")