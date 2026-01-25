import os
import time
from groq import Groq
from dotenv import load_dotenv
import json
import re  # for counting

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_insights(chunk_text, chunk_number):
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON. No explanations."},
                    {"role": "user", "content": f"""Extract in valid JSON only:
- "revenue": main revenue figures (with year/quarter)
- "net_income": net income/profit
- "eps": earnings per share
- "risks": top 3 risks (list of strings)
- "outlook": 1-2 sentence outlook
Use "" or [] for missing.

Text (first 2000 chars):
{chunk_text[:2000]}"""}
                ],
                temperature=0.3,
                max_tokens=300
            )
            raw = response.choices[0].message.content.strip()
            try:
                insights = json.loads(raw)
            except json.JSONDecodeError:
                insights = {"error": "JSON parse failed", "raw": raw}
            return f"Chunk {chunk_number}:\n{json.dumps(insights, indent=2)}\n"
        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                wait = 5 * (2 ** attempt)
                print(f"Rate limit on chunk {chunk_number} (attempt {attempt+1}/5). Wait {wait}s...")
                time.sleep(wait)
            else:
                print(f"Error on chunk {chunk_number}: {str(e)}")
                break
    return f"Chunk {chunk_number}: [Skipped - rate limit or error]\n"

if __name__ == "__main__":
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print("extracted_text.txt not found - run extract_text.py first!")
        exit(1)

    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap

    # Limit for live/demo (Render timeout)
    max_chunks = 20
    chunks = chunks[:max_chunks]

    print(f"Extracting insights from first {len(chunks)} chunks...\n")

    all_insights = []
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)}...")
        result = extract_insights(chunk, i+1)
        all_insights.append(result)

        # Save after each chunk
        with open("insights.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_insights))

    print("Insights saved to insights.txt")