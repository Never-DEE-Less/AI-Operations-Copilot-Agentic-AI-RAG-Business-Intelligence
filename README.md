# # AI Operations Copilot | Agentic AI, RAG & Business Intelligence

An AI-powered operations dashboard that combines business analytics, natural-language data querying, and Retrieval-Augmented Generation (RAG) to answer questions about business metrics and indexed documents.

## Overview

AI Operations Copilot is an AI-powered analytics application that combines business intelligence, tool-augmented LLM workflows, and Retrieval-Augmented Generation (RAG) in a full-stack application.

Built with FastAPI, React, TypeScript, PostgreSQL, and pgvector, the application enables users to explore business metrics through natural-language queries and retrieve relevant information from indexed PDF documents. It uses LangChain-based agent orchestration and locally hosted Ollama models for tool selection, document retrieval, and question answering.

## Key Engineering Contributions

- **AI Application Development:** Developed a full-stack AI analytics application integrating a React dashboard with FastAPI REST endpoints.
- **Agentic AI & Tool Orchestration:** Implemented LLM-driven routing to specialized analytics and document-retrieval tools for business questions.
- **Retrieval-Augmented Generation (RAG):** Built a PDF ingestion and semantic search pipeline using text chunking, Ollama embeddings, and PostgreSQL/pgvector.
- **Business Intelligence:** Implemented analytics for revenue by category, monthly revenue trends, and top-customer rankings.
- **Reliable Document Q&A:** Added source filtering, similarity-distance thresholds, and handling for questions whose answers are absent from retrieved documents.
- **Database Engineering:** Integrated SQLAlchemy, PostgreSQL models, vector storage, and Alembic migrations.
- **Testing & Validation:** Created automated tests for API behavior, analytics tools, and agent routing, including multi-tool execution scenarios.

## Features

- **Business analytics:** Analyze revenue by category, monthly revenue trends, and top customers.
- **AI assistant:** Ask natural-language questions through a chat interface.
- **Tool orchestration:** Route questions to the appropriate analytics or document-search tools.
- **Document Q&A with RAG:** Retrieve relevant text from indexed PDF documents to answer document-related questions.
- **Vector search:** Store and retrieve document embeddings using PostgreSQL with pgvector.
- **REST API:** Serve application functionality through FastAPI endpoints.
- **Database migrations:** Manage database schema changes using Alembic.
- **Automated tests:** Test API behavior, analytics tools, and agent routing.

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Frontend | React, TypeScript, Vite |
| Database | PostgreSQL, SQLAlchemy, pgvector |
| Migrations | Alembic |
| AI orchestration | LangChain, LangGraph |
| Language models | Ollama with Qwen2.5 7B |
| Embeddings | Ollama with nomic-embed-text |
| Document processing | pypdf, LangChain text splitters |
| Testing | pytest, HTTPX |
| Development environment | Docker Compose, uv, npm |

## Architecture

```text
React + TypeScript Dashboard
            |
            v
       FastAPI Backend
            |
            v
     AI Agent / Router
       /           \
      v             v
Analytics Tools   Document Retrieval
      |             |
      v             v
Business Data    PostgreSQL + pgvector
                    ^
                    |
              PDF Ingestion
```

The AI agent selects tools based on the user's question. Analytics requests use the corresponding business-data tools, while document questions use retrieval over indexed document chunks.

## Project Structure

```text
AI_Ops_Project/
├── frontend/                 # React + TypeScript UI
├── migrations/               # Alembic migrations
├── scripts/                  # Data seeding, ingestion and evaluation
├── src/ai_ops/
│   ├── api/                  # API routes
│   ├── core/                 # Application configuration
│   ├── db/                   # Database models and sessions
│   ├── rag/                  # Document retrieval
│   ├── agent.py              # AI agent configuration
│   ├── agent_tools.py        # Analytics and retrieval tools
│   ├── analytics.py          # Analytics queries
│   └── main.py               # FastAPI application
├── tests/                    # Automated tests
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- [Node.js and npm](https://nodejs.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/)

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Never-DEE-Less/AI_Ops_Project.git
cd AI_Ops_Project
```

### 2. Install Python dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create your local environment file from the example:

```bash
cp .env.example .env
```

Review `.env.example` and configure the database connection and any other settings required by the application. Keep `.env` private and never commit secrets.

### 4. Start PostgreSQL

```bash
docker compose up -d
```

Ensure the database settings in `.env` match the PostgreSQL configuration in `docker-compose.yml`.

### 5. Apply database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the local language model

Install and start Ollama, then download the models used by the application:

```bash
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```

### 7. Start the backend

From the project root:

```bash
uv run uvicorn ai_ops.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 8. Start the frontend

Open a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open the local frontend URL printed by Vite, typically http://localhost:5173.

## Document Ingestion

Place a PDF you are authorized to process in the expected local document directory, then run the ingestion script:

```bash
uv run python scripts/ingest_pdf.py
```

Check the script's configuration before running it to confirm the input PDF path, embedding model, and vector-store settings.

The document-search workflow retrieves relevant text from indexed documents. Answers should reflect the retrieved content rather than inventing missing details.

## Testing

Run the automated test suite:

```bash
uv run pytest -v
```

Run the agent evaluation script:

```bash
uv run python scripts/test_agent.py
```

The evaluation script checks whether expected tools are executed for representative questions. Tool selection alone does not establish that every generated answer is factually correct.

## API

The application includes health checks, business analytics endpoints, and an AI question-answering endpoint.

Explore the available routes and request schemas through the interactive FastAPI documentation at `/docs` after starting the backend.

## Security and Limitations

- Do not commit `.env`, API keys, passwords, private documents, or personal datasets.
- Local Ollama models require Ollama to be running and the required models to be installed.
- A public deployment needs a reachable model endpoint, suitable database hosting, and production environment configuration.
- Local development success does not by itself establish production readiness.

## Future Improvements

- Deploy the frontend and API with production-ready configuration.
- Add authentication and authorization.
- Improve monitoring, logging, and error handling.
- Expand automated evaluation to assess answer correctness as well as tool selection.
- Add deployment documentation and a live demo when available.

## License

No license has been specified yet.

