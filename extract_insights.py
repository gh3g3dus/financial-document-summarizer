import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_insights(chunk_text, chunk_number):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON. No other text."},
                {"role": "user", "content": f"""From this 10-K section, extract:
- "revenue": main revenue figures (with year/quarter)
- "net_income": net income/profit
- "eps": earnings per share
- "risks": top 3 risks (list of strings)
- "outlook": 1-2 sentence strategic outlook
Use "" or [] for missing items.

Text:
{chunk_text[:2000]}"""}  # Limit text to avoid token overflow
            ],
            temperature=0.3,
            max_tokens=300
        )
        raw = response.choices[0].message.content.strip()
        try:
            insights = json.loads(raw)
        except:
            insights = {"error": "JSON parse failed", "raw": raw}
        return f"Chunk {chunk_number}:\n{json.dumps(insights, indent=2)}\n"
    except Exception as e:
        return f"Chunk {chunk_number}: Error - {str(e)}\n"

if __name__ == "__main__":
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except:
        print("Missing extracted_text.txt - run extract_text.py first!")
        exit()

    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap

    max_chunks = 30  # Same as your summary run
    chunks = chunks[:max_chunks]

    all_insights = []
    for i, chunk in enumerate(chunks):
        print(f"Extracting chunk {i+1}/{max_chunks}...")
        result = extract_insights(chunk, i+1)
        all_insights.append(result)

    with open("insights.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_insights))

    print("Done! Insights saved to insights.txt")