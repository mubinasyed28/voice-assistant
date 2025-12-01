import openai, os, json, dateparser, re

openai.api_key = os.getenv("OPENAI_API_KEY")

def general_reply(text):
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":text}]
    )
    return res["choices"][0]["message"]["content"]

def extract_reminder_sync(text):
    prompt = f"""
Extract task, time, phone from this message.
Return only JSON like:
{{
 "task": "...",
 "time": "...",
 "phone": "..."
}}
Message: "{text}"
"""
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )

    content = res["choices"][0]["message"]["content"]
    try:
        json_str = re.search(r'\{.*\}', content, re.S).group(0)
        data = json.loads(json_str)
    except:
        data = {"task": text, "time": None, "phone": None}

    if data.get("time"):
        parsed = dateparser.parse(data["time"])
        data["time"] = parsed.isoformat() if parsed else None

    return data