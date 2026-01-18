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
