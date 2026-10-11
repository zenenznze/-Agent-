#!/usr/bin/env python3
"""Check task-owned handbook links and chapter registration; no external reads."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
names = [
    "00-心智模型.md", "01-开场五要素.md", "03-先对齐模型假设.md",
    "04-人类给什么-Agent查什么.md", "05-反馈与纠正.md", "06-验收条件怎么写.md",
    "07-并行与委派.md", "08-反模式清单.md", "09-模板库.md",
    "10-本次案例复盘.md", "17-复盘到实际修复.md", "18-长期积累与修订.md",
]
errors = []
for name in names:
    path = root / name
    body = path.read_text(encoding="utf-8")
    if not body.startswith("# "):
        errors.append(f"{name}: missing title")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
        target = target.split("#", 1)[0]
        if not target or "://" in target:
            continue
        destination = (path.parent / target).resolve()
        if not destination.is_relative_to(root) or not destination.exists():
            errors.append(f"{name}: invalid local link {target}")
readme = (root / "README.md").read_text(encoding="utf-8")
for name in names[-2:]:
    if f"({name})" not in readme:
        errors.append(f"README: unregistered chapter {name}")
for error in errors:
    print(error, file=sys.stderr)
print(f"Checked {len(names)} task-owned chapters; {len(errors)} errors. Semantic validity requires case review.")
raise SystemExit(bool(errors))
