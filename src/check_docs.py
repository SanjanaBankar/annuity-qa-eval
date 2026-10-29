from pathlib import Path

docs_dir = Path("data/policies")
for f in sorted(docs_dir.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    print(f"{f.name}: {len(text)} characters")