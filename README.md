![Alt text](./EG_LOGO.png)
# Synthetic Review Generator with Guardrails

This project implements a **synthetic data generation pipeline** for realistic software/tool reviews, enriched with **automated quality guardrails** and **model-level comparison**.  
The system is designed to generate human-like reviews, evaluate their quality, enforce diversity, and compare multiple LLMs under identical conditions.

---

## 🚀 Project Overview

The goal of this project is to generate **high-quality synthetic user reviews** while avoiding:
- Near-duplicate content
- Unrealistic or marketing-style language
- Domain-irrelevant text
- Sentiment–rating mismatch

To achieve this, we combine:
- Controlled generation via prompts and model parameters
- Semantic evaluation using sentence embeddings
- Automatic rejection and regeneration
- Comparative evaluation between multiple LLMs

---

## ✨ Key Features

- **Synthetic Review Generation**
  - Persona-aware, rating-controlled review generation
  - Supports multiple LLMs (Groq-hosted LLaMA models)
  - Configurable via JSON

- **Quality Guardrails**
  - Semantic diversity enforcement
  - Domain realism validation
  - Exaggeration / marketing-hype detection
  - Length and rating-consistency checks
  - Composite quality score (0–1)

- **Automatic Regeneration**
  - Low-quality samples are rejected and regenerated
  - Configurable retry limits

- **Model Comparison**
  - Compare quality, diversity, and performance across models
  - Generates a structured Markdown report

- **FastAPI Interface**
  - Downloadable quality report (`.md`)
  - Ready for extension (API / CLI)

---

## 🧠 Models Used

The project compares two Groq-hosted models under identical conditions:

- **LLaMA 3.3 70B – Versatile**
- **LLaMA 4 Scout 17B – Instruct**

Both models:
- Use the same prompts
- Use the same generation parameters
- Are evaluated using the same quality pipeline

---

## 🏗️ Architecture Overview

```text
Generation
   ↓
Prompt + Model Parameters
   ↓
Raw Review
   ↓
Quality Evaluation
   ├─ Length Check
   ├─ Semantic Diversity (Sentence Transformers)
   ├─ Domain Semantic Similarity
   ├─ Rating Consistency
   ├─ Exaggeration Detection
   ↓
Quality Score (0–1)
   ↓
Accept / Reject
   ↓
Dataset + Metrics
   ↓
Model Comparison Report (.md)
```


## 🏗️ Architecture Overview

```
├── config
│   ├── config.json
│   └── __init__.py
├── generate_reports
│   ├── generate_reports.py
│   ├── __init__.py
│   └── __pycache__
│       ├── generate_reports.cpython-310.pyc
│       └── __init__.cpython-310.pyc
├── helpers
│   ├── compare_models.py
│   ├── compare_real.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── compare_models.cpython-310.pyc
│   │   ├── compare_real.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   └── utils.cpython-310.pyc
│   └── utils.py
├── llm_store
│   ├── groq.py
│   ├── __init__.py
│   └── __pycache__
│       ├── groq.cpython-310.pyc
│       └── __init__.cpython-310.pyc
├── main.py
├── output
│   ├── llama-4-scout-17b-16e-instruct.json
│   ├── real_reviews.json
│   └── reviews_llama-3.3-70b-versatile.json
├── __pycache__
│   └── main.cpython-310.pyc
├── README.md
├── reports
│   └── report.md
├── requirements.txt
├── review
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── review_generated_sample.cpython-310.pyc
│   └── review_generated_sample.py
└── routes
    ├── generate.py
    ├── generate_reports_api.py
    ├── __init__.py
    └── __pycache__
        ├── generate.cpython-310.pyc
        ├── generate_reports_api.cpython-310.pyc
        └── __init__.cpython-310.pyc

15 directories, 36 files
```

## 📊 Quality Scoring

Each review receives a **composite quality score** based on:

| Component          | Description                            |
| ------------------ | -------------------------------------- |
| Length             | Compliance with min/max word limits    |
| Semantic Diversity | Penalizes near-duplicate content       |
| Domain Realism     | Semantic similarity to domain anchor   |
| Rating Consistency | Alignment between text and rating      |
| Forbidden Penalty  | Penalizes exaggerated / marketing tone |

### Final Quality Formula

```text
quality =
(0.20 × length
+ 0.35 × diversity
+ 0.25 × domain
+ 0.20 × rating)
× penalty
```

## 🧬 Semantic Evaluation

* Uses **Sentence Transformers (MiniLM)** on CPU for portability
* All embeddings are normalized
* Cosine similarity is used for:

  * Inter-review similarity (diversity)
  * Domain realism scoring
  * Exaggeration detection (anchor-based)

This avoids brittle keyword-based heuristics.

## 📈 Model Comparison

The system compares models on:

### Performance

* Average generation time
* Median generation time
* Attempts per accepted review

### Quality

* Average quality score
* Quality variance (consistency)
* Acceptance rate

### Diversity

* Average semantic similarity
* Near-duplicate rate
* Average diversity score

### Domain Realism

* Domain semantic score
* Forbidden / exaggeration score

## 🐳 Docker Support

The project is fully containerized using **Docker** to ensure reproducibility, portability, and ease of deployment across different environments.

The Docker setup is **CPU-only** and optimized for lightweight NLP workloads, making it suitable for local development, servers, and cloud environments without GPU requirements.

---

## 📦 Docker Requirements

* Docker >= 20.x
* No GPU or CUDA required
* Internet access on first run (to download models)

---

## 🏗️ Docker Image Design

* **Base image:** `python:3.10-slim`
* **Execution mode:** CPU-only
* **Web server:** Uvicorn
* **Framework:** FastAPI
* **Semantic models:** Sentence Transformers (MiniLM)

The image is intentionally kept minimal to reduce size and startup time.

---

## 🛠️ Build Docker Image

From the project root directory:

```bash
docker build -t synthetic-review-api .
```

This will:

* Install all Python dependencies
* Copy the full project source
* Prepare the FastAPI application for execution

---

## ▶️ Run the Container

### Basic run

```bash
docker run -p 8000:8000 synthetic-review-api
```

Access the API at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---

## 📂 Persisting Outputs (Recommended)

To persist generated reports and outputs outside the container:

```bash
docker run \
  -p 8000:8000 \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/output:/app/output \
  synthetic-review-api
```

This ensures:

* Generated Markdown reports are saved locally
* Output datasets are preserved across container restarts

---

## 📄 Downloading the Report (Docker)

Once the container is running, the comparison report can be downloaded via:

```http
POST /generate_reports
```

The response is a downloadable Markdown file:

```
model_comparison.md
```

---

## ⚙️ Environment & Performance Notes

* Sentence Transformer models are downloaded on first run and cached inside the container
* Initial startup may take slightly longer due to model loading
* Subsequent requests are significantly faster
* The system is optimized for datasets in the range of hundreds to low thousands of samples

---

## 🔒 Security & Best Practices

* No dynamic file paths are exposed in the API
* Download endpoints are read-only
* Docker image excludes unnecessary files via `.dockerignore`
* CPU-only execution avoids GPU dependency issues

---

## 📌 Design Rationale

Docker was chosen to:

* Standardize the execution environment
* Simplify deployment and evaluation
* Avoid dependency conflicts
* Ensure consistent benchmarking across models

---

## 🧾 Example README Footer Addition (Optional)

```md
This project is fully containerized and can be deployed on any Docker-compatible environment without additional system dependencies.
```

---

## ✅ Summary of Docker Integration

* ✔ Portable deployment
* ✔ CPU-only (no CUDA required)
* ✔ FastAPI-ready
* ✔ Persistent outputs supported
* ✔ Production-friendly setup

---
