import express from 'express';
import { Pool } from 'pg';
import bodyParser from 'body-parser';
import axios from 'axios';

const app = express();
const port = 3000;

app.use(bodyParser.json());

// PostgreSQL connection
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: parseInt(process.env.DB_PORT || '5432'),
});

// Initialize database
async function initDB() {
  const client = await pool.connect();
  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        model VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        conversation_id INTEGER REFERENCES conversations(id),
        role VARCHAR(10) NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
  } finally {
    client.release();
  }
}

initDB().catch(console.error);

const pythonApiUrl = process.env.PYTHON_API_URL || 'http://localhost:5000';

// API Endpoints
app.post('/chat', async (req, res) => {
  const { model, question } = req.body;

  if (!model || !question) {
    return res.status(400).json({ error: 'Both model and question are required' });
  }

  try {
    const pythonResponse = await axios.post(`${pythonApiUrl}/chat`, { model, message: question });
    const response = pythonResponse.data.response;
    await saveConversation(model, question, response);
    res.json({ response });
  } catch (error) {
    console.error('Error calling Python API:', error);
    res.status(500).json({ error: 'An error occurred while processing the request' });
  }
});

async function saveConversation(model: string, question: string, answer: string) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const conversationResult = await client.query(
      'INSERT INTO conversations (model) VALUES ($1) RETURNING id',
      [model]
    );
    const conversationId = conversationResult.rows[0].id;
    await client.query(
      'INSERT INTO messages (conversation_id, role, content) VALUES ($1, $2, $3), ($1, $4, $5)',
      [conversationId, 'user', question, 'assistant', answer]
    );
    await client.query('COMMIT');
  } catch (e) {
    await client.query('ROLLBACK');
    throw e;
  } finally {
    client.release();
  }
}

app.get('/conversations', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT id, model, created_at FROM conversations ORDER BY created_at DESC LIMIT 10'
    );
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred while fetching conversations' });
  }
});

app.get('/conversation/:id', async (req, res) => {
  const conversationId = req.params.id;
  try {
    const result = await pool.query(
      'SELECT role, content, created_at FROM messages WHERE conversation_id = $1 ORDER BY created_at ASC',
      [conversationId]
    );
    res.json(result.rows);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred while fetching conversation details' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});