import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_insights(chunk_text, chunk_number):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a financial analyst. Extract key insights from this 10-K section in JSON format."},
            {"role": "user", "content": f"""Extract the following in valid JSON only:
- "revenue": main revenue figures mentioned (with year if available)
- "net_income": net income or profit figures
- "risks": top 3 risks or challenges mentioned
- "outlook": strategic initiatives or outlook
Use "" for missing items.

Text:
{chunk_text}"""}
        ],
        temperature=0.3,
        max_tokens=300
    )
    return f"--- Chunk {chunk_number} Insights ---\n{response.choices[0].message.content.strip()}\n"

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

    max_chunks = 30  # Limit for speed
    chunks = chunks[:max_chunks]

    all_insights = []
    for i, chunk in enumerate(chunks):
        print(f"Extracting insights from chunk {i+1}...")
        insights = extract_insights(chunk, i+1)
        all_insights.append(insights)

    with open("insights.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_insights))

    print("Insights saved to insights.txt")