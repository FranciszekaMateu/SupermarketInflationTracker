import pandas as pd

def calcular_inflacion(filepath, fecha_inicio, fecha_fin):
    historico = pd.read_csv(filepath, names=['nombre', 'precio', 'fecha'])
    
    precios_inicio = historico[historico['fecha'] == fecha_inicio]
    precios_fin = historico[historico['fecha'] == fecha_fin]
    
    inflacion = precios_fin.set_index('nombre')['precio'] / precios_inicio.set_index('nombre')['precio'] - 1
    
    inflacion_promedio = inflacion.mean() * 100
    return inflacion, inflacion_promedio

if __name__ == "__main__":
    fecha_inicio = '2024-01-01'
    fecha_fin = '2024-06-01'
    inflacion, inflacion_promedio = calcular_inflacion('../data/precios_productos.csv', fecha_inicio, fecha_fin)
    
    print(inflacion)
    print(f'Inflación promedio: {inflacion_promedio:.2f}%')
