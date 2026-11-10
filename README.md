# 生成式 AI 作業簿

這學期生成式 AI 課程的作業作品集，一份作業一頁：從 Colab 函數圖形、DNN 手寫辨識，到 Prompt、Vibe Coding、對話機器人、RAG 和 AI Agent。

- 網站：https://elainechiu2005-collab.github.io/genai-portfolio/
- 專案規則：[AGENTS.md](AGENTS.md)（給 AI 開發助手看的規則，也適合人閱讀）

## 怎麼新增一份作業
1. 在 `data/works.json` 加一筆作業資料。
2. 複製 `templates/work-template.html` 到 `works/`，填寫五個固定區塊。
3. 截圖放進 `assets/img/`。

首頁的集點卡、作業清單與上一篇／下一篇會自動更新。詳細規則見 AGENTS.md 第 5 節。

## 本機預覽
```
python -m http.server
```
打開 http://localhost:8000
