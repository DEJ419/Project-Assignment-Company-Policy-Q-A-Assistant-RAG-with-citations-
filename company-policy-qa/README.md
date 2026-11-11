# Kestrel Nova Ltd - Company Policy Q&A Assistant

A Retrieval-Augmented Generation (RAG) microservice that answers employee questions based strictly on company policy documents, featuring precise verbatim quote citations and robust out-of-domain refusals.

---

## Models & Tech Stack
* **LLM:** `gpt-4o-mini` (via OpenAI API) configured with zero temperature (`temperature=0.0`) for deterministic, grounded extraction.
* **Embeddings:** `all-MiniLM-L6-v2` via `sentence-transformers` for local semantic vector generation.
* **Vector Store:** ChromaDB (In-memory mode).
* **Framework:** FastAPI & Uvicorn.

---

## Design Choices & Rationale
1. **Document Splitting Strategy:** Policy documents are split by top-level Markdown section headers (`## <section_number>`) rather than fixed token lengths. This preserves policy context integrity and allows exact section number mapping for citations.
2. **Retrieval Top-K:** We retrieve the top 4 semantic chunks to ensure comprehensive context coverage while preventing prompt dilution or hallucination.
3. **Refusal Mechanism:** System instructions enforce strict grounding. If retrieved chunks do not contain the answer, the model outputs `answered: false` with a standardized refusal message, avoiding speculative answers.
4. **Citation Validation:** Citations are required to include exact verbatim quotes (`citations[].quote`), verified against source documents.

---

## Setup & Running the Service

1. Clone repository and navigate to root directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create your environment configuration file:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY into the .env file
   ```
4. Start the FastAPI server:
   ```bash
   python app.py
   ```
   *(The service runs on port `8000` by default or reads from the `PORT` environment variable.)*

---

## Evaluation & Test Execution
Run the evaluation script across all test questions:
```bash
python evaluate.py
```

## Summary Counts (Evaluation on Test Questions)
* **Correct Answers:** 12
* **Correct Refusals:** 3
* **Failures (Incorrect / Wrong Refusals):** 0
