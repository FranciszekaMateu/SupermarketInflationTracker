from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def obtener_urls_productos(url_categoria):
    urls_productos = []
    driver = webdriver.Chrome()

    for page in range(1, 41):  
        url = f"{url_categoria}?page={page}"
        print(f"Scraping la página: {url}")
        driver.get(url)

        try:
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="vtex-product-summary-2-x-clearLink h-100 flex flex-column"]'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find_all('a', class_='vtex-product-summary-2-x-clearLink h-100 flex flex-column')

            if not items:
                print("No se encontraron más productos en la página {page}.")

            for item in items:
                url_producto = item['href']
                if not url_producto.startswith('http'):
                    url_producto = 'https://www.devoto.com.uy' + url_producto
                urls_productos.append(url_producto)

        except Exception as e:
            print(f"Error al acceder a la página {page}: {e}")

    driver.quit()
    return urls_productos

def scrape_producto(url_producto, driver):
    
    print(f"Scraping el producto: {url_producto}")
    driver.get(url_producto)

    try:
        
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="devotouy-products-components-0-x-sellingPriceWithUnitMultiplier"]'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        nombre = soup.find('span',class_='devotouy-store-components-3-x-productBrand').text.strip()
        precio = soup.find('span', class_='devotouy-products-components-0-x-sellingPriceWithUnitMultiplier').text.strip()
        precio = float(precio.replace('$', '').replace(',', ''))      
        producto = {
            'nombre': nombre,
            'precio': precio,
        }
    except Exception as e:
        print(f"Error al scrapeando el producto: {e}")
        producto = None
    
    return producto

def guardar_datos(productos, filepath_base):
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    filepath = f"{filepath_base}_dv_{fecha_actual}.csv"  
    
    df = pd.DataFrame(productos)
    df['fecha'] = fecha_actual  
    df.to_csv(filepath, mode='a', header=False, index=False)

if __name__ == "__main__":
    categorias = [
        'https://www.devoto.com.uy/puericultura',
        # 'https://www.devoto.com.uy/bebidas',
        # 'https://www.devoto.com.uy/alimentos',
        # 'https://www.devoto.com.uy/frescos',
        # 'https://www.devoto.com.uy/perfumeria-y-limpieza'
        
    ]

    todos_los_productos = []

    driver = webdriver.Chrome()

    for categoria in categorias:
        urls_productos = list(set(obtener_urls_productos(categoria)))

        for url in urls_productos:
            producto = scrape_producto(url, driver)
            if producto:
                todos_los_productos.append(producto)

    driver.quit()

    print(f"Total de productos scrapeados: {len(todos_los_productos)}")
    guardar_datos(todos_los_productos, '../data/precios_producto')  

