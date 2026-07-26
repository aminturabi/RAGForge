<div align="center">

# ⚡ RAGForge

### *A Production-Grade, Highly Modular RAG Framework & Plug-and-Play Toolkit*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![CI Build](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20%26%20Decoupled-purple.svg)](docs/ARCHITECTURE.md)

[Features](#-key-features) •
[Architecture](#-architecture) •
[Quick Start](#-quick-start) •
[Plugin Ecosystem](#-plugin-ecosystem) •
[Examples](#-interactive-examples) •
[Roadmap](#-project-roadmap) •
[Contributing](CONTRIBUTING.md)

---

</div>

**RAGForge** is an open-source, highly modular Retrieval-Augmented Generation (RAG) framework built for software engineers, AI researchers, and open-source contributors. Unlike monolithic chatbot scripts, **RAGForge** decouples every single component in the RAG pipeline into plug-and-play, replaceable modules backed by abstract interfaces and a dynamic registry system.

Whether you need to swap vector databases from **ChromaDB** to **FAISS**, **Qdrant**, or **Pinecone**, switch embedding models, or ingest non-traditional documents (CSV, Markdown, Web URLs, YouTube transcripts, GitHub repositories), RAGForge lets you register new components with a single Python decorator.

---

## 🚀 Key Features

- **🧩 100% Replaceable Architecture**: Every RAG component (Loader, Chunker, Embedding Model, Vector Store, Retriever, Reranker, LLM Provider, Output Formatter) is an isolated module.
- **🔌 Dynamic Plugin System**: Simply create a python file under `plugins/` and add `@register_plugin("category", "name")`.
- **⚡ Multiple Vector Store Backends**: Built-in support for **ChromaDB**, **FAISS**, **Qdrant**, and **Pinecone**.
- **📄 Multi-Source Ingestion**: Load PDF, CSV, Markdown, Web pages, YouTube transcripts, and GitHub codebase directories out of the box.
- **🛡️ Clean Architecture & SOLID Principles**: Type hints, strict contracts, DI containers, and graceful error handling (`PluginDependencyError`).
- **🌐 Legacy Flask Web Dashboard**: Complete backward compatibility with the existing glassmorphic Flask web app and API routes.

---

## 🏗️ Architecture

```
                    ┌─────────────────────────┐
                    │  Flask / REST / CLI /   │  (Delivery Layer)
                    │     Example Scripts     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       RAGService        │  (Application Orchestrator)
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         │              Abstract Core Contracts          │  (Domain Interfaces)
         └───────┬───────┬───────┬───────┬───────┬───────┘
                 │       │       │       │       │
                 ▼       ▼       ▼       ▼       ▼
              Loaders Chunker Embed Vector  LLMs...       (Plugins Layer)
```

---

## 📦 Installation

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/aminturabi/RAGForge.git
cd RAGForge

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🏁 Quick Start

### 1. Python API Usage
```python
from core.container import build_service

# Build default RAG service with ChromaDB + Groq + SentenceTransformers
service = build_service()

# Index a document
result = service.index_document(file_path="sample.pdf", original_filename="sample.pdf")

# Query the collection
response = service.query(collection_name=result["collection_name"], query="What is the summary?")
print(response["answer"])
```

### 2. Running the Flask Web App
```bash
python app.py
```
Navigate to `http://127.0.0.1:5000` to access the glassmorphic web dashboard!

### 3. REST API Endpoints
- `POST /api/upload`: Upload and index a document (`.pdf`, `.txt`, `.csv`, `.md`, `.html`).
- `POST /api/query`: Query an indexed document collection with top-K vector search and Groq LLM completion.
- `GET /api/collections`: List all active collections in vector store.
- `POST /api/clear`: Delete a collection from vector store.
- `GET /api/plugins`: Inspect registered plugin capabilities by category.

---

## 🧩 Plugin Ecosystem

RAGForge allows contributors to easily add new capabilities:

| Component Type | Included Plugins |
| --- | --- |
| **Document Loaders** | `Composite`, `PDF`, `Text`, `CSV`, `Markdown`, `Web`, `YouTube`, `GitHub` |
| **Chunking Strategies** | `RecursiveCharacter` |
| **Embedding Models** | `SentenceTransformer` (`all-MiniLM-L6-v2`) |
| **Vector Databases** | `Chroma`, `FAISS`, `Qdrant`, `Pinecone` |
| **Retrievers** | `DenseVectorRetriever` |
| **Rerankers** | `NoOpReranker` |
| **LLM Providers** | `Groq` |
| **Formatters** | `DefaultJSON` |

### How to Create a Custom Plugin
```python
from core.contracts import VectorStoreBackend
from core.registry import register_plugin

@register_plugin("vectorstores", "my_custom_store")
class MyCustomStore(VectorStoreBackend):
    def add_documents(self, collection_name, documents, embeddings, ids):
        ...
    def query(self, collection_name, query_embeddings, n_results=4):
        ...
    def delete_collection(self, collection_name):
        ...
    def list_collections(self):
        ...
```

---

## 💡 Interactive Examples

Run any of the provided example scripts under `examples/`:

- **PDF Chat**: `python examples/pdf_chat.py`
- **CSV Data Chat**: `python examples/csv_chat.py`
- **Markdown Chat**: `python examples/markdown_chat.py`
- **Website Chat**: `python examples/website_chat.py`
- **GitHub Repo Chat**: `python examples/github_repository_chat.py`
- **YouTube Transcript Chat**: `python examples/youtube_transcript_chat.py`
- **Research Paper Chat**: `python examples/research_paper_chat.py`

---

## 🗺️ Project Roadmap

- [x] **v1.0.0 (Current)**: Core Clean Architecture refactor, dynamic plugin registration, vector store backends (Chroma, FAISS, Qdrant, Pinecone), expanded loaders, and legacy Flask support.
- [ ] **v1.5.0**: BM25 + Dense Hybrid Search retriever, Cohere Reranker, Ollama local LLM plugin, and async batching.
- [ ] **v2.0.0**: RAG evaluation pipeline metrics (Faithfulness, Context Precision/Recall) under `evaluation/`, latency benchmarking suite under `benchmarks/`.
- [ ] **v3.0.0**: Multi-modal embeddings (CLIP), agentic RAG routing with tool execution, distributed index management, and FastAPI web runtime.

---

## 🙋 FAQ

#### Q: How does RAGForge handle missing vector store packages?
**A**: RAGForge uses graceful lazy-loading. If a user selects `qdrant` or `pinecone` without having installed `qdrant-client` or `pinecone-client`, RAGForge raises a descriptive `PluginDependencyError` instructing the user on how to install the required package.

#### Q: Is the original Flask app still supported?
**A**: Yes! The original Flask application endpoints in `api/routes.py` and `app.py` use adapter layers (`rag/`) that seamlessly map onto the new `RAGService` orchestrator.

---

## 🤝 Contributing

Contributions are welcome!

Check out the [Good First Issues](docs/GOOD_FIRST_ISSUES.md) to get started.

- Report bugs
- Suggest features
- Improve documentation
- Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 License

Distributed under the [MIT License](LICENSE).


