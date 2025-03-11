const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Conexion a PostgreSQL usando DATABASE_URL de Render
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
});

// Ruta para obtener todas las rutas de evacuacion
app.get('/evacuacion', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT id, nombre, ST_AsGeoJSON(geom) AS geom
      FROM rutas_evacuacion;
    `);
    res.json(result.rows);
  } catch (err) {
    console.error('Error al obtener las rutas de evacuación:', err);
    res.status(500).json({ error: 'Error al obtener las rutas de evacuación' });
  }
});

// Ruta para obtener la mejor ruta segun el sector seleccionado
app.post('/ruta_optima', async (req, res) => {
  const { sector_id } = req.body;
  console.log('Buscando ruta para sector:', sector_id);

  if (!sector_id) {
    return res.status(400).json({ error: 'Sector no especificado' });
  }

  try {
    const result = await pool.query(`
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
    console.error('Error al obtener la ruta óptima:', err);
    res.status(500).json({ error: 'Error al obtener la ruta optimizada' });
  }
});

// Servir el archivo GeoJSON de los sectores
app.get('/sectores', (req, res) => {
  const filePath = path.join(__dirname, 'sectores.geojson');

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error al leer el archivo de sectores:', err);
      res.status(500).json({ error: 'Error al leer el archivo de sectores' });
    } else {
      res.setHeader('Content-Type', 'application/json');
      res.send(data);
    }
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});