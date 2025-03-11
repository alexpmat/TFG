
# Optimización de Rutas de Evacuación ante Tsunamis
**Aplicación en: Playa Centro, Alicante**

Este proyecto desarrolla un sistema de optimización de rutas de evacuación ante tsunamis mediante teoría de grafos y machine learning. Integra bases de datos espaciales, algoritmos de optimización de rutas (Dijkstra), modelos de machine learning y visualización web interactiva con Leaflet.

---

## Estructura del Proyecto

```
/backend
    ├── server.js
    ├── package.json
    ├── package-lock.json
    └── rutaEvacuacion.geojson
/frontend
    ├── WebVisorTFG.html
    ├── sectores.geojson
/ml_model
    ├── train_model.py
    ├── app.py
    └── model.pkl
evacuacion_tsunamis.sql
README.md
.gitignore

---

## Requisitos

### Software necesario
- Node.js (v14 o superior)
- PostgreSQL + PostGIS
- Python 3.8 o superior
- Librerías Python:
  - pandas
  - scikit-learn
  - shapely
- Navegador Web (Chrome recomendado)

---

## Instalación

### 1. Clonar el Repositorio
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio


### 2. Backend (API REST)
cd backend
npm install

Iniciar el servidor Node.js:
node server.js

Servidor disponible en `http://localhost:3000`.

### 3. Base de Datos
CREATE DATABASE evacuacion_tsunamis;
CREATE EXTENSION postgis;

Importar el script SQL:
psql -U postgres -d evacuacion_tsunamis -f evacuacion_tsunamis.sql

### 4. Frontend (Visor Web)
npx serve ./frontend

Accede a: [http://localhost:5000](http://localhost:5000)

### 5. Machine Learning (opcional)
cd ml_model
python train_model.py

---

## Configuración

Modificar el acceso a PostgreSQL en `server.js` si es necesario:
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'evacuacion_tsunamis',
    password: 'tu_password',
    port: 5432,
});

---

## Tecnologías utilizadas
- Node.js + Express
- PostgreSQL + PostGIS
- Python + scikit-learn
- Leaflet.js
- GeoJSON

---

## Licencia
Proyecto de un Trabajo de Fin de Grado (TFG) de Ingeniería Informática. Uso académico y educativo.

---

## Autor
- Alex Pareja Mateos
- Universidad Alfonso X el Sabio
- Contacto: aparemat@myuax.com