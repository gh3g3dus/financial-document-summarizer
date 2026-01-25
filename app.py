from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    insights = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                print("Running extraction...")
                subprocess.run(["python", "extract_text.py", url], check=True)

                print("Running summarization...")
                subprocess.run(["python", "summarize_chunks.py"], check=True)

                print("Running insights extraction...")
                subprocess.run(["python", "extract_insights.py"], check=True)   
                with open("full_summary.txt", "r", encoding="utf-8") as f:
                    summary = f.read()

                with open("insights.txt", "r", encoding="utf-8") as f:
                    insights = f.read()
            except subprocess.CalledProcessError as e:
                error = f"Processing failed (exit code {e.returncode}): {e.stderr.strip() or 'Unknown error'}"
            except FileNotFoundError as e:
                error = f"File not found: {str(e)} - Check if extraction completed."
            except Exception as e:
                error = f"Unexpected error: {str(e)}"

    return render_template("index.html", summary=summary, insights=insights, error=error)

if __name__ == "__main__":
    app.run(debug=True)