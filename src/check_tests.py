import json
from collections import Counter
from pathlib import Path

data = json.loads(Path("tests/test_set.json").read_text(encoding="utf-8"))
print(len(data), "questions")
print(Counter(item["category"] for item in data))