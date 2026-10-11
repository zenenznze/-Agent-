#!/usr/bin/env python3
"""Read-only local-link/navigation/privacy checks; not semantic method verification."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
errors = []
files = sorted(root.rglob("*.md"))
readme = (root / "README.md").read_text()
for path in files:
    text = path.read_text()
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        rel, _, fragment = unquote(target.strip("<>")).partition("#")
        destination = path.parent / rel
        if not destination.is_file():
            errors.append(f"missing link: {path.relative_to(root)} -> {target}")
        elif fragment:
            headings = re.findall(r"^#+ (.+)$", destination.read_text(), re.M)
            anchors = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings]
            if fragment not in anchors:
                errors.append(f"missing anchor: {path.relative_to(root)} -> {target}")
    if re.search(r"/home/(?!<user>|user/)[^/\s]+/|/lzcapp/document/projects/|sk-[A-Za-z0-9]{16,}", text):
        errors.append(f"private path/token pattern: {path.relative_to(root)}")
    if path.parent == root and re.match(r"\d\d-", path.name) and path.name not in readme:
        errors.append(f"chapter not registered: {path.name}")
print(json.dumps({"result":"FAIL" if errors else "PASS","markdown_files":len(files),"errors":errors,"scope":"links/navigation/known privacy patterns; semantic validity not measured"},ensure_ascii=False))
sys.exit(bool(errors))
