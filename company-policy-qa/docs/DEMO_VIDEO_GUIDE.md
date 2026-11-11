# Demo Video Presentation Guide (2–3 Minutes)

This document provides a structure and script for recording the 2-3 minute demo video demonstrating the API service in operation[cite: 6].

---

## Video Outline & Timeline

| Time | Topic | Action / Screen Focus |
| :--- | :--- | :--- |
| **0:00 - 0:30** | Introduction & Overview | Show repository directory layout in your editor or terminal. |
| **0:30 - 1:15** | Environment & Startup | Run `python app.py` and point out health check output at `GET /health`[cite: 3]. |
| **1:15 - 2:15** | Live Endpoint Demonstration | Run cURL / Postman queries showing: 1. A valid answered question with citations[cite: 3]. 2. An out-of-policy question triggering refusal (`answered: false`)[cite: 3]. |
| **2:15 - 3:00** | Automated Evaluation Run | Execute `python evaluate.py` and view the populated `results.csv`[cite: 5]. |

---

## Demo Script

### 1. Introduction
> "Hello! In this demo, I'm presenting the Kestrel Nova Company Policy Q&A Assistant built with FastAPI, OpenAI, and ChromaDB[cite: 6]."

### 2. Starting the Service
> "First, we check our `.env` configuration and launch the server using `python app.py`. As seen in the terminal, Uvicorn starts listening on port 8000[cite: 3]."

### 3. Asking Policy Questions
> "Next, we run a query regarding business travel accommodation limits. The assistant returns `answered: true` along with the exact section citation and verbatim quote[cite: 3, 4]. When we ask a non-policy question like office pet policies, the model correctly responds with `answered: false`[cite: 3]."

### 4. Evaluation Script
> "Finally, we run `python evaluate.py` to evaluate all test cases and update `results.csv`[cite: 5]."
