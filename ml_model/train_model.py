import pandas as pd
import json
import joblib
from shapely.wkt import loads
from shapely.geometry import mapping
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

print("Cargando archivos CSV...")

# Rutas CSV por sector
file_paths = [
    # Sector 1
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM1.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM2.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM3.csv",
    # Sector 2
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM4.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM5.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM6.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM7.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM8.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM9.csv",
    # Sector 3
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM10.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM11.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM12.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM13.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM14.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM15.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM16.csv",
    # Sector 4
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM17.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM18.csv",
    r"C:\Users\alexp\Desktop\TFG\Tsunamis\Rutas\CM19.csv"
]

# Cargar y concatenar todas las rutas en un solo DataFrame
df_list = [pd.read_csv(file) for file in file_paths]
df = pd.concat(df_list, ignore_index=True)

# Definir variables de entrada y salida para el modelo
X = df[["start_entry_cost", "end_exit_cost", "cost_on_graph"]]
y = df["total_cost"]

# División de datos y entrenamiento del modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
modelo.fit(X_train, y_train)

# Evaluación del modelo
y_pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Guardar el modelo con sus métricas
joblib.dump((modelo, {
    "mae": mae,
    "mse": mse,
    "rmse": rmse,
    "r2": r2
}), "model.pkl")

print(f"Modelo guardado. MAE: {mae:.2f} | R2: {r2:.2f}")

# Asociar rutas óptimas por sector para el GeoJSON
geojson_data = {"type": "FeatureCollection", "features": []}

# Información de los sectores
sectores_info = {
    1: "Sector 1",
    2: "Sector 2",
    3: "Sector 3",
    4: "Sector 4"
}

# Definir los sectores y el número de rutas en cada uno
sector_rutas = {
    1: 3,
    2: 6,
    3: 7,
    4: 3
}

# Recorrer los sectores y generar una ruta óptima para cada uno
index = 0
for sector_id, cantidad in sector_rutas.items():
    rutas_sector = df_list[index:index + cantidad]
    rutas_df = pd.concat(rutas_sector, ignore_index=True)

    # Seleccionar la mejor ruta en función del menor coste total
    mejor_ruta = rutas_df.loc[rutas_df["total_cost"].idxmin()]

    geometry = loads(mejor_ruta["WKT"])
    geojson_feature = {
        "type": "Feature",
        "geometry": mapping(geometry),
        "properties": {
            "sector_id": sector_id,
            "sector": sectores_info[sector_id],
            "start_entry_cost": mejor_ruta["start_entry_cost"],
            "end_exit_cost": mejor_ruta["end_exit_cost"],
            "cost_on_graph": mejor_ruta["cost_on_graph"],
            "total_cost": mejor_ruta["total_cost"]
        }
    }

    geojson_data["features"].append(geojson_feature)
    index += cantidad

# Guardar el archivo GeoJSON final
ruta_geojson = "rutaEvacuacion.geojson"
with open(ruta_geojson, "w") as f:
    json.dump(geojson_data, f, indent=4)

print("GeoJSON con rutas por sector guardado correctamente.")