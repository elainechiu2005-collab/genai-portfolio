# 抽卡玩家權益 LLM Wiki

生成式 AI 課程第 10 週作業：用 LLM Wiki 做一份教學 HTML 簡報。

- **主題：** 抽卡玩家的消費權益（臺灣法規）
- **讀者：** 第一次課金、沒讀過法條的大學生
- **教學簡報：** [slides/index.html](slides/index.html)（線上版：https://elainechiu2005-collab.github.io/genai-portfolio/llm-wiki/slides/）

## 資料夾
| 位置 | 內容 |
|---|---|
| `SCHEMA.md` | 維護 Wiki 的規則（給 LLM 看） |
| `discussion.md` | 先討論、後生成的討論紀錄 |
| `raw/` | 8 份來源筆記（S1～S8），只新增不修改 |
| `wiki/` | 11 個頁面＋ `index.md` 目錄＋ `log.md` 操作紀錄 |
| `tools/` | `check_wiki.py`（lint）、`check_slides.py`（簡報事實檢查） |
| `runs/run-01/` | 一次實際執行的每一步輸出與檢查紀錄 |
| `loop-diagram.html` | 迴圈流程圖 |
| `slides/` | 教學 HTML 簡報 |

## 怎麼跑檢查
```bash
cd llm-wiki
python tools/check_wiki.py
python tools/check_slides.py
```

wiki 頁之間用 `[[頁面名]]` 連結（Obsidian 格式），在 GitHub 上會顯示成文字，請從 `wiki/index.md` 找頁面。

本 Wiki 與簡報只是學習整理，不是法律意見；實際爭議請洽 1950 或各縣市消保官。
