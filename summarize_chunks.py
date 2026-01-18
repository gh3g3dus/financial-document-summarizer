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
                print(f"Error on attempt {attempt+1}: {str(e)}")
                time.sleep(2 ** attempt)
    return "[Summary skipped due to persistent rate limit/error]"

def summarize_chunk(chunk_text, chunk_number):
    messages = [
        {"role": "system", "content": "You are a senior financial analyst. Summarize this 10-K section in 150–200 words, focusing on key business updates, financial performance, risks, and strategic outlook."},
        {"role": "user", "content": chunk_text}
    ]
    return call_groq_with_retry(messages)

if __name__ == "__main__":
    # Load the full extracted text
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print("Error: extracted_text.txt not found. Run extract_text.py first!")
        exit()

    # === CHUNKING LOGIC ===
    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap
    # =========================================

    # === LIMIT PROCESSING (optional - change number or comment out) ===
    max_chunks_to_process = 50  # Set to 30, 50, or None for all chunks
    if max_chunks_to_process is not None:
        chunks = chunks[:max_chunks_to_process]
    # =========================================

    print(f"Loaded {len(full_text):,} characters → {len(chunks)} chunks to process.\n")

    all_summaries = []

    # Load any existing summary (for resuming)
    output_file = "full_summary.txt"
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            existing = f.read().strip()
            if existing:
                all_summaries = existing.split("\n\n--- Chunk")  # rough split
                # Clean up the split (add back separator)
                all_summaries = [s.strip() for s in all_summaries if s.strip()]
                print(f"Loaded {len(all_summaries)} existing summaries. Resuming...\n")

    # Determine starting point (if resuming)
    start_index = len(all_summaries)
    print(f"Starting from chunk {start_index + 1}/{len(chunks)}\n")

    for i in range(start_index, len(chunks)):
        chunk_number = i + 1
        print(f"Processing chunk {chunk_number}/{len(chunks)}...")
        summary = summarize_chunk(chunks[i], chunk_number)
        all_summaries.append(f"--- Chunk {chunk_number} Summary ---\n{summary}\n")

        # Save progressively after every chunk
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(all_summaries))

    print(f"\nProcessing complete! Full summary saved to {output_file}")