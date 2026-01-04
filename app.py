from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        # Placeholder — we'll fill this in next steps
        summary = "AI summary will appear here after processing..."
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)