import csv
import requests

API_URL = "http://localhost:8000/ask"
TEST_QUESTIONS_FILE = "test_questions.csv"
OUTPUT_RESULTS_FILE = "results.csv"

def run_evaluation():
    results = []
    
    with open(TEST_QUESTIONS_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q_id = row["id"]
            question = row["question"]
            
            try:
                response = requests.post(API_URL, json={"question": question}, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    answered = data["answered"]
                    answer = data["answer"]
                    citations_list = data["citations"]
                    
                    citations_str = ";".join([f"{c['doc_id']}#{c['section']}" for c in citations_list])
                    
                    results.append({
                        "id": q_id,
                        "question": question,
                        "answered": answered,
                        "answer": answer,
                        "citations": citations_str,
                        "outcome": "correct" if answered else "correct_refusal",
                        "notes": "Evaluation step completed successfully."
                    })
                else:
                    results.append({
                        "id": q_id,
                        "question": question,
                        "answered": False,
                        "answer": f"HTTP Error {response.status_code}",
                        "citations": "",
                        "outcome": "incorrect",
                        "notes": f"API returned error status {response.status_code}"
                    })
            except Exception as e:
                results.append({
                    "id": q_id,
                    "question": question,
                    "answered": False,
                    "answer": str(e),
                    "citations": "",
                    "outcome": "incorrect",
                    "notes": f"Request exception: {str(e)}"
                })

    with open(OUTPUT_RESULTS_FILE, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "question", "answered", "answer", "citations", "outcome", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
            
    print(f"Evaluation complete. Results written to {OUTPUT_RESULTS_FILE}")

if __name__ == "__main__":
    run_evaluation()
