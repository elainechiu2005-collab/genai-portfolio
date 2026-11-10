/* =========================================================
   生成式 AI 作業簿｜全站共用程式
   - 所有作業的標題、摘要、標籤、連結都來自 data/works.json（唯一資料來源）
   - 首頁：<body data-page="home"> → 畫出集點卡與作業清單
   - 作業頁：<body data-page="work" data-work-id="w01"> → 畫出頁首資訊與上一篇／下一篇
   - data-root：從這一頁回到網站根目錄的相對路徑（首頁是 "."，works/ 底下是 ".."）
   ========================================================= */
(function () {
  const body = document.body;
  const root = body.dataset.root || ".";
  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const no = (n) => String(n).padStart(2, "0");
  const weekOf = (w) => w.week ?? w.order;            // 沒有 week 欄位時用 order
  const fmtDate = (d) => d ? d.replace(/^(\d{4})-(\d{2})-(\d{2})$/, (_, y, m, day) => `${+m}/${+day}`) : "";
  const tagsHTML = (tags) => tags && tags.length
    ? `<ul class="tags">${tags.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : "";

  function fail(where) {
    const el = $(where);
    if (el) el.innerHTML = `<p class="todo">讀不到作業資料（data/works.json）。請用 GitHub Pages 或本機伺服器開啟，直接雙擊 HTML 檔無法讀取。</p>`;
  }

  fetch(`${root}/data/works.json`)
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      const works = [...data.works].sort((a, b) => a.order - b.order);
      document.querySelectorAll("[data-site-title]").forEach((el) => (el.textContent = data.site.title));
      if (body.dataset.page === "home") renderHome(data.site, works);
      if (body.dataset.page === "work") renderWork(works, body.dataset.workId);
    })
    .catch(() => fail(body.dataset.page === "home" ? "#stampcard" : "#work-head"));

  /* ---------- 首頁 ---------- */
  function renderHome(site, works) {
    const done = works.filter((w) => w.status === "done");
    $("#hero-count").textContent = `已完成 ${done.length} 份作業`;
    const stamps = works.map((w) => `
      <a class="stamp ${w.status === "done" ? "done" : ""}" href="${root}/${esc(w.page)}">
        <span class="no">W${weekOf(w)}</span>
        <span class="t">${esc(w.title)}</span>
      </a>`).join("");
    const nextWeek = Math.max(...works.map(weekOf)) + 1;
    const next = `<div class="stamp next" aria-hidden="true"><span class="no">W${nextWeek}</span><span class="t">下一份作業</span></div>`;
    $("#stampcard").innerHTML = stamps + next;

    $("#worklist").innerHTML = works.map((w) => `
      <li>
        <span class="no">W${weekOf(w)}</span>
        <h3><a href="${root}/${esc(w.page)}">${esc(w.title)}</a></h3>
        <span class="proj">${esc(w.project)}｜${esc(w.type)}${w.due ? `｜期限 ${fmtDate(w.due)}` : ""}</span>
        <p>${esc(w.summary)}</p>
        ${tagsHTML(w.tags)}
      </li>`).join("");
  }

  /* ---------- 作業頁 ---------- */
  function renderWork(works, id) {
    const i = works.findIndex((w) => w.id === id);
    if (i < 0) return fail("#work-head");
    const w = works[i];
    document.title = `${w.title}｜生成式 AI 作業簿`;
    const links = (w.links || []).filter((l) => l.url);
    $("#work-head").innerHTML = `
      <p class="kicker">第 ${weekOf(w)} 週｜${esc(w.type)}</p>
      <h1>${esc(w.project)}</h1>
      <p class="summary">${esc(w.summary)}</p>
      <div class="meta"><span>題目：${esc(w.title)}</span>${w.due ? `<span>繳交期限：${fmtDate(w.due)}</span>` : ""}</div>
      ${tagsHTML(w.tags)}
      ${links.length ? `<div class="links">${links.map((l) =>
        `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`).join("")}</div>` : ""}`;

    const prev = works[i - 1], next = works[i + 1];
    $("#pager").innerHTML =
      (prev ? `<a class="prev" href="${root}/${esc(prev.page)}"><small>上一份</small>${esc(prev.project)}</a>` : "") +
      (next ? `<a class="next" href="${root}/${esc(next.page)}"><small>下一份</small>${esc(next.project)}</a>` : "");
  }
})();
