/* ================================================================
   TFT 시즌3 갤럭시 — 프론트엔드 (game.js)
   ================================================================ */

(() => {
"use strict";

/* ---------- 상수 ---------- */
const BOARD_ROWS = 4, BOARD_COLS = 7, BENCH_SIZE = 9;

/* ---------- DOM 참조 ---------- */
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

const lobbyScreen   = $("#lobby-screen");
const gameScreen    = $("#game-screen");
const goScreen      = $("#gameover-screen");
const nameInput     = $("#name-input");
const joinBtn       = $("#join-btn");
const startBtn      = $("#start-btn");
const lobbyPlayers  = $("#lobby-players");
const lobbyMsg      = $("#lobby-msg");
const roundInfo     = $("#round-info");
const phaseInfo     = $("#phase-info");
const timerDisp     = $("#timer-display");
const myName        = $("#my-name");
const myHp          = $("#my-hp");
const myGold        = $("#my-gold");
const myLevel       = $("#my-level");
const myXp          = $("#my-xp");
const synergyList   = $("#synergy-list");
const standingsBar  = $("#standings-bar");
const boardEl       = $("#board");
const benchEl       = $("#bench");
const shopCards     = $("#shop-cards");
const refreshBtn    = $("#refresh-btn");
const levelBtn      = $("#level-btn");
const readyBtn      = $("#ready-btn");
const itemList      = $("#item-list");
const augmentList   = $("#augment-list");
const combatLog     = $("#combat-log");
const combatContent = $("#combat-log-content");
const augModal      = $("#augment-modal");
const augChoices    = $("#augment-choices");
const goTitle       = $("#go-title");
const goStandings   = $("#go-standings");

/* ---------- 상태 ---------- */
let ws = null;
let playerId = null;
let isHost = false;
let state = null;       // 서버에서 받은 전체 상태
let selectedItem = -1;  // 아이템 장착용 인덱스

// 드래그 관련
let dragging = null;      // { type:'bench'|'board', index/row,col, el }
let dragGhost = null;

/* =================================================================
   WebSocket 연결
   ================================================================= */
function connect(name) {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  ws = new WebSocket(`${proto}://${location.host}/ws`);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: "join", name }));
  };

  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    handleMessage(msg);
  };

  ws.onclose = () => {
    lobbyMsg.textContent = "서버 연결이 끊어졌습니다.";
  };
}

function send(obj) {
  if (ws && ws.readyState === 1) ws.send(JSON.stringify(obj));
}

/* =================================================================
   메시지 핸들러
   ================================================================= */
function handleMessage(msg) {
  switch (msg.type) {
    case "welcome":
      playerId = msg.player_id;
      isHost = msg.is_host;
      if (isHost) startBtn.classList.remove("hidden");
      break;

    case "lobby":
      renderLobby(msg);
      break;

    case "error":
      alert(msg.msg);
      break;

    case "phase":
      phaseInfo.textContent = msg.phase === "prep" ? `준비 (${msg.info})` : "전투 중";
      roundInfo.textContent = `라운드 ${msg.round}`;
      if (msg.phase === "prep") {
        combatLog.classList.add("hidden");
      }
      if (msg.phase === "combat") {
        combatContent.innerHTML = "";
      }
      showScreen("game");
      break;

    case "timer":
      timerDisp.textContent = msg.remaining;
      break;

    case "state":
      state = msg;
      renderGame();
      break;

    case "action_result":
      if (!msg.success) showToast(msg.msg);
      break;

    case "combat_result":
      showCombatResult(msg);
      break;

    case "standings":
      renderStandings(msg.standings);
      break;

    case "augment_offer":
      showAugmentModal(msg.choices);
      break;

    case "augment_selected":
      augModal.classList.add("hidden");
      break;

    case "eliminated":
      showToast(`탈락! 최종 순위: ${msg.rank}위`);
      break;

    case "game_over":
      showGameOver(msg);
      break;
  }
}

/* =================================================================
   화면 전환
   ================================================================= */
function showScreen(name) {
  lobbyScreen.classList.remove("active");
  gameScreen.classList.remove("active");
  goScreen.classList.remove("active");
  if (name === "lobby") lobbyScreen.classList.add("active");
  else if (name === "game") gameScreen.classList.add("active");
  else if (name === "gameover") goScreen.classList.add("active");
}

/* =================================================================
   로비 렌더링
   ================================================================= */
function renderLobby(msg) {
  lobbyPlayers.innerHTML = msg.players.map(p => {
    const hostTag = p.id === msg.host_id ? '<span class="host-tag">👑 방장</span>' : '';
    return `<div class="lp-row">${esc(p.name)}${hostTag}</div>`;
  }).join("");
  lobbyMsg.textContent = `${msg.count}명 접속 중`;
}

/* =================================================================
   게임 렌더링 (메인)
   ================================================================= */
function renderGame() {
  if (!state) return;
  const p = state.player;

  // 상단 바
  myName.textContent = p.name;
  myHp.textContent = `${p.hp} HP`;
  myGold.textContent = `${p.gold} G`;
  myLevel.textContent = `Lv.${p.level}`;
  myXp.textContent = `${p.xp}/${p.xp_to_level} XP`;
  roundInfo.textContent = `라운드 ${state.round}`;

  renderBoard(p);
  renderBench(p);
  renderShop(p);
  renderSynergies(state.synergies);
  renderItems(p);
  renderAugments(p);
  renderOpponents(state.opponents);
}

/* ---------- 보드 ---------- */
function renderBoard(p) {
  boardEl.innerHTML = "";
  for (let r = 0; r < BOARD_ROWS; r++) {
    for (let c = 0; c < BOARD_COLS; c++) {
      const cell = document.createElement("div");
      cell.className = "board-cell";
      cell.dataset.row = r;
      cell.dataset.col = c;
      const key = `${r},${c}`;
      const unit = p.board[key];
      if (unit) {
        cell.classList.add("has-unit");
        cell.appendChild(createUnitChip(unit));
        addDragSource(cell, "board", { row: r, col: c });
      }
      // 드롭 대상
      cell.addEventListener("dragover", ev => { ev.preventDefault(); cell.classList.add("drag-over"); });
      cell.addEventListener("dragleave", () => cell.classList.remove("drag-over"));
      cell.addEventListener("drop", ev => { ev.preventDefault(); cell.classList.remove("drag-over"); handleDrop("board", r, c); });
      // 아이템 장착 클릭
      cell.addEventListener("click", () => {
        if (selectedItem >= 0 && unit) {
          send({ type: "equip_item", item_idx: selectedItem, target_source: "board", target_idx: [r, c] });
          selectedItem = -1;
        }
      });
      boardEl.appendChild(cell);
    }
  }
}

/* ---------- 벤치 ---------- */
function renderBench(p) {
  benchEl.innerHTML = "";
  for (let i = 0; i < BENCH_SIZE; i++) {
    const cell = document.createElement("div");
    cell.className = "bench-cell";
    cell.dataset.idx = i;
    const unit = p.bench[i];
    if (unit) {
      cell.classList.add("has-unit");
      cell.appendChild(createUnitChip(unit));
      addDragSource(cell, "bench", { index: i });
    }
    cell.addEventListener("dragover", ev => { ev.preventDefault(); cell.classList.add("drag-over"); });
    cell.addEventListener("dragleave", () => cell.classList.remove("drag-over"));
    cell.addEventListener("drop", ev => { ev.preventDefault(); cell.classList.remove("drag-over"); handleDrop("bench_slot", i); });
    cell.addEventListener("click", () => {
      if (selectedItem >= 0 && unit) {
        send({ type: "equip_item", item_idx: selectedItem, target_source: "bench", target_idx: i });
        selectedItem = -1;
      }
    });
    benchEl.appendChild(cell);
  }
}

/* ---------- 유닛 칩 생성 ---------- */
function createUnitChip(unit) {
  const div = document.createElement("div");
  div.className = `unit-chip cost${unit.cost}`;
  div.setAttribute("draggable", "false"); // 부모 셀이 드래그
  const stars = "★".repeat(unit.star || 1);
  div.innerHTML = `<span class="star">${stars}</span>
    <span class="uname">${esc(unit.name)}</span>
    <div class="item-dots">${(unit.items||[]).map(()=>'<span class="item-dot"></span>').join("")}</div>`;
  // 툴팁 (hover)
  const traits = (unit.traits||[]).join(", ");
  const items = (unit.items||[]).join(", ");
  div.title = `${unit.name} ★${unit.star||1}\n비용: ${unit.cost}\nHP: ${unit.hp} AD: ${unit.ad}\n특성: ${traits}\n아이템: ${items||'없음'}`;
  return div;
}

/* ---------- 드래그 소스 ---------- */
function addDragSource(cell, srcType, srcData) {
  cell.setAttribute("draggable", "true");
  cell.addEventListener("dragstart", ev => {
    dragging = { type: srcType, ...srcData };
    ev.dataTransfer.effectAllowed = "move";
    cell.style.opacity = "0.4";
  });
  cell.addEventListener("dragend", () => {
    cell.style.opacity = "1";
    dragging = null;
  });
}

/* ---------- 드롭 처리 ---------- */
function handleDrop(destType, ...args) {
  if (!dragging) return;
  const src = dragging;

  if (src.type === "bench" && destType === "board") {
    // 벤치 → 보드 배치
    send({ type: "place", bench_index: src.index, row: args[0], col: args[1] });
  } else if (src.type === "board" && destType === "board") {
    // 보드 → 보드 이동
    send({ type: "move_board", fr: src.row, fc: src.col, tr: args[0], tc: args[1] });
  } else if (src.type === "board" && destType === "bench_slot") {
    // 보드 → 벤치 회수
    send({ type: "remove", row: src.row, col: src.col });
  }
  dragging = null;
}

/* ---------- 상점 ---------- */
function renderShop(p) {
  shopCards.innerHTML = "";
  const shop = p.shop || [];
  for (let i = 0; i < 5; i++) {
    const card = document.createElement("div");
    const champ = shop[i];
    if (champ) {
      card.className = `shop-card cost${champ.cost}`;
      card.innerHTML = `<span>${esc(champ.name)}</span><span class="sc-cost">${champ.cost} G</span>`;
      card.addEventListener("click", () => send({ type: "buy", index: i }));
    } else {
      card.className = "shop-card empty";
      card.innerHTML = `<span>—</span>`;
    }
    shopCards.appendChild(card);
  }
}

/* ---------- 시너지 ---------- */
function renderSynergies(synergies) {
  synergyList.innerHTML = "";
  if (!synergies) return;
  // synergies는 { 특성이름: { count, thresholds, active_level } } 형태
  const entries = Object.entries(synergies).sort((a,b) => b[1].count - a[1].count);
  for (const [name, info] of entries) {
    const div = document.createElement("div");
    const isActive = info.active_level > 0;
    div.className = `synergy-row${isActive ? " active-syn" : ""}`;
    const threshStr = (info.thresholds || []).map((t,i) => i < info.active_level ? `[${t}]` : t).join("/");
    div.textContent = `${isActive?"✦ ":""}${name} ${info.count} (${threshStr})`;
    synergyList.appendChild(div);
  }
}

/* ---------- 아이템 ---------- */
function renderItems(p) {
  itemList.innerHTML = "";
  const items = p.items || [];
  items.forEach((item, idx) => {
    const div = document.createElement("div");
    div.className = `item-row${selectedItem === idx ? " selected" : ""}`;
    div.textContent = item;
    div.addEventListener("click", () => {
      selectedItem = selectedItem === idx ? -1 : idx;
      renderItems(p);
    });
    itemList.appendChild(div);
  });
  if (items.length === 0) {
    itemList.innerHTML = '<div style="opacity:.4;font-size:11px">없음</div>';
  }
}

/* ---------- 증강 ---------- */
function renderAugments(p) {
  augmentList.innerHTML = "";
  const augs = p.augments || [];
  if (augs.length === 0) {
    augmentList.innerHTML = '<div style="opacity:.4;font-size:11px">없음</div>';
    return;
  }
  augs.forEach(aug => {
    const div = document.createElement("div");
    const tier = aug.tier || "silver";
    div.className = `aug-row aug-${tier}`;
    div.textContent = aug.name;
    div.title = aug.desc || "";
    augmentList.appendChild(div);
  });
}

/* ---------- 상대방 (순위바) ---------- */
function renderOpponents(opponents) {
  if (!opponents) return;
  standingsBar.innerHTML = "";
  opponents.forEach(op => {
    const chip = document.createElement("span");
    chip.className = `st-chip${op.alive ? "" : " dead"}`;
    chip.textContent = `${esc(op.name)} ${op.hp}HP Lv${op.level}${op.ready?" ✓":""}`;
    standingsBar.appendChild(chip);
  });
}

function renderStandings(standings) {
  if (!standings) return;
  standingsBar.innerHTML = "";
  standings.forEach(s => {
    const chip = document.createElement("span");
    chip.className = `st-chip${s.alive ? "" : " dead"}`;
    chip.textContent = `${esc(s.name)} ${s.hp}HP`;
    standingsBar.appendChild(chip);
  });
}

/* =================================================================
   전투 결과
   ================================================================= */
function showCombatResult(msg) {
  combatLog.classList.remove("hidden");
  const won = msg.winner_id === msg.my_id;
  let html = `<p style="font-weight:700;color:${won ? "var(--green)" : "var(--hp-red)"}">`;
  html += won ? `✓ 승리 vs ${esc(msg.opponent)}` : `✗ 패배 vs ${esc(msg.opponent)} (-${msg.damage} HP)`;
  html += "</p>";
  if (msg.events) {
    for (const e of msg.events.slice(-20)) {
      html += `<p>${esc(e.msg || JSON.stringify(e))}</p>`;
    }
  }
  combatContent.innerHTML = html;
}

/* =================================================================
   증강 모달
   ================================================================= */
function showAugmentModal(choices) {
  augChoices.innerHTML = "";
  choices.forEach((aug, idx) => {
    const card = document.createElement("div");
    const tier = aug.tier || "silver";
    card.className = `aug-card ${tier}`;
    card.innerHTML = `<h3>${esc(aug.name)}</h3><p>${esc(aug.desc || "")}</p><p style="margin-top:6px;color:var(--gold)">${tier.toUpperCase()}</p>`;
    card.addEventListener("click", () => {
      send({ type: "select_augment", index: idx });
      augModal.classList.add("hidden");
    });
    augChoices.appendChild(card);
  });
  augModal.classList.remove("hidden");
}

/* =================================================================
   게임 오버
   ================================================================= */
function showGameOver(msg) {
  goTitle.textContent = `🏆 승자: ${esc(msg.winner)}`;
  showScreen("gameover");
}

/* =================================================================
   유틸
   ================================================================= */
function esc(s) {
  if (!s) return '';
  const d = document.createElement("div");
  d.textContent = String(s);
  return d.innerHTML;
}

function showToast(msg) {
  const div = document.createElement("div");
  div.style.cssText = "position:fixed;top:50px;left:50%;transform:translateX(-50%);background:#333;color:#fff;padding:8px 18px;border-radius:8px;z-index:999;font-size:13px;";
  div.textContent = msg;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 2500);
}

/* =================================================================
   이벤트 바인딩
   ================================================================= */
joinBtn.addEventListener("click", () => {
  const name = nameInput.value.trim();
  if (!name) return alert("닉네임을 입력하세요");
  joinBtn.disabled = true;
  connect(name);
});

nameInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") joinBtn.click();
});

startBtn.addEventListener("click", () => send({ type: "start_game" }));
refreshBtn.addEventListener("click", () => send({ type: "refresh" }));
levelBtn.addEventListener("click", () => send({ type: "level" }));
readyBtn.addEventListener("click", () => send({ type: "ready" }));

// 벤치에서 우클릭 판매
benchEl.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  const cell = e.target.closest(".bench-cell");
  if (cell) send({ type: "sell", source: "bench", index: Number(cell.dataset.idx) });
});

// 보드에서 우클릭 판매
boardEl.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  const cell = e.target.closest(".board-cell");
  if (cell) send({ type: "sell", source: "board", row: Number(cell.dataset.row), col: Number(cell.dataset.col) });
});

// 초기 화면
showScreen("lobby");

})();
