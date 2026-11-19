"""Wiki lint：檢查來源標註、數字是否出自 raw、連結與孤兒頁。
用法：python tools/check_wiki.py   （在 llm-wiki/ 目錄下執行）
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = {p.name.split("-")[0]: p.read_text(encoding="utf-8") for p in (ROOT / "raw").glob("S*.md")}
PAGES = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "wiki").glob("*.md")}
SPECIAL = {"index", "log"}
NUM = re.compile(r"\d+(?:\.\d+)?")
SREF = re.compile(r"S(\d)")
LINK = re.compile(r"\[\[([^\]]+)\]\]")

def body(text):
    return text.split("---", 2)[2] if text.startswith("---") else text

def fm_sources(text):
    m = re.search(r"^sources:\s*\[(.*?)\]", text, re.M)
    return {s.strip() for s in m.group(1).split(",")} if m else set()

def is_fact(line):
    s = line.strip()
    if not s or s.startswith(("#", ">", "|---", "**白話")):
        return False
    if s.startswith("|") and ("來源" in s or "依據" in s or "條次" in s) and "S" not in s.replace("來源", ""):
        return False  # 表頭
    return s.startswith(("- ", "|")) or re.match(r"\d+\. ", s)

problems = []
def report(kind, page, msg):
    problems.append((kind, page, msg))

linked_from_index = set(LINK.findall(PAGES.get("index", "")))
for name, text in PAGES.items():
    if name in SPECIAL:
        continue
    b = body(text)
    links = LINK.findall(b)
    for l in links:
        if l not in PAGES:
            report("壞連結", name, f"[[{l}]] 不存在")
    if not links:
        report("沒有連結", name, "至少要連到 1 個其他頁")
    if name not in linked_from_index:
        report("孤兒頁", name, "index.md 沒有列出")
    used = {f"S{n}" for n in SREF.findall(b)}
    declared = fm_sources(text)
    if used - declared:
        report("frontmatter", name, f"內文用到 {sorted(used - declared)} 但 sources 沒寫")
    for line in b.splitlines():
        if not is_fact(line):
            continue
        refs = {f"S{n}" for n in SREF.findall(line)}
        if not refs and "推論" not in line and "待確認" not in line:
            report("缺來源", name, line.strip()[:60])
            continue
        pool = " ".join(RAW.get(r, "") for r in (refs or declared))
        for n in NUM.findall(re.sub(r"S\d|第 ?\d+ ?條(之 ?\d+)?|第 ?\d+ ?[項款]", "", line)):
            if n not in pool:
                report("數字不在來源", name, f"「{n}」不在 {sorted(refs or declared)}：{line.strip()[:50]}")

for kind, page, msg in problems:
    print(f"[{kind}] {page}: {msg}")
print(f"\n共 {len(PAGES) - len(SPECIAL)} 頁，{len(problems)} 個問題")
sys.exit(1 if problems else 0)
