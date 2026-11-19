<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Disaster Relief Triage — Ramon Cortez, AI Architect</title>
<style>
  :root {
    --bg: #020617;
    --panel: #0f172a;
    --panel-2: #020617;
    --line: #1e293b;
    --line-2: #334155;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --dim: #64748b;
    --amber: #d97706;
    --amber-soft: #fbbf24;
    --red: #ef4444;
    --green: #10b981;
    --purple: #a855f7;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 1.5rem;
  }
  .wrap { max-width: 1280px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem; }
  .row { display: flex; align-items: center; gap: 0.75rem; }
  .between { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
  .card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1.25rem;
  }
  .label {
    font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: var(--muted);
  }
  .muted { color: var(--muted); }
  .dim { color: var(--dim); }

  /* header */
  header {
    display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
    gap: 1rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--line);
  }
  h1 { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.01em; display: flex; align-items: center; gap: 0.6rem; }
  h1 svg { width: 28px; height: 28px; color: var(--amber-soft); flex-shrink: 0; }
  .sub { color: var(--muted); font-size: 0.9rem; margin-top: 0.3rem; }
  .credit { color: var(--dim); font-size: 0.8rem; margin-top: 0.25rem; }
  .status-pill {
    display: flex; align-items: center; gap: 0.6rem;
    background: var(--panel); border: 1px solid var(--line);
    padding: 0.5rem 1rem; border-radius: 12px;
  }
  .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--amber); }
  .dot.live { background: var(--green); animation: ping 1.4s ease-in-out infinite; }
  .status-text { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--amber-soft); }
  .status-text.live { color: #34d399; }
  @keyframes ping { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

  /* banner */
  .banner {
    background: rgba(120, 53, 15, 0.25); border: 1px solid rgba(180, 83, 9, 0.5);
    border-radius: 12px; padding: 0.75rem 1rem; font-size: 0.8rem; color: #fcd34d;
  }

  /* input */
  .input-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }
  input[type="text"] {
    flex: 1; min-width: 240px;
    background: var(--panel-2); border: 1px solid var(--line); border-radius: 12px;
    padding: 0.85rem 1rem; font-size: 0.9rem; color: var(--text); font-family: inherit;
    outline: none; transition: border-color 0.2s;
  }
  input[type="text"]:focus { border-color: var(--amber); }
  input[type="text"]:disabled { opacity: 0.6; }
  .btn {
    border: none; border-radius: 12px; padding: 0.85rem 1.5rem;
    font-size: 0.9rem; font-weight: 600; font-family: inherit; color: #fff;
    background: var(--amber); cursor: pointer; transition: background 0.2s;
  }
  .btn:hover { background: #b45309; }
  .btn:disabled { opacity: 0.6; cursor: wait; }
  .presets { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.85rem; align-items: center; font-size: 0.8rem; }
  .chip {
    background: var(--line); color: #cbd5e1; border: 1px solid var(--line-2);
    border-radius: 8px; padding: 0.35rem 0.75rem; font-size: 0.78rem; font-family: inherit; cursor: pointer;
  }
  .chip:hover { background: var(--line-2); }
  .hint { font-size: 0.72rem; color: var(--dim); margin-top: 0.75rem; min-height: 1em; }

  /* stats */
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
  .stat { text-align: center; }
  .stat-num { font-size: 2rem; font-weight: 700; }
  .stat-label { font-size: 0.68rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.3rem; font-weight: 600; }

  /* filters */
  .filters { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
  .filter-group { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .filter {
    background: var(--line); color: #cbd5e1; border: 1px solid var(--line-2);
    border-radius: 12px; padding: 0.5rem 1rem; font-size: 0.78rem; font-weight: 600; font-family: inherit; cursor: pointer;
  }
  .filter.on { background: var(--amber); color: #fff; border-color: var(--amber); }

  /* main grid */
  .main { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .panel { height: 500px; display: flex; flex-direction: column; }
  .panel-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
  .badge { font-size: 0.72rem; color: var(--dim); background: var(--panel-2); border: 1px solid var(--line); border-radius: 8px; padding: 0.25rem 0.6rem; }
  .feed { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 0.75rem; padding-right: 0.25rem; }

  .req {
    background: rgba(2, 6, 23, 0.6); border: 1px solid var(--line);
    border-left: 4px solid var(--line-2); border-radius: 12px; padding: 0.85rem 1rem;
    animation: fadeIn 0.35s ease-out;
  }
  .req.critical { border-left-color: var(--red); }
  .req.high { border-left-color: var(--amber); }
  .req.routine { border-left-color: var(--green); }
  .req.review { border-left-color: var(--purple); }
  .req-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
  .req-loc { font-size: 0.8rem; font-weight: 600; color: #e2e8f0; }
  .tag { font-size: 0.65rem; font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.06em; border: 1px solid; }
  .tag.critical { color: #f87171; background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.35); }
  .tag.high { color: #fbbf24; background: rgba(245,158,11,0.15); border-color: rgba(245,158,11,0.35); }
  .tag.routine { color: #34d399; background: rgba(16,185,129,0.15); border-color: rgba(16,185,129,0.35); }
  .tag.review { color: #c084fc; background: rgba(168,85,247,0.15); border-color: rgba(168,85,247,0.35); }
  .req-msg { font-size: 0.8rem; font-style: italic; color: #cbd5e1; margin-bottom: 0.5rem; }
  .req-foot { display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--dim); }
  .req-foot strong { color: var(--muted); text-transform: uppercase; }
  .req-foot .route { color: var(--amber-soft); font-weight: 500; }

  /* map */
  .map {
    flex: 1; position: relative; border-radius: 12px; overflow: hidden; border: 1px solid var(--line);
    background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
  }
  .grid-lines {
    position: absolute; inset: 0; opacity: 0.35; pointer-events: none;
    background-image: linear-gradient(to right, #1e293b 1px, transparent 1px), linear-gradient(to bottom, #1e293b 1px, transparent 1px);
    background-size: 4rem 4rem;
  }
  .zone { position: absolute; font-size: 0.65rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; pointer-events: none; }
  .z1 { left: 1.5rem; top: 1.5rem; } .z2 { right: 1.5rem; top: 1.5rem; }
  .z3 { left: 1.5rem; bottom: 1.5rem; } .z4 { right: 1.5rem; bottom: 1.5rem; }
  .incident {
    position: absolute; width: 14px; height: 14px; border-radius: 50%;
    transform: translate(-50%, -50%); transition: all 0.5s; box-shadow: 0 0 10px currentColor;
  }
  .incident.critical { background: var(--red); color: var(--red); animation: pulseGlow 2s infinite; }
  .incident.high { background: var(--amber); color: var(--amber); }
  .incident.routine { background: var(--green); color: var(--green); }
  .incident.review { background: var(--purple); color: var(--purple); }

  /* teams */
  .teams { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
  .team { text-align: center; padding: 1rem; }
  .team-name { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); display: block; margin-bottom: 0.35rem; }
  .team-val { font-size: 1.1rem; font-weight: 700; }

  footer { text-align: center; color: var(--dim); font-size: 0.78rem; margin-top: 0.5rem; }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  @keyframes pulseGlow { 0%,100% { box-shadow: 0 0 0 rgba(239,68,68,0.4); } 50% { box-shadow: 0 0 15px rgba(239,68,68,0.9); } }

  @media (max-width: 900px) {
    .main { grid-template-columns: 1fr; }
    .stats, .teams { grid-template-columns: repeat(2, 1fr); }
  }
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div>
      <h1>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        Disaster Relief Triage &amp; Dispatch
      </h1>
      <p class="sub">Aid requests in, urgency scored, routed to the right team in seconds.</p>
      <p class="credit">Built by Ramon Cortez, AI Architect</p>
    </div>
    <div class="status-pill">
      <div id="statusDot" class="dot"></div>
      <span id="statusText" class="status-text">Local classifier</span>
    </div>
  </header>

  <div class="banner"><strong>Simulated data.</strong> All requests, names, and locations are mock examples for demonstration. No real incidents.</div>

  <div class="card">
    <div class="between" style="margin-bottom:0.75rem">
      <span class="label">Submit a dispatch request</span>
      <span style="font-size:0.72rem;color:var(--amber-soft)">Type a message or click a preset</span>
    </div>
    <div class="input-row">
      <input type="text" id="customInput" maxlength="300"
        placeholder="e.g. Elderly diabetic person trapped on 2nd floor, water rising fast near North District...">
      <button id="submitBtn" class="btn">Dispatch</button>
    </div>
    <div class="presets">
      <span class="dim" style="font-weight:500">Presets:</span>
      <button class="chip preset" data-text="Severe chest pain and difficulty breathing on 4th avenue">Medical Emergency</button>
      <button class="chip preset" data-text="Main water pipe burst flooding lower level apartments">Infrastructure Break</button>
      <button class="chip preset" data-text="Need blankets and warm shelter for 15 displaced children">Shelter Request</button>
    </div>
    <p id="inputNote" class="hint"></p>
    <div id="answer" style="display:none;margin-top:1rem;background:#070a14;border:1px solid #1e294b;border-left:4px solid #06b6d4;border-radius:10px;padding:1rem"></div>
  </div>

  <div class="card stats">
    <div class="stat"><div class="stat-num" id="sTotal">0</div><div class="stat-label">Total processed</div></div>
    <div class="stat"><div class="stat-num" id="sCritical" style="color:#f87171">0</div><div class="stat-label">Critical priority</div></div>
    <div class="stat"><div class="stat-num" id="sRouted" style="color:#34d399">0</div><div class="stat-label">Auto-routed</div></div>
    <div class="stat"><div class="stat-num" id="sReview" style="color:#c084fc">0</div><div class="stat-label">Human review</div></div>
  </div>

  <div class="card filters">
    <span class="label">Filter by urgency</span>
    <div class="filter-group">
      <button class="filter on" data-filter="all">All</button>
      <button class="filter" data-filter="critical">Critical</button>
      <button class="filter" data-filter="high">High</button>
      <button class="filter" data-filter="routine">Routine</button>
      <button class="filter" data-filter="review">Review</button>
    </div>
  </div>

  <div class="main">
    <div class="card panel">
      <div class="panel-head">
        <span class="label">Incoming feed</span>
        <span id="activeFilterBadge" class="badge">Showing: ALL</span>
      </div>
      <div class="feed" id="feed"></div>
    </div>

    <div class="card panel">
      <div class="panel-head">
        <span class="label">Priority map (simulated sectors)</span>
      </div>
      <div class="map" id="map">
        <div class="grid-lines"></div>
        <span class="zone z1">North District</span>
        <span class="zone z2">Riverside</span>
        <span class="zone z3">Harbor Sector</span>
        <span class="zone z4">Eastfield Zone</span>
      </div>
    </div>
  </div>

  <div class="teams">
    <div class="card team"><span class="team-name">Medical response</span><span class="team-val" id="tMedical">0 routed</span></div>
    <div class="card team"><span class="team-name">Water &amp; supplies</span><span class="team-val" id="tWater">0 routed</span></div>
    <div class="card team"><span class="team-name">Shelter operations</span><span class="team-val" id="tShelter">0 routed</span></div>
    <div class="card team"><span class="team-name">Power &amp; infra</span><span class="team-val" id="tPower">0 routed</span></div>
  </div>

  <footer>Simulated disaster response demo &bull; Ramon Cortez, AI Architect</footer>
</div>

<script>
  // Leave empty to run the local keyword classifier (no key, works offline).
  // Set to your backend URL (serverless function holding the Gemini key).
  // Expected: POST { text } -> JSON { loc, need, urgency, x, y }
  const TRIAGE_ENDPOINT = "";

  const LOCATIONS = ["North District", "Riverside", "Harbor Sector", "Eastfield Zone"];
  const NEEDS = ["medical", "water", "shelter", "power", "unclear"];
  const URGENCIES = ["critical", "high", "routine", "review"];
  const TEAM_IDS = { medical: "tMedical", water: "tWater", shelter: "tShelter", power: "tPower" };

  const SEEDS = [
    { loc: "North District", msg: "Mother and infant, no insulin left, water rising near the house", need: "medical", urgency: "critical", x: 25, y: 30 },
    { loc: "Riverside", msg: "Need drinking water for 6 people, roads closed", need: "water", urgency: "high", x: 70, y: 25 },
    { loc: "Harbor Sector", msg: "Elderly man on oxygen, power out since morning", need: "power", urgency: "critical", x: 30, y: 70 },
    { loc: "Eastfield Zone", msg: "Family displaced, need a safe place tonight", need: "shelter", urgency: "high", x: 75, y: 65 },
    { loc: "Riverside", msg: "any food or supplies available?", need: "unclear", urgency: "review", x: 60, y: 40 },
    { loc: "North District", msg: "Blankets delivered for the shelter at the school gym", need: "shelter", urgency: "routine", x: 35, y: 45 },
    { loc: "Harbor Sector", msg: "Cut on leg, bleeding slowed but needs a nurse", need: "medical", urgency: "high", x: 20, y: 80 },
    { loc: "Eastfield Zone", msg: "Phone battery dying, can we charge somewhere nearby", need: "power", urgency: "routine", x: 80, y: 50 }
  ];

  let requests = [];
  let currentFilter = "all";
  let streamIndex = 0;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function clamp(n, lo, hi, fallback) {
    const v = Number(n);
    return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : fallback;
  }

  function normalize(raw, msg) {
    return {
      loc: LOCATIONS.includes(raw.loc) ? raw.loc : "North District",
      msg: msg,
      need: NEEDS.includes(raw.need) ? raw.need : "unclear",
      urgency: URGENCIES.includes(raw.urgency) ? raw.urgency : "review",
      x: clamp(raw.x, 15, 85, 50),
      y: clamp(raw.y, 15, 85, 50)
    };
  }

  function localClassify(text) {
    const t = text.toLowerCase();
    let need = "unclear", urgency = "high";
    if (/insulin|oxygen|breath|chest|heart|bleed|trapped|diabetic|medication|nurse|medical/.test(t)) need = "medical";
    else if (/water|pipe|flood/.test(t)) need = "water";
    else if (/shelter|blanket|displaced|warm|children/.test(t)) need = "shelter";
    else if (/power|electric|battery|charge|line down/.test(t)) need = "power";

    if (/trapped|not breathing|severe|chest pain|bleeding|oxygen|insulin|rising fast/.test(t)) urgency = "critical";
    else if (text.trim().length < 15 || need === "unclear") urgency = "review";
    else if (/routine|delivered|donat/.test(t)) urgency = "routine";

    let loc = "North District";
    if (/riverside|river/.test(t)) loc = "Riverside";
    else if (/harbor|harbour|dock/.test(t)) loc = "Harbor Sector";
    else if (/eastfield|east/.test(t)) loc = "Eastfield Zone";

    return normalize({ loc, need, urgency, x: 15 + Math.random() * 70, y: 15 + Math.random() * 70 }, text);
  }

  async function classify(text) {
    if (!TRIAGE_ENDPOINT) return { result: localClassify(text), mode: "local" };
    try {
      const res = await fetch(TRIAGE_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      return { result: normalize(data, text), mode: "ai" };
    } catch (err) {
      return { result: localClassify(text), mode: "local-fallback" };
    }
  }

  function setStatus(mode) {
    const dot = document.getElementById("statusDot");
    const txt = document.getElementById("statusText");
    const live = mode === "ai";
    dot.className = "dot" + (live ? " live" : "");
    txt.className = "status-text" + (live ? " live" : "");
    txt.textContent = live ? "AI classifier connected" : "Local classifier (no AI key)";
    document.getElementById("inputNote").textContent = live
      ? "Requests are classified by the AI backend."
      : "Requests are classified by local keyword rules. Connect a backend endpoint to use AI.";
  }

  function render() {
    const feed = document.getElementById("feed");
    const map = document.getElementById("map");
    feed.innerHTML = "";
    map.querySelectorAll(".incident").forEach(d => d.remove());

    const counts = { total: requests.length, critical: 0, routed: 0, review: 0 };
    const teams = { medical: 0, water: 0, shelter: 0, power: 0 };

    requests.forEach(r => {
      if (r.urgency === "critical") counts.critical++;
      if (r.urgency === "review") counts.review++;
      else { counts.routed++; if (teams[r.need] !== undefined) teams[r.need]++; }
    });

    requests.forEach(r => {
      if (currentFilter !== "all" && r.urgency !== currentFilter) return;

      const card = document.createElement("div");
      card.className = "req " + r.urgency;
      card.innerHTML =
        '<div class="req-top"><span class="req-loc">' + esc(r.loc) + '</span>' +
        '<span class="tag ' + r.urgency + '">' + esc(r.urgency) + '</span></div>' +
        '<div class="req-msg">"' + esc(r.msg) + '"</div>' +
        '<div class="req-foot"><span>Need: <strong>' + esc(r.need) + '</strong></span>' +
        '<span class="route">' + (r.urgency === "review" ? "Queued for human review" : "Auto-routed") + '</span></div>';
      feed.appendChild(card);

      const dot = document.createElement("div");
      dot.className = "incident " + r.urgency;
      dot.style.left = r.x + "%";
      dot.style.top = r.y + "%";
      dot.title = r.loc + ": " + r.msg;
      map.appendChild(dot);
    });

    document.getElementById("sTotal").textContent = counts.total;
    document.getElementById("sCritical").textContent = counts.critical;
    document.getElementById("sRouted").textContent = counts.routed;
    document.getElementById("sReview").textContent = counts.review;
    Object.keys(TEAM_IDS).forEach(k => {
      document.getElementById(TEAM_IDS[k]).textContent = teams[k] + " routed";
    });
  }

  function add(r) {
    requests.unshift(r);
    if (requests.length > 60) requests.pop();
    render();
  }

  function setFilter(f) {
    currentFilter = f;
    document.querySelectorAll(".filter").forEach(b => b.classList.toggle("on", b.dataset.filter === f));
    document.getElementById("activeFilterBadge").textContent = "Showing: " + f.toUpperCase();
    render();
  }

  function showAnswer(r, mode) {
    const box = document.getElementById("answer");
    const team = r.urgency === "review" ? "Human review queue" : TEAM_NAMES[r.need];
    const label = URG_LABEL[r.urgency];
    box.style.display = "block";
    box.innerHTML =
      '<div class="label" style="margin-bottom:0.5rem">Dispatch answer</div>' +
      '<div style="font-size:0.95rem;margin-bottom:0.4rem"><b>Priority:</b> ' + esc(label) + '</div>' +
      '<div style="font-size:0.95rem;margin-bottom:0.4rem"><b>Routed to:</b> ' + esc(team) + '</div>' +
      '<div style="font-size:0.85rem;color:#8b9bb4;margin-bottom:0.4rem"><b>Location:</b> ' + esc(r.loc) + ' &middot; <b>Need:</b> ' + esc(r.need) + '</div>' +
      '<div style="font-size:0.75rem;color:#64748b">' + (mode === "ai" ? "Classified by AI backend" : "Classified by local rules (no AI key)") + '</div>';
  }

  async function submit() {
    const input = document.getElementById("customInput");
    const btn = document.getElementById("submitBtn");
    const note = document.getElementById("inputNote");
    const text = input.value.trim();

    if (!text) {
      note.textContent = "Type a request or click a preset first.";
      input.focus();
      return;
    }

    btn.disabled = true;
    btn.textContent = "Classifying...";
    note.textContent = "";

    const { result, mode } = await classify(text);
    setStatus(mode === "ai");
    add(result);
    showAnswer(result, mode);

    input.value = "";
    btn.disabled = false;
    btn.textContent = "Dispatch";
    input.focus();
  }

  function streamNext() {
    const seed = SEEDS[streamIndex % SEEDS.length];
    streamIndex++;
    add(Object.assign({}, seed));
    setTimeout(streamNext, 3500);
  }

  document.getElementById("submitBtn").addEventListener("click", submit);
  document.getElementById("customInput").addEventListener("keydown", e => { if (e.key === "Enter") submit(); });
  document.querySelectorAll(".preset").forEach(b => b.addEventListener("click", () => {
    const input = document.getElementById("customInput");
    input.value = b.dataset.text;
    document.getElementById("inputNote").textContent = "Preset loaded. Click Dispatch.";
    input.focus();
  }));
  document.querySelectorAll(".filter").forEach(b => b.addEventListener("click", () => setFilter(b.dataset.filter)));

  setStatus(TRIAGE_ENDPOINT ? "ai" : "local");
  SEEDS.slice(0, 3).reverse().forEach(s => requests.unshift(Object.assign({}, s)));
  streamIndex = 3;
  render();
  setTimeout(streamNext, 3500);
</script>
</body>
</html>
