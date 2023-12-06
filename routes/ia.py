from fastapi import APIRouter
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import random

ia = APIRouter()

@ia.get('/ia')
def fit_model():
    df_pozos_from_csv = pd.read_csv('C:/Users/Pablo/Documents/IPF/Trabajo final integración/modelo_pozo_hidrocarburos/data/pozos_petroleo_10000.csv')

    # Preparar los datos para el modelo
    X = df_pozos_from_csv[['Profundidad', 'Presion', 'Temperatura']]  # Variables independientes
    y = df_pozos_from_csv['Produccion_Petroleo']  # Variable dependiente
    
    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Escalar características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Crear y entrenar el modelo de Random Forest con los mejores hiperparámetros
    model = RandomForestRegressor(n_estimators=150, max_depth=5, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Predicción de la producción de petróleo con los datos de un nuevo pozo
    valores_nuevo_pozo = {
        'Profundidad': [3791],
        'Presion': [5298.44],
        'Temperatura': [168.39]
    }
    
    datos_nuevo_pozo = pd.DataFrame(valores_nuevo_pozo)
    datos_nuevo_pozo_scaled = scaler.transform(datos_nuevo_pozo)
    produccion_predicha = model.predict(datos_nuevo_pozo_scaled)
    
    # Graficar la predicción del nuevo pozo
    fechas = pd.date_range(start='2023-12-01', periods=365 * 3, freq='D')
    produccion_acumulada = [0]
    for i, fecha in enumerate(fechas[:-1]):
        fluctuacion = random.uniform(-0.05, 0.05)
        nueva_produccion = max(0, produccion_acumulada[i] + produccion_predicha * (1 + fluctuacion))
        produccion_acumulada.append(nueva_produccion[0])
        
    result = {
        "fechas": fechas.strftime("%Y-%m-%d").tolist(),
        "produccion_acumulada": produccion_acumulada
    }
    
    return result
