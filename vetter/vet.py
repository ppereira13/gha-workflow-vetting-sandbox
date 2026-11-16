import json
import subprocess
import sys

import ollama

MODEL = "llama3.2"


def run_zizmor(workflow_path):
    result = subprocess.run(
        ["zizmor", "--format", "json", workflow_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def explain(finding, workflow_text):
    prompt = f"""You are a GitHub Actions security reviewer.
A static analysis tool reported this finding:

Rule: {finding["ident"]}
Description: {finding["desc"]}
Severity: {finding["determinations"]["severity"]}

Workflow under review:
{workflow_text}

In at most four sentences, explain the risk for this specific workflow
and recommend a concrete fix."""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


workflow = sys.argv[1]
findings = run_zizmor(workflow)

with open(workflow, encoding="utf-8") as f:
    workflow_text = f.read()

for finding in findings:
    severity = finding["determinations"]["severity"]
    print(f"[{severity}] {finding['ident']}: {finding['desc']}")
    print(explain(finding, workflow_text))
    print()