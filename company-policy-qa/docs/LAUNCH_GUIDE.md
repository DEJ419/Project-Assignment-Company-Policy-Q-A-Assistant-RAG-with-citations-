# Project Launch & Operational Manual

Follow these steps to run, configure, and evaluate the Policy Q&A Assistant.

---

## Prerequisites
- Python 3.9+ installed
- OpenAI API Key

---

## Step-by-Step Setup

### 1. Extract Project Archives
Ensure all policy files (`policies/*.md`) are placed inside the `policies/` directory in the repository root[cite: 1].

### 2. Virtual Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create your `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Edit `.env` and insert your API key[cite: 3]:
```env
PORT=8000
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 4. Running the Microservice
Start the FastAPI application:
```bash
python app.py
```
The server will start listening on `http://localhost:8000`[cite: 3].

### 5. Running Health Check & Testing Endpoints
In a separate terminal, test the service health:
```bash
curl http://localhost:8000/health
```
*Expected Output:* `{"status":"ok"}`[cite: 3]

Test an ask request:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How much paternity leave do I get?"}'
```

### 6. Executing Automated Evaluation
Run the test harness across `test_questions.csv`[cite: 1, 5]:
```bash
python evaluate.py
```
Results will be written directly to `results.csv`[cite: 5].
