# Behobia – San Sebastián Analytics

> Pipeline end-to-end de scraping, ETL y visualización interactiva sobre los resultados de una de las carreras populares más importantes del norte de España.

**[Ver app en Streamlit Cloud]()** 

![Captura](demo.gif)

---

## El problema

La organización de la Behobia–San Sebastián acumula años de datos de clasificación públicamente accesibles pero sin explotar analíticamente. Con más de **123.000 registros entre 2021 y 2025**, existe información valiosa sobre logística del evento, perfil demográfico de los participantes e inteligencia deportiva que, a priorir, no estaba siendo utilizada.

El objetivo fue construir un sistema que extrajera, transformara y visualizara esos datos para responder tres preguntas concretas:

- **Operativa:** ¿dónde se concentran los abandonos y las llegadas a meta?
- **Mercado:** ¿cómo ha evolucionado la participación y qué nichos geográficos y demográficos existen?
- **Deportiva:** ¿cuál es el perfil de rendimiento del corredor popular y dónde decae?

En función de las respuestas a estas preguntas base, se generan diversos insights que pueden ser utilizados como aporte de valor para la toma de nuevas decisiones, impactando en mejoras logísticas o económicas para la organización de la prueba. 

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Extracción | Python - Requests - BeautifulSoup |
| Transformación | Pandas - Regex |
| Almacenamiento | CSV (maestro) - SQLite (exploración) |
| Visualización | Plotly - Streamlit |
| Despliegue | Streamlit Cloud |

---

## Arquitectura del pipeline

```
1º. Web oficial Behobia

2º. scraper.py (behobia_{año}_final.csv  (x5 años))

3º. cargador_transformador.py
- Concatenación de CSVs anuales
- Normalización de texto (nombres, localidades, categorías)
- Parsing de tiempos HH:MM:SS -> segundos
- Generación de métricas derivadas (ritmo, resultado, punto de abandono)

4º. behobia_maestro.csv (~123k registros limpios)

5º. app.py + graficos_*.py
- Carga en memoria con @st.cache_data
- 8 visualizaciones interactivas en Plotly
- Filtro por edición (2021–2025)
```

---

## Estructura del repositorio

```
behobia-analytics/
- app.py                      # Orquestador 
- utils.py                    # Layout, componentes
- graficos_operativo.py       # Bloque 1: abandonos y afluencia en meta
- graficos_mercado.py         # Bloque 2: género, fidelización, localidades, inclusión
- graficos_deportivo.py       # Bloque 3: el muro y segmentación por ritmo
- scraper.py                  # Scraping paginado de la web oficial
- cargador_transformador.py   # ETL: limpieza, transformación y enriquecimiento
- gestor_bd.py                # Modelado relacional en SQLite (ver nota abajo)
- main.py                     # Script de ejecución del pipeline completo
-style.css                    # Estilos de la app
- behobia_maestro.csv         # Dataset final procesado
- requirements.txt
```

---

## Cómo ejecutar en local

**1. Clonar el repositorio**
```bash
git clone https://github.com/manuelpalasanchez/behobia-analytics.git
cd behobia-analytics
```

**2. Crear entorno virtual e instalar dependencias**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**3. Lanzar la app**
```bash
streamlit run app.py
```

> El dataset `behobia_maestro.csv` ya está incluido en el repositorio. No es necesario ejecutar el pipeline de scraping para usar la app.

**Opcional para regenerar el dataset desde cero**
```bash
python main.py
```
> El scraping de las 5 ediciones no es inmediato. La web implementa rate limiting, por lo que el script incluye pausas entre peticiones y guardado incremental por si ocurren interrupciones.

---

## Insights clave

**Optimización operativa**
- Los tramos 0–5 km y 10–15 km concentran el 67% de los abandonos por lo que son puntos críticos ideales para refuerzo médico o refuerzo preventivo con avituallamientos.
- El pico de llegadas a meta se produce entre los minutos 100 y 120 (hora y 40, dos horas), lo que permite dimensionar con precisión el personal de entrega de medallas y staff necesario.

**Inteligencia de mercado**
- La participación femenina creció un +71% en términos absolutos desde 2021, pasando de representar el 25,5% al 34% del total.
- Donostia-San Sebastián, Madrid y Barcelona lideran la procedencia acumulada, convirtiéndolos en núcleos prioritarios para campañas de captación.
- El 27,7% de los participantes son corredores recurrentes, con margen de mejora mediante programas de fidelización que aporten ventajas a dicho grupo.

**Inteligencia deportiva**
- El fenómeno del "Muro" (llevado a la distancia de media maratón) ocurre en todas las categorías: la pérdida de ritmo se agudiza significativamente a partir del km 15.
- La segmentación por ritmo revela mercados claramente diferenciados: Senior M y Promesa M concentran perfiles Pro/Avanzado, mientras las categorías femeninas y veteranas dominan los segmentos Popular/Recreativo. Esto se podría traducir en campañas de productosd personalizadas y dirigidas a este tipo de perfiles, o por el contrario a perfiles más casuales pero de manera coordinada. 

---

## Decisiones técnicas y evolución

**SQLite -> CSV directo**
El pipeline original cargaba el dataset procesado en una base de datos SQLite con modelo dimensional (tabla de hechos `Resultados` + dimensiones `Localidades` y `Categorias`). Para el despliegue de la app, se optó por utilizar directamente el CSV maestro: los datos son estáticos, no requieren actualizaciones, y eliminar la capa de BD reduce dependencias y simplifica el despliegue en Streamlit Cloud sin coste de infraestructura. El código de `gestor_bd.py` se mantiene en el repositorio como documentación del modelado relacional realizado.

**Matplotlib -> Plotly**
Los gráficos originales del análisis se generaban en Matplotlib como imágenes estáticas para el informe. La migración a Plotly permite interactividad nativa (hover, zoom, filtrado) sin coste adicional de desarrollo, y se integra directamente con Streamlit.

**Monolito -> módulos**
La primera versión de la app concentraba toda la lógica en un único archivo. La refactorización en módulos por bloque temático (`graficos_operativo`, `graficos_mercado`, `graficos_deportivo`) y recursos de apoyo compartidos (`utils`) facilita el mantenimiento y la extensión del proyecto.

---

## Autor

**Manuel Palacios Sánchez**
[github.com/manuelpalasanchez](https://github.com/manuelpalasanchez) · [LinkedIn](www.linkedin.com/in/manuelpalasanchez) 