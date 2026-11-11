import os
import re
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

app = FastAPI(title="Kestrel Nova Policy Q&A Assistant", version="1.0.0")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="company_policies")

POLICIES_DIR = "policies"

def load_and_chunk_policies():
    if not os.path.exists(POLICIES_DIR):
        return
    
    for filename in os.listdir(POLICIES_DIR):
        if filename.endswith(".md"):
            doc_id = filename[:-3]
            filepath = os.path.join(POLICIES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            sections = re.split(r'\n(?=##\s+\d+[\.\s])', content)
            
            for section_text in sections:
                if not section_text.strip():
                    continue
                
                match = re.search(r'##\s+(\d+)', section_text)
                section_num = match.group(1) if match else "1"
                
                chunks = section_text.split("\n\n")
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) < 20:
                        continue
                    chunk_id = f"{doc_id}_sec{section_num}_chunk{i}"
                    embedding = embedder.encode(chunk).tolist()
                    
                    collection.add(
                        ids=[chunk_id],
                        embeddings=[embedding],
                        documents=[chunk.strip()],
                        metadatas=[{"doc_id": doc_id, "section": section_num}]
                    )

load_and_chunk_policies()

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)

class Citation(BaseModel):
    doc_id: str
    section: str
    quote: str

class AskResponse(BaseModel):
    question: str
    answered: bool
    answer: str
    citations: List[Citation] = []

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask_policy(req: AskRequest):
    question = req.question.strip()
    
    q_embedding = embedder.encode(question).tolist()
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=4
    )
    
    retrieved_docs = results['documents'][0] if results['documents'] else []
    retrieved_metas = results['metadatas'][0] if results['metadatas'] else []
    
    if not retrieved_docs:
        return AskResponse(
            question=question,
            answered=False,
            answer="The policy documents do not contain information about this.",
            citations=[]
        )
    
    context_blocks = []
    for doc, meta in zip(retrieved_docs, retrieved_metas):
        context_blocks.append(f"[Doc ID: {meta['doc_id']}, Section: {meta['section']}]\n{doc}")
    
    context_str = "\n\n---\n\n".join(context_blocks)
    
    prompt = f"""You are an internal corporate policy assistant for Kestrel Nova Ltd.
Answer the employee's question using ONLY the provided policy excerpts.
Every fact in your answer must be supported by the text. 

If the answer cannot be found in the excerpts, you must set answered to false and state that the policy documents do not contain the information. Do not guess or extrapolate.

Context Excerpts:
{context_str}

Question: {question}

Return your response in strict JSON format with keys:
- "answered": boolean (true if found, false otherwise)
- "answer": string (plain language answer, or refusal statement)
- "citations": array of objects, each containing:
    - "doc_id": file name without .md
    - "section": top-level section number as a string (e.g., "4")
    - "quote": exact verbatim quote copied from the source text supporting the claim.
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise corporate policy assistant. Output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        import json
        response_data = json.loads(completion.choices[0].message.content)
        
        answered = response_data.get("answered", False)
        answer_text = response_data.get("answer", "")
        raw_citations = response_data.get("citations", [])
        
        formatted_citations = []
        if answered:
            for c in raw_citations:
                formatted_citations.append(Citation(
                    doc_id=c.get("doc_id"),
                    section=str(c.get("section")),
                    quote=c.get("quote")
                ))
        
        return AskResponse(
            question=question,
            answered=answered,
            answer=answer_text,
            citations=formatted_citations if answered else []
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal failure: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
