"""簡報檢查：每張投影片的數字都要出現在它引用的 Wiki 頁；引用頁必須存在；條件詞不可遺漏。
用法：python tools/check_slides.py
"""
import re, sys, pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "wiki").glob("*.md")}
doc = (ROOT / "slides" / "index.html").read_text(encoding="utf-8")
slides = re.findall(r'<section class="slide[^"]*" data-src="([^"]+)">(.*?)</section>', doc, re.S)
# 條件詞規則：出現左邊的關鍵字時，同一張投影片必須也出現右邊的條件詞（來自 run-01 檢查點 B 的教訓）
QUALIFIERS = {"30 日內": "扣除必要成本", "最長停 7 日": "每次", "3 萬元": "限期改正", "7 日內可以書面解除": "未使用"}
problems = []
for n, (src, raw) in enumerate(slides, 1):
    srcs = [s.strip() for s in src.split(",")]
    for s in srcs:
        if s not in PAGES:
            problems.append(f"第 {n} 張：引用頁 [[{s}]] 不存在")
    pool = " ".join(PAGES.get(s, "") for s in srcs)
    if "index" in srcs:  # 封面與回顧：可引用任何頁
        pool = " ".join(PAGES.values())
    text = re.sub(r"<p class=\"src\">.*?</p>|<div class=\"src\">.*?</div>", "", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text)
    for num in set(re.findall(r"\d+(?:\.\d+)?", text)):
        if num not in pool:
            problems.append(f"第 {n} 張：數字「{num}」不在 {srcs}")
    for key, need in QUALIFIERS.items():
        if key in text and need not in text:
            problems.append(f"第 {n} 張：出現「{key}」但缺少條件詞「{need}」")
    for link in re.findall(r'wiki/([^"/]+)\.md', raw):
        if link not in PAGES:
            problems.append(f"第 {n} 張：連結 wiki/{link}.md 不存在")
for p in problems: print("[問題]", p)
print(f"\n共 {len(slides)} 張投影片，{len(problems)} 個問題")
sys.exit(1 if problems else 0)
