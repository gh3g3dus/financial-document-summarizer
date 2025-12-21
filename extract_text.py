import requests
from bs4 import BeautifulSoup
import sys
import os

def download_and_extract_html(url, output_file="extracted_text.txt"):
    # Download HTML
    headers = {"User-Agent": "Your Name your.email@example.com"}  # Required by SEC
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for errors
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, "lxml")
    
    # Remove scripts/styles (junk)
    for script in soup(["script", "style", "header", "footer"]):
        script.decompose()
    
    # Get text (preserves some structure)
    text = soup.get_text(separator="\n", strip=True)
    
    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Text extracted to {output_file}")
    print(f"First 500 characters:\n{text[:500]}")
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <edgar_htm_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    download_and_extract_html(url)