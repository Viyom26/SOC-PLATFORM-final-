import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_log(log):
    prompt = f"""
You are a SOC security expert.

Analyze this log:
{log}

Give:
1. Threat explanation
2. Risk level
3. Recommended action
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def summarize_logs(logs):
    prompt = f"""
You are a SOC AI system.

Summarize these logs:
{logs[:20]}

Give:
- Overall threat level
- Key attack patterns
- Recommended action
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content