import json
import subprocess
import sys

import ollama

import rag

MODEL = "llama3.2"


def run_zizmor(workflow_path):
    result = subprocess.run(
        ["zizmor", "--format", "json", workflow_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def explain(finding, workflow_text, notes):
    reference = "\n\n".join(note["text"] for note in notes)
    prompt = f"""You are a GitHub Actions security reviewer.
A static analysis tool reported this finding:

Rule: {finding["ident"]}
Description: {finding["desc"]}
Severity: {finding["determinations"]["severity"]}

Reference notes (trusted, use them as your only source of facts):
{reference}

Workflow under review:
{workflow_text}

In at most four sentences, explain the risk for this specific workflow
and recommend the fix described in the reference notes."""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


workflow = sys.argv[1]
findings = run_zizmor(workflow)

with open(workflow, encoding="utf-8") as f:
    workflow_text = f.read()

index, all_notes = rag.build_index()

for finding in findings:
    severity = finding["determinations"]["severity"]
    query = f"{finding['ident']}: {finding['desc']}"
    notes = rag.search(index, all_notes, query)

    print(f"[{severity}] {finding['ident']}: {finding['desc']}")
    print("Sources:", ", ".join(note["source"] for note in notes))
    print(explain(finding, workflow_text, notes))
    print()

blocking = [f for f in findings if f["determinations"]["severity"] == "High"]
if blocking:
    print(f"VERDICT: BLOCK ({len(blocking)} high severity findings)")
    sys.exit(1)
print("VERDICT: ALLOW")