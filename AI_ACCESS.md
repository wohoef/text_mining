# AI Access Instructions

Setup steps for calling Gemini through our shared Google Cloud project.

You're added to our shared Google Cloud project (`auc-text-mining-antithesis`) and can call Gemini directly. One-time setup:

## 1. Install the gcloud CLI
https://cloud.google.com/sdk/docs/install

## 2. Log in with the Gmail you sent Jonathan
```
gcloud auth login
```

## 3. Set up application default credentials (this is what Python uses)
```
gcloud auth application-default login
```

## 4. Point gcloud at our project
```
gcloud config set project auc-text-mining-antithesis
gcloud auth application-default set-quota-project auc-text-mining-antithesis
```

## 5. Install the Python SDK
```
pip install google-genai
```

## 6. Smoke test, run this in Python:
```python
from google import genai
client = genai.Client(
    vertexai=True,
    project="auc-text-mining-antithesis",
    location="europe-west4",
)
r = client.models.generate_content(
    model="gemini-3-flash",
    contents="Reply with exactly: HELLO",
)
print(r.text)
```

If it prints `HELLO`, you're set.

## Notes
- All calls bill against our shared 100 euro trial credits, so don't loop on huge inputs without telling the group.
- Use `gemini-3-flash` for bulk runs, `gemini-3-pro` only for prompt design / QC.
- Region is `europe-west4` (closest to NL).
- No API keys needed, auth is via your Google login.
