# LLM Chat Application

Chat application using Large Language Models (LLMs), combining Python, Node.js, and PostgreSQL.

## Components

1. [Python LLM Backend](./python/README.md)
2. [Node.js API Server](./node_api/README.md)
3. PostgreSQL Database

## Quick Start with Docker Compose

1. Clone the repository:
   ```
   git clone https://github.com/emman25/llm.git
   cd llm
   ```

2. Start the application:
   ```
   docker-compose up --build
   ```

4. Access the API at `http://localhost:3000`

## Project Structure

```
project_root/
├── docker-compose.yml
├── README.md
├── python/
│   ├── README.md
│   ├── Dockerfile
│   └── ...
└── node_api/
    ├── README.md
    ├── Dockerfile
    └── ...
```

For detailed information on each component, refer to their respective READMEs.

## Development

Modify files in `python/` or `node_api/` directories, then rebuild:
```
docker-compose down
docker-compose up --build
```
