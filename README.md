# 🤖 AI Log Analysis Agent (RAG Powered)

## 📖 Project Overview

AI Log Analysis Agent is a Retrieval-Augmented Generation (RAG) based application that automatically analyzes application logs using Artificial Intelligence.

Instead of manually searching thousands of log entries, users can simply ask questions in natural language. The system retrieves the most relevant log entries using semantic search and generates an AI-powered analysis using a Large Language Model (LLM).

The project demonstrates the complete RAG pipeline including log parsing, knowledge base creation, embedding generation, vector database indexing, retrieval, prompt engineering, and AI-powered analysis.

---

# 🎯 Problem Statement

Modern software systems generate a huge number of log files. Finding the root cause of an issue manually is time-consuming.

Traditional keyword search often fails because similar issues can be described using different words.

This project solves the problem by using semantic search with vector embeddings and Retrieval-Augmented Generation (RAG).

---

# ✨ Features

- Parse structured and semi-structured log files
- Create a searchable knowledge base
- Generate text embeddings using SentenceTransformer
- Store embeddings in Qdrant Vector Database
- Semantic similarity search
- AI-powered log analysis using Ollama
- Conversation mode
- Automatic JSON report generation
- Configurable using JSON configuration files

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| SentenceTransformers | Text Embeddings |
| Qdrant | Vector Database |
| Ollama | Local LLM Runtime |
| llama3.2 | AI Language Model |
| JSON | Configuration and Reports |
| argparse | Command-line Interface |

---

# 🏗 System Architecture

```
                   User Question
                         │
                         ▼
              SentenceTransformer
                         │
                 Query Embedding
                         │
                         ▼
                 Qdrant Vector DB
                         │
              Retrieve Similar Logs
                         │
                         ▼
                 Prompt Engineering
                         │
                         ▼
                 Ollama (llama3.2)
                         │
                         ▼
                AI Generated Analysis
                         │
                         ▼
               JSON Analysis Report
```

---

# 📂 Project Structure

```text
AI_LOG_ANALYSIS_AGENT/

├── agent/
├── Parser/
├── knowledge_base/
├── embeddings/
├── retriever/
├── vector_db/
├── logs/
├── test_logs/
├── output/
├── output_report/
├── config.json
├── test_config.json
├── requirements.txt
├── README.md
└── explanation.txt
```

---

# 🔄 Workflow

### Step 1

Parse raw log files into structured documents.

↓

### Step 2

Create a Knowledge Base.

↓

### Step 3

Generate embeddings using SentenceTransformer.

↓

### Step 4

Store embeddings inside Qdrant.

↓

### Step 5

Convert user query into an embedding.

↓

### Step 6

Retrieve Top-K relevant logs using cosine similarity.

↓

### Step 7

Build a Retrieval-Augmented prompt.

↓

### Step 8

Generate AI analysis using Ollama (llama3.2).

↓

### Step 9

Display analysis and save it as a JSON report.

---

# 🚀 Installation

Install required packages

```bash
pip install -r requirements.txt
```

Pull Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

# ▶ Running the Project

### Create Knowledge Base

```bash
python -m knowledge_base.create_knowledge_base --config test_config.json
```

### Generate Embeddings

```bash
python -m embeddings.generate_embeddings --config test_config.json
```

### Store Embeddings

```bash
python -m vector_db.qdrant_store --config test_config.json
```

### Run AI Agent

```bash
python -m agent.ai_agent --config test_config.json
```

---

# 💬 Sample Questions

```
packet errors

database timeout

authentication failure

invalid token

memory leak

NOT FOUND packets

slow query

connection timeout
```

---

# 📄 Output

The AI generates a professional report containing:

- Executive Summary
- Root Cause Analysis
- Error Severity
- Supporting Evidence
- Affected Components
- Possible Impact
- Recommended Resolution
- Confidence Score

Each analysis is automatically saved as:

```
output_report/
analysis_YYYYMMDD_HHMMSS.json
```

---

# 📚 Concepts Demonstrated

- Log Parsing
- Knowledge Base Creation
- Sentence Embeddings
- Vector Databases
- Semantic Search
- Cosine Similarity
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Local Large Language Models

---

# 🚀 Future Enhancements

- Streamlit Web Interface
- FastAPI Integration
- PDF Report Generation
- Metadata Filtering
- Hybrid Search
- Dashboard Visualization
- Multi-LLM Support
- Cloud Deployment

---

# 👨‍💻 Author

**Manit Shah**

B.Tech Computer Science Engineering (AI & ML)

Adani University

---

# 📜 License

This project is developed for educational and learning purposes.