[project_readme.md](https://github.com/user-attachments/files/34687128/project_readme.md)
# Project-Assignment-Company-Policy-Q-A-Assistant-RAG-with-citations-
# Kestrel Nova Ltd - Company Policy Q&A Assistant

A Retrieval-Augmented Generation (RAG) microservice that answers employee policy questions adhering strictly to internal policy documents, featuring precise verbatim citations and out-of-domain refusals.

---

## 1. Setup & Installation

### Prerequisites
* Python 3.9+
* OpenAI API Key

### Environment Setup
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/your-username/company-policy-qa.git
   cd company-policy-qa
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and add your `OPENAI_API_KEY`.

---

## 2. Running the Service

Start the FastAPI service:
```bash
python app.py
```
The service will start on `http://0.0.0.0:8000` (or the port specified in `PORT` env var).

Verify the health check endpoint:
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{ "status": "ok" }
```

---

## 3. Architecture & Models Used

* **Language Model:** `gpt-4o-mini` via OpenAI API (temperature set to `0.0` for deterministic extraction).
* **Embeddings Model:** `sentence-transformers/all-MiniLM-L6-v2` for dense semantic vector representation.
* **Vector Store:** ChromaDB running in-memory for instant startup and fast vector similarity search.
* **API Framework:** FastAPI with Pydantic payload validation.

---

## 4. Design Choices

* **Chunking Strategy:** Policies are partitioned by top-level Markdown headers (`## Section`). This retains complete contextual semantics of each policy section while maintaining exact mapping for top-level section citations.
* **Retrieval Configuration:** Top $K=4$ nearest neighbor chunks are retrieved per query. This maximizes recall while keeping prompt context focused and within context length limits.
* **Refusal Logic:** If retrieved contexts fail to yield a direct, facts-supported answer, the LLM is constrained to output `answered: false` with a standardized refusal string. Guessing and external knowledge extrapolation are strictly forbidden via system prompts.
* **Verbatim Citations:** Quotations are extracted directly from source text without modification, complying with strict matching validation rules.

---

## 5. Evaluation & Test Results Summary

To run the automated evaluation script on all 15 test questions:
```bash
python evaluate.py
```

### Summary Metrics
| Outcome Category | Count |
| :--- | :---: |
| **Correct Answers** | **11** |
| **Correct Refusals** | **4** |
| **Failures / Misclassifications** | **0** |
| **Total Test Cases** | **15** |

Detailed per-question breakdown is recorded in `results.csv`.
