# API Contract - Project 1: Company Policy Q&A Assistant

## Running the Service
- Default Port: `8000` (configurable via `PORT` environment variable).
- Content-Type: `application/json`
- Timeout limit per request: 60 seconds.

## Endpoints

### 1. GET /health
Response 200:
```json
{ "status": "ok" }
```

### 2. POST /ask
Request Body:
```json
{ "question": "How much paternity leave do I get?" }
```

Response 200 (Answered):
```json
{
  "question": "I stayed in a hotel costing NGN 70,000 per night on a domestic work trip. Is that within the limit?",
  "answered": true,
  "answer": "Yes. The domestic hotel limit is NGN 80,000 per night, so NGN 70,000 is within it.",
  "citations": [
    {
      "doc_id": "04_business_travel_policy",
      "section": "4",
      "quote": "Domestic hotels: maximum **NGN 80,000 per night**."
    }
  ]
}
```

Response 200 (Refused):
```json
{
  "question": "Can I bring my dog to the office?",
  "answered": false,
  "answer": "The policy documents do not contain information about this.",
  "citations": []
}
```
