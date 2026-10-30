import json

with open("outputs/results.json", encoding="utf-8") as f:
    data = json.load(f)

counts = {}

def walk(x):
    if isinstance(x, dict):
        if "source_file" in x:
            name = x["source_file"]
            counts[name] = counts.get(name, 0) + 1
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(data)
for name, n in sorted(counts.items()):
    print(n, "facts from", name)