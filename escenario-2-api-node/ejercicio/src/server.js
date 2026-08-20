const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  port: Number(process.env.DB_PORT) || 5432,
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'apidb'
});

function validarUsuario({ nombre, email }, parcial = false) {
  const errores = [];

  if (!parcial || nombre !== undefined) {
    if (!nombre || typeof nombre !== 'string' || nombre.trim().length < 2) {
      errores.push('nombre debe tener al menos 2 caracteres');
    }
  }

  if (!parcial || email !== undefined) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || typeof email !== 'string' || !emailRegex.test(email)) {
      errores.push('email debe ser un correo válido');
    }
  }

  return errores;
}

app.get('/health', (req, res) => {
  res.json({ status: 'OK', servicio: 'API Node.js Ejercicio', timestamp: new Date() });
});

app.get('/usuarios', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuarios ORDER BY id DESC');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/usuarios/:id', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM usuarios WHERE id = $1', [req.params.id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/usuarios', async (req, res) => {
  const errores = validarUsuario(req.body);
  if (errores.length) {
    return res.status(400).json({ errores });
  }

  try {
    const { nombre, email } = req.body;
    const result = await pool.query(
      'INSERT INTO usuarios (nombre, email) VALUES ($1, $2) RETURNING *',
      [nombre.trim(), email.trim().toLowerCase()]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.put('/usuarios/:id', async (req, res) => {
  const errores = validarUsuario(req.body, true);
  if (errores.length) {
    return res.status(400).json({ errores });
  }

  const { nombre, email } = req.body;
  if (nombre === undefined && email === undefined) {
    return res.status(400).json({ errores: ['Debe enviar nombre y/o email'] });
  }

  try {
    const actual = await pool.query('SELECT * FROM usuarios WHERE id = $1', [req.params.id]);
    if (actual.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }

    const nuevoNombre = nombre !== undefined ? nombre.trim() : actual.rows[0].nombre;
    const nuevoEmail = email !== undefined ? email.trim().toLowerCase() : actual.rows[0].email;

    const result = await pool.query(
      'UPDATE usuarios SET nombre = $1, email = $2 WHERE id = $3 RETURNING *',
      [nuevoNombre, nuevoEmail, req.params.id]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/usuarios/:id', async (req, res) => {
  try {
    const result = await pool.query(
      'DELETE FROM usuarios WHERE id = $1 RETURNING *',
      [req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json({ mensaje: 'Usuario eliminado', usuario: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API ejercicio escuchando en puerto ${PORT}`);
});
