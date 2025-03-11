const express = require('express');
const fs = require('fs');
const cors = require('cors');
const { Client } = require('pg');

const app = express();
const port = 3000;

// Habilitar CORS para permitir solicitudes desde diferentes orígenes
app.use(cors());

// Habilitar el uso de JSON en las solicitudes
app.use(express.json());


// Configuración de la conexión a la base de datos PostgreSQL
const client = new Client({
    user: 'postgres',
    host: 'localhost',
    database: 'evacuacion_tsunamis',  // Nombre de la base de datos
    password: 'contrasenia',
    port: 5432,
});

// Conectar a la base de datos
client.connect();

// Ruta para obtener las rutas de evacuación desde la base de datos
app.get('/evacuacion', async (req, res) => {
    try {
        const result = await client.query(`
            SELECT id, nombre, ST_AsGeoJSON(geom) AS geom
            FROM rutas_evacuacion;
        `);
        res.json(result.rows);
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Error al obtener los datos de evacuación' });
    }
});

// Ruta para servir el archivo GeoJSON con las rutas de evacuación generadas
app.get('/evacuacion_geojson', (req, res) => {
    const filePath = 'data/rutaEvacuacion.geojson';
    
    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            console.error("Error: No se encontró el archivo GeoJSON.");
            return res.status(500).json({ error: 'No se pudo encontrar el archivo GeoJSON' });
        }

        fs.readFile(filePath, (err, data) => {
            if (err) {
                console.error("Error al leer el archivo GeoJSON:", err);
                return res.status(500).json({ error: 'No se pudo leer el archivo GeoJSON' });
            }
            console.log("Archivo GeoJSON leído correctamente.");
            res.header('Content-Type', 'application/json');
            res.send(data);
        });
    });
});

// Endpoint que devuelve la ruta óptima según el sector elegido
app.post('/ruta_optima', async (req, res) => {
    const { sector_id } = req.body;
    console.log('Buscando ruta para sector:', sector_id);

    if (!sector_id) {
        return res.status(400).json({ error: 'Sector no especificado' });
    }

    try {
        // Consulta la base de datos para obtener la ruta más óptima de ese sector
        const result = await client.query(`
            SELECT id, nombre, ST_AsGeoJSON(geom) AS geom
            FROM rutas_evacuacion
            WHERE sector_id = $1
            ORDER BY prioridad DESC
            LIMIT 1;
        `, [sector_id]);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No se encontró una ruta para el sector seleccionado' });
        }

        res.json(result.rows[0]);

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Error al obtener la ruta optimizada' });
    }
});


// Iniciar el servidor
app.listen(port, () => {
    console.log(`Servidor escuchando en http://localhost:${port}`);
});