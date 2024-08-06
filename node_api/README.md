# Node.js LLM Chat API Server
A RESTful API server for interfacing with the Python LLM Chat application.

## Features
- RESTful API for LLM chat interactions
- Manages communication with Python LLM script
- Stores conversation history

## Quick Start

1. Clone and navigate to the repository:
   ```
   git clone https://github.com/emman25/llm.git
   cd llm/node_api
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   PYTHON_SCRIPT_PATH=../python/app.py
   HUGGINGFACEHUB_API_TOKEN=your-huggingface-token
   ```

4. Start the server:
   ```
   npm start
   ```

The server will start on `http://localhost:3000` by default.

## API Endpoints

- `POST /chat`
  - Body: `{ "model": "llama2" or "mistral", "message": "Your message here" }`
  - Returns: `{ "response": "AI response here" }`

- `GET /conversations`
  - Returns: List of recent conversations

- `GET /conversation/:id`
  - Returns: Details of a specific conversation

## Docker Usage

Build and run with Docker:
```
docker build -t nodejs-llm-api .
docker run -p 3000:3000 --env-file .env nodejs-llm-api
```

## Notes
- Requires Node.js 18+
- Ensure the Python LLM script is correctly set up and accessible