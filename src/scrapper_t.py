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
            driver.execute_script("localStorage.setItem('Location', JSON.stringify(arguments[0]));", 
                                  {"description": "Montevideo y Ciudad de la Costa",
                                   "postalCode": "11800",
                                   "geoCoordinates": [-56.1672997, -34.8944046],
                                   "sellerId": "tatauymontevideo"})

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="product-link"]'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.find_all('a', class_='link-module--fs-link--5aae5', attrs={
                'data-testid': 'product-link',
                'data-store-link': 'true'
            })

            if not items:
                print("No se encontraron más productos en la página {page}.")

            for item in items:
                url_producto = item['href']
                if not url_producto.startswith('http'):
                    url_producto = 'https://www.tata.com.uy' + url_producto
                urls_productos.append(url_producto)

        except Exception as e:
            print(f"Error al acceder a la página {page}: {e}")

    driver.quit()
    return urls_productos

def scrape_producto(url_producto, driver):
    
    print(f"Scraping el producto: {url_producto}")
    driver.get(url_producto)

    try:
        driver.execute_script("localStorage.setItem('Location', JSON.stringify(arguments[0]));", 
                              {"description": "Montevideo y Ciudad de la Costa",
                               "postalCode": "11800",
                               "geoCoordinates": [-56.1672997, -34.8944046],
                               "sellerId": "tatauymontevideo"})
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="price-module--fs-price--9b997 text__lead"]'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        nombre = soup.find('h1').text.strip()
        precio = soup.find('span', class_='price-module--fs-price--9b997 text__lead').text.strip()
        precio = float(precio.replace('$', '').replace(',', '')) / 10
        marca = soup.find('h2').text.strip()
        
        producto = {
            'nombre': nombre,
            'precio': precio,
            'marca': marca
        }
    except Exception as e:
        print(f"Error al scrapeando el producto: {e}")
        producto = None
    
    return producto

def guardar_datos(productos, filepath_base):
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    filepath = f"{filepath_base}_t_{fecha_actual}.csv"  
    
    df = pd.DataFrame(productos)
    df['fecha'] = fecha_actual  
    df.to_csv(filepath, mode='a', header=False, index=False)

if __name__ == "__main__":
    categorias = [
        'https://www.tata.com.uy/almacen',
        'https://www.tata.com.uy/frescos',
        'https://www.tata.com.uy/congelados',
        'https://www.tata.com.uy/bebidas',
        'https://www.tata.com.uy/limpieza',
        'https://www.tata.com.uy/perfumeria',
        'https://www.tata.com.uy/mascotas',
        'https://www.tata.com.uy/bebes',
        'https://www.tata.com.uy/hogar-y-bazar',
        'https://www.tata.com.uy/textil',
        'https://www.tata.com.uy/electro',
        'https://www.tata.com.uy/ferreteria',
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

