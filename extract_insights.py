import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_insights(chunk_text, chunk_number):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a financial analyst. Extract key insights from this 10-K section in valid JSON format only."},
            {"role": "user", "content": f"""Extract the following in valid JSON:
- "revenue": main revenue figures (with year/quarter if available)
- "net_income": net income or profit figures
- "eps": earnings per share (if mentioned)
- "risks": top 3 risks or challenges (as list of strings)
- "outlook": strategic initiatives or outlook (1-2 sentences)
Use "" or [] for missing items. Return ONLY JSON.

Text:
{chunk_text}"""}
        ],
        temperature=0.3,
        max_tokens=300
    )
    try:
        insights = json.loads(response.choices[0].message.content.strip())
    except:
        insights = {"error": "JSON parsing failed"}
    return f"--- Chunk {chunk_number} Insights ---\n{json.dumps(insights, indent=2)}\n"

if __name__ == "__main__":
    with open("extracted_text.txt", "r", encoding="utf-8") as f:
        full_text = f.read()

    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap

    max_chunks = 30  # Same limit as summaries
    chunks = chunks[:max_chunks]

    all_insights = []
    for i, chunk in enumerate(chunks):
        print(f"Extracting insights from chunk {i+1}...")
        insights = extract_insights(chunk, i+1)
        all_insights.append(insights)

    with open("insights.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_insights))

    print("Insights saved to insights.txt")