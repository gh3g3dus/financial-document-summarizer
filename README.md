# Financial Document AI Summarizer

## Current Results (Jan 2026)
- Extracted & chunked NVIDIA 10-K filing
- AI-generated summaries for first **30 chunks** using Groq
- Clean executive overview: [executive_summary.md](executive_summary.md)
- Full raw summaries: [full_summary.txt](full_summary.txt)

Live web demo coming soon!

An AI-powered tool that processes public SEC EDGAR financial filings (10-Ks, etc.) to generate executive summaries and extract key insights — perfect for audit, compliance, and financial analysis.

Built using skills from the **IBM AI Developer Professional Certificate** (generative AI, prompt engineering, Python, Flask).

## Features (Current)
- Downloads and extracts clean text from SEC EDGAR HTML filings
- Intelligent chunking for large documents (e.g., 132 chunks from NVIDIA 10-K)
- Groq-powered AI summarization (Llama 3.3-70B) for fast, high-quality executive summaries
- Basic Flask web interface (in progress)

## Tech Stack
- Python 3
- Requests + BeautifulSoup (HTML extraction)
- Groq API (fast LLM inference)
- Flask (web framework)
- pdfplumber (PDF support – planned)

## Quick Start (Local)
```bash
git clone https://github.com/gh3g3dus/financial-document-summarizer.git
cd financial-document-summarizer
python -m venv venv
venv\Scripts\activate          # Windows CMD
pip install -r requirements.txt

# Extract text from a filing
python extract_text.py https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000023/nvda-20250126.htm

# Chunk and summarize (first 30 chunks demo)
python summarize_chunks.py