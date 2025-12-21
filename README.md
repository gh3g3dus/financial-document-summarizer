# Financial Document Summarizer & Insights Extractor

An AI-powered tool that processes public financial filings (10-K, 10-Q, earnings transcripts) to generate executive summaries, extract key metrics, and highlight risks — ideal for audit, compliance, and financial analysis workflows.

Built as a practical demonstration of generative AI skills from the **IBM AI Developer Professional Certificate**.

## Features
- Downloads and extracts clean text from SEC EDGAR HTML filings
- Intelligent text chunking for LLM processing
- (In progress) Generative AI summarization and insight extraction using OpenAI/Groq
- (Planned) Flask web interface for file upload and results display

## Tech Stack
- Python 3
- Requests + BeautifulSoup (HTML parsing)
- OpenAI API / Groq (generative AI)
- Flask (web framework)
- pdfplumber (fallback for PDF support)

## Quick Start
```bash
git clone https://github.com/yourusername/financial-document-summarizer.git
cd financial-document-summarizer
python -m venv venv
venv\Scripts\activate    # On Windows
# .\venv\Scripts\Activate.ps1 on PowerShell
pip install -r requirements.txt

# Extract text from a filing
python extract_text.py https://www.sec.gov/Archives/edgar/data/0001045810/000104581025000023/nvda-20250126.htm

# Chunk the extracted text
python chunk_text.py
