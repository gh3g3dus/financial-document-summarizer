def extract_insights(chunk_text, chunk_number):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON. No explanations, no code fences, no backticks, no markdown."},
                {"role": "user", "content": f"""From this 10-K section, extract in valid JSON only:
- "revenue": main revenue figures (with year/quarter if available)
- "net_income": net income or profit figures
- "eps": earnings per share (if mentioned)
- "risks": top 3 risks or challenges (list of strings)
- "outlook": 1-2 sentence strategic initiatives or outlook
Use "" or [] for missing items.

Text (first 2000 chars):
{chunk_text[:2000]}"""}
            ],
            temperature=0.3,
            max_tokens=300
        )
        raw = response.choices[0].message.content.strip()

        # Clean Markdown/code fences
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:].strip()
        if raw.startswith("```"):
            raw = raw[3:].strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        try:
            insights = json.loads(raw)
        except json.JSONDecodeError:
            insights = {"error": "JSON parse failed", "raw": raw}

        return f"Chunk {chunk_number}:\n{json.dumps(insights, indent=2)}\n"
    except Exception as e:
        return f"Chunk {chunk_number}: [Error - {str(e)}]\n"