# Annuity & Loan Policy Q&A Bot: LLM Evaluation Harness

A retrieval-based Q&A bot over fake annuity and personal-loan policy documents, plus an automated pytest suite that measures how reliable its answers are.

The focus is **testing the LLM**, not building the bot: correctness, groundedness, hallucination, refusal of out-of-scope questions, and prompt-injection resistance, with measured before/after results when the prompt changes.

## What it tests

| Category | What a pass means |
|---|---|
| Answerable | Correct answer, supported by the documents |
| Unanswerable | Says the documents don't cover it; invents nothing |
| Out of scope | Politely declines (investing, tax advice, account access, unrelated topics) |
| Prompt injection | Ignores malicious instructions and stays in role |

Test questions live in `tests/test_set.json`, each with an expected answer and, where useful, strings the answer must contain.

## How it works

1. **Documents:** three fake policy files in `data/policies/` (annuity, loan, servicing FAQ).
2. **Bot (`src/bot.py`):** splits documents into sections, retrieves the most relevant ones by keyword, and sends them to an LLM with a system prompt.
3. **Tests (`tests/test_bot.py`):** pytest runs every question through the bot and applies checks:
   - exact-match checks for key facts
   - an LLM judge for correctness, groundedness (is every claim supported by the retrieved text?), admitting unknowns, refusal, and injection resistance
4. **Prompts:** `prompts/v1.txt` (baseline) and `prompts/v2.txt` (improved), compared on the same test set.
5. **Reports:** each run saves pass rates to `results/report_<version>.json`.

## Results

| Check | Prompt v1 | Prompt v2 |
|---|---|---|
| Overall pass rate | TBD | TBD |
| Answer correctness | TBD | TBD |
| Groundedness | TBD | TBD |
| Admits unknown (no hallucination) | TBD | TBD |
| Refuses out-of-scope | TBD | TBD |
| Resists prompt injection | TBD | TBD |

**What changed in v2:** TBD (for example: "answer only from the context", an explicit refusal rule, and an injection defense).

**Key findings:** TBD (for example: which failures came from retrieval and which from the LLM).

## Run it yourself

```bash
git clone https://github.com/YOUR-USERNAME/annuity-qa-eval.git
cd annuity-qa-eval
python -m venv .venv
.venv\Scripts\Activate.ps1      # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (free key from https://console.groq.com):

```
GROQ_API_KEY=your-key
MODEL_NAME=openai/gpt-oss-20b
```

Try the bot:

```bash
python src/bot.py
```

Run the evaluation for each prompt version:

```powershell
$env:PROMPT_VERSION="v1"; pytest -v
$env:PROMPT_VERSION="v2"; pytest -v
```

(Mac/Linux: `PROMPT_VERSION=v1 pytest -v`)

## Design decisions

- **Free LLM API (Groq):** the project is reproducible at no cost.
- **Response caching:** each question hits the API once per prompt version, so re-runs take seconds and API outages don't block testing.
- **`temperature=0`:** results are as repeatable as possible.
- **Simple keyword retrieval:** failures are easy to diagnose (is it retrieval or the LLM?).
- **Prompts live in files:** a prompt change needs no code change.
- **Custom LLM judge:** a small, transparent grader instead of a heavy framework. Frameworks like DeepEval or promptfoo implement the same metrics.

## Limitations

- Fake documents and a small hand-written test set, so pass rates are indicative, not statistically strong.
- LLM-judged checks can be wrong. TBD: note how many verdicts you spot-checked by hand.
- The same model family is used as bot and judge, which can bias results.
- Keyword retrieval can miss paraphrased questions.

## Project structure

```
data/policies/   fake policy documents
src/bot.py       retrieval + LLM bot
tests/           test set and pytest tests
prompts/         v1 (baseline) and v2 (improved)
results/         saved evaluation reports
```git add .