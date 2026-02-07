# Financial Document AI Summarizer

An AI-powered web tool that analyzes SEC EDGAR financial filings (10-Ks, 10-Qs) by extracting text, chunking it, generating executive summaries, and extracting key insights using **Groq (Llama 3.3-70B)**.

Built as a portfolio project to demonstrate practical AI skills from the **IBM AI Developer Professional Certificate** (generative AI, prompt engineering, Python, Flask, deployment).

### Features
- Input any SEC EDGAR HTML filing URL
- Automatic text extraction (BeautifulSoup)
- Intelligent chunking for large documents
- Full AI summarization (132 chunks for NVIDIA 10-K example)
- Structured insights extraction (revenue, risks, outlook)
- Flask web interface with live demo on Render

### Live Demo
https://financial-summarizer-wfgq.onrender.com/

**Notes on free tier**:
- First load may take 30–60 seconds (Render spin-up)
- Processing limited to 20–30 chunks for speed due to rate limits
- Full 132-chunk analysis available locally

### Local Run Instructions
```bash
git clone https://github.com/gh3g3dus/financial-document-summarizer.git
cd financial-document-summarizer

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat   # Windows CMD

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py