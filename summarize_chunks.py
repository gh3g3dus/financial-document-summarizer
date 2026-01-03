import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_chunk(chunk_text, chunk_number):
    """Send one chunk to Groq and get a summary"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Excellent balance of quality & speed
        messages=[
            {
                "role": "system",
                "content": "You are a senior financial analyst specializing in 10-K filings. Summarize the section concisely (150–250 words), highlighting key business updates, financial performance, risks, and strategic outlook."
            },
            {
                "role": "user",
                "content": chunk_text
            }
        ],
        temperature=0.5,
        max_tokens=500
    )
    summary = response.choices[0].message.content.strip()
    return f"--- Summary of Chunk {chunk_number} ---\n{summary}\n\n"

if __name__ == "__main__":
    # Load the full extracted text
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print("Error: extracted_text.txt not found. Run extract_text.py first!")
        exit()

    # Simple chunking (reuse logic from before)
    max_chars = 3000
    overlap = 200
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + max_chars
        chunks.append(full_text[start:end])
        start = end - overlap

    print(f"Loaded {len(chunks)} chunks. Summarizing the first 5 for preview...\n")

    all_summaries = []
    for i, chunk in enumerate(chunks[:5]):  # Start with first 5 chunks
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, i+1)
        all_summaries.append(summary)
        print(summary)

    # Save preview
    with open("summary_preview.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_summaries))
    
    print("Preview summaries saved to summary_preview.txt")
    print("Next step: Expand to all chunks and add insights extraction!")