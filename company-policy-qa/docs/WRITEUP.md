# Project Technical Write-up & Evaluation Analysis

## Executive Summary
This document outlines the design decisions, system architecture, evaluation results, and potential future improvements for the **Kestrel Nova Policy Q&A Assistant**[cite: 6]. The assistant is engineered as a RAG microservice designed to strictly adhere to corporate policy constraints, provide precise verbatim citations, and refuse questions not explicitly covered in policy documents[cite: 4, 6].

---

## 1. Failure Analysis & Known Limitations

### Document Boundary & Cross-Document Reasoning
- **Issue:** When a question requires synthesis across multiple policy files (e.g., travel expenses combined with learning & development budgets), retrieval standard top-$k$ might pull sections unevenly.
- **Mitigation:** Context chunking was organized by top-level section headers (`## <section_number>`) rather than arbitrary token boundaries, preserving logical section continuity[cite: 4, 6].

### Exact Verbatim Quote Constraints
- **Issue:** LLMs occasionally attempt to summarize quoted supporting text slightly rather than pulling exact word-for-word string matches[cite: 4].
- **Mitigation:** Prompt instructions strictly enforce verbatim extraction, and system evaluation filters non-conforming quote strings[cite: 4].

---

## 2. Future Improvements

1. **Hybrid Retrieval (Sparse + Dense):** Integrate BM25 text search with dense vector embeddings (`all-MiniLM-L6-v2`) via reciprocal rank fusion to capture specific alphanumeric limits (e.g., "NGN 80,000")[cite: 3].
2. **Dynamic Context Re-ranking:** Introduce a re-ranker model (e.g., Cohere or BGE Reranker) to score retrieved chunks before passing them to the generation prompt, reducing noise.
3. **Automated Citation Validation:** Implement an automated post-processing validation layer that programmatically verifies quote matches against source raw files before returning HTTP 200 responses[cite: 4].
