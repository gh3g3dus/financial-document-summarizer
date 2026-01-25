import os
import time
from groq import Groq
from dotenv import load_dotenv
import re  # for counting existing chunks

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

    # === RESUME & BATCH CONTROL ===
    output_file = "full_summary.txt"

    # Load existing content and count chunks reliably
    existing_content = ""
    existing_chunk_count = 0
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            existing_content = f.read().strip()
        # Count existing summaries using regex
        matches = re.findall(r'--- Chunk \d+ Summary ---', existing_content)
        existing_chunk_count = len(matches)
        print(f"Detected {existing_chunk_count} existing chunks. Appending new ones...\n")

    # Starting chunk number (resume after existing)
    start_from_chunk = existing_chunk_count + 1

    # Slice chunks to start from resume point
    chunks = chunks[start_from_chunk - 1:]

    # Optional: Limit this run to X chunks (to avoid rate limits)
    max_batch_size = 30  # Change to 10, 20, 50, or None for all remaining
    if max_batch_size is not None:
        chunks = chunks[:max_batch_size]

    print(f"Resuming from chunk {start_from_chunk} → Processing {len(chunks)} chunks this run...\n")

    all_summaries = []

    # If we have existing content, start with it
    if existing_content:
        all_summaries.append(existing_content + "\n\n")

    # Process the batch
    for i in range(len(chunks)):
        chunk_number = start_from_chunk + i
        print(f"Processing chunk {chunk_number} (this run: {i+1}/{len(chunks)})...")
        summary = summarize_chunk(chunks[i], chunk_number)
        all_summaries.append(f"--- Chunk {chunk_number} Summary ---\n{summary}\n")

        # Save progressively after every chunk
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(all_summaries))

    print(f"\nBatch complete! Current progress saved to {output_file}")
    if len(chunks) > 0:
        next_start = start_from_chunk + len(chunks)
        print(f"Next batch: Update 'start_from_chunk' to {next_start} and rerun (or set max_batch_size = None for all remaining).")
    else:
        print("All chunks processed! Full summary complete.")