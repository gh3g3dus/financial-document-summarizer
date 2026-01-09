import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq_with_retry(messages, max_retries=10):
    """Call Groq with exponential backoff for rate limits and other errors"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.5,
                max_tokens=400
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                wait_time = 5 * (2 ** attempt)  # 5s, 10s, 20s...
                print(f"Rate limit hit (attempt {attempt+1}/{max_retries}). Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Error on attempt {attempt+1}: {e}")
                time.sleep(2 ** attempt)
    return "[Summary skipped due to persistent rate limit/error]"

def summarize_chunk(chunk_text, chunk_number):
    messages = [
        {"role": "system", "content": "You are a senior financial analyst. Summarize this 10-K section in 150–200 words, focusing on key business updates, financial performance, risks, and strategic outlook."},
        {"role": "user", "content": chunk_text}
    ]
    return call_groq_with_retry(messages)

if __name__ == "__main__":
    # Load extracted text
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print("Error: extracted_text.txt not found. Run extract_text.py first!")
        exit()

    # === CHUNKING LOGIC (this was missing) ===
    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap
    
    max_chunks_to_process = 30  
    chunks = chunks[:max_chunks_to_process]  

    print(f"Limiting to first {len(chunks)} chunks for faster processing...\n")
    # =========================================

    print(f"Loaded {len(full_text):,} characters → {len(chunks)} chunks. Starting summarization...\n")

    all_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, i+1)
        all_summaries.append(f"--- Chunk {i+1} Summary ---\n{summary}\n\n")

    # Save full summary
    with open("full_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_summaries))

    print("\nAll done! Full AI-generated summary saved to full_summary.txt")