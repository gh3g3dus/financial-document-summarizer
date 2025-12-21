def chunk_text(text, max_chars=3000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
        if start < 0:
            start = 0
    return [c for c in chunks if c]  # Remove any empty chunks


if __name__ == "__main__":
    # Test the function with your extracted text
    try:
        with open("extracted_text.txt", "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print("Error: extracted_text.txt not found. Run extract_text.py first!")
        sys.exit(1)
    
    chunks = chunk_text(full_text)
    
    print(f"Successfully created {len(chunks)} chunks from {len(full_text):,} characters.")
    print("\n--- Preview of first 3 chunks ---")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1} ({len(chunk):,} characters):")
        print(chunk[:500] + "..." if len(chunk) > 500 else chunk)
    
    # Save chunks for later use (optional but helpful)
    for i, chunk in enumerate(chunks):
        with open(f"chunk_{i+1}.txt", "w", encoding="utf-8") as f:
            f.write(chunk)
    print(f"\nSaved {len(chunks)} chunk files (chunk_1.txt, chunk_2.txt, etc.).")