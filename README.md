# SupermarketInflationTracker
SupermarketInflationTracker es un proyecto que realiza scraping de precios de productos en supermercados Uruguayos en línea y calcula la inflación basada en los datos obtenidos. Este proyecto automatiza el proceso de recopilación de datos de precios, almacenamiento histórico y cálculo de la inflación, proporcionando una herramienta útil para el monitoreo económico.

## Características

- **Scraping de precios**: Obtiene los precios actuales de los productos desde varios sitios web de supermercados.
- **Almacenamiento de datos**: Guarda los datos de precios en archivos CSV para análisis histórico.
- **Cálculo de inflación**: Calcula la inflación comparando los precios actuales con los precios anteriores.
- **Automatización**: Scripts automatizados para actualizar y analizar los datos periódicamente.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/InflationScraper.git
    cd InflationScraper
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta el script `scrape.py` para obtener los precios actuales:
    ```bash
    python scripts/scrape.py
    ```

2. Ejecuta el script `calculate_inflation.py` para calcular la inflación:
    ```bash
    python scripts/calculate_inflation.py
    ```

3. Ejecuta el script `update_data.py` para actualizar los datos históricos:
    ```bash
    python scripts/update_data.py
    ```
