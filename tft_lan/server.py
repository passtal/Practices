"""TFT 시즌3 갤럭시 LAN - aiohttp 웹서버 + WebSocket"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json, time, copy, random, asyncio, socket
from aiohttp import web
import aiohttp

from config import *
from game import (
    create_player, init_unit_pool, generate_shop, return_shop_to_pool,
    get_board_units, calculate_synergies, count_board_units,
    buy_unit, sell_unit, place_unit, move_board_unit, remove_to_bench,
    refresh_shop, level_up, grant_round_income, grant_round_xp,
    equip_item, drop_items, offer_augments, apply_augment,
    simulate_combat, simulate_pve, pair_players, try_star_upgrade,
)

STATIC = os.path.join(os.path.dirname(__file__), "static")


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


# ======================================================================
#  GameServer
# ======================================================================

class GameServer:
    def __init__(self):
        self.players = {}
        self.websockets = {}
        self.unit_pool = init_unit_pool()
        self.round_num = 0
        self.phase = "waiting"
        self.host_id = None
        self.next_id = 0
        self.lock = asyncio.Lock()
        self.prep_task = None
        self.augment_choices = {}

    # ------ WebSocket handler ------
    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        pid = None
        try:
            async for raw in ws:
                if raw.type == aiohttp.WSMsgType.TEXT:
                    msg = json.loads(raw.data)
                    if msg.get("type") == "join" and pid is None:
                        pid = await self._register(ws, msg.get("name", "???"))
                        if pid is None:
                            await self._send(ws, {"type": "error", "msg": "서버 가득 참 또는 게임 진행 중"})
                            await ws.close()
                            return
                    elif pid is not None:
                        await self._handle(pid, msg)
                elif raw.type == aiohttp.WSMsgType.ERROR:
                    break
        finally:
            if pid is not None:
                await self._disconnect(pid)
        return ws

    async def _send(self, ws, msg):
        try:
            await ws.send_json(msg)
        except Exception:
            pass

    async def _broadcast(self, msg):
        for ws in list(self.websockets.values()):
            await self._send(ws, msg)

    # ------ 접속/해제 ------
    async def _register(self, ws, name):
        async with self.lock:
            if self.phase != "waiting" or len(self.players) >= MAX_PLAYERS:
                return None
            pid = self.next_id
            self.next_id += 1
            self.players[pid] = create_player(pid, name)
            self.websockets[pid] = ws
            if self.host_id is None:
                self.host_id = pid
        await self._send(ws, {"type": "welcome", "player_id": pid, "is_host": pid == self.host_id})
        await self._broadcast_lobby()
        print(f"[접속] {name} (ID:{pid})")
        return pid

    async def _disconnect(self, pid):
        async with self.lock:
            if pid in self.players:
                self.players[pid]["alive"] = False
                print(f"[연결 끊김] {self.players[pid]['name']}")
            self.websockets.pop(pid, None)

    # ------ 메시지 처리 ------
    async def _handle(self, pid, msg):
        t = msg.get("type")
        async with self.lock:
            player = self.players.get(pid)
            if not player:
                return

            if t == "start_game" and pid == self.host_id and self.phase == "waiting":
                if len(self.players) >= MIN_PLAYERS:
                    asyncio.create_task(self._game_loop())
                    return
                else:
                    await self._send(self.websockets[pid], {"type": "error", "msg": f"최소 {MIN_PLAYERS}명 필요"})
                    return

            if self.phase != "prep":
                if t == "select_augment":
                    await self._handle_augment(pid, msg)
                return

            if not player["alive"]:
                return

            ok, txt = False, ""
            if t == "buy":
                ok, txt = buy_unit(player, msg.get("index", -1), self.unit_pool)
            elif t == "sell":
                src = msg.get("source", "bench")
                if src == "bench":
                    ok, txt = sell_unit(player, "bench", msg.get("index", -1), self.unit_pool)
                else:
                    ok, txt = sell_unit(player, "board", (msg.get("row", -1), msg.get("col", -1)), self.unit_pool)
            elif t == "place":
                ok, txt = place_unit(player, msg.get("bench_index", -1), msg.get("row", -1), msg.get("col", -1))
            elif t == "move_board":
                ok, txt = move_board_unit(player, msg.get("fr", -1), msg.get("fc", -1), msg.get("tr", -1), msg.get("tc", -1))
            elif t == "remove":
                ok, txt = remove_to_bench(player, msg.get("row", -1), msg.get("col", -1))
            elif t == "refresh":
                ok, txt = refresh_shop(player, self.unit_pool)
            elif t == "level":
                ok, txt = level_up(player)
            elif t == "equip_item":
                ok, txt = equip_item(player, msg.get("item_idx", -1), msg.get("target_source", ""), msg.get("target_idx"))
            elif t == "ready":
                player["ready"] = True
                ok, txt = True, "준비 완료!"
            else:
                return

        ws = self.websockets.get(pid)
        if ws:
            await self._send(ws, {"type": "action_result", "success": ok, "msg": txt})
        if ok:
            await self._send_state(pid)

    async def _handle_augment(self, pid, msg):
        choice_idx = msg.get("index", -1)
        choices = self.augment_choices.get(pid)
        if not choices or choice_idx < 0 or choice_idx >= len(choices):
            return
        player = self.players[pid]
        apply_augment(player, choices[choice_idx])
        del self.augment_choices[pid]
        ws = self.websockets.get(pid)
        if ws:
            await self._send(ws, {"type": "augment_selected", "augment": choices[choice_idx]})
            await self._send_state(pid)

    # ------ 게임 루프 ------
    async def _game_loop(self):
        async with self.lock:
            self.phase = "prep"

        while True:
            self.round_num += 1
            print(f"\n=== 라운드 {self.round_num} ===")

            is_pve = self.round_num <= PVE_ROUNDS

            # 수입 & 경험치
            async with self.lock:
                alive = {pid: p for pid, p in self.players.items() if p["alive"]}
                if len(alive) <= 1 and self.round_num > PVE_ROUNDS:
                    break
                for pid, player in alive.items():
                    if self.round_num > 1:
                        grant_round_income(player, self.round_num)
                        grant_round_xp(player, self.round_num)
                    else:
                        player["gold"] = 3
                        player["level"] = 1
                    player["ready"] = False
                    return_shop_to_pool(player, self.unit_pool)
                    player["shop"] = generate_shop(player, self.unit_pool)
                    # 증강 라운드 무료 리프레시 재적용
                    for aug in player.get("augments", []):
                        eff = aug.get("effect", {})
                        if "free_refresh" in eff:
                            player["free_refreshes"] = eff["free_refresh"]

            # 증강 제안
            augment_offered = False
            if self.round_num in AUGMENT_ROUNDS:
                augment_offered = True
                async with self.lock:
                    for pid, player in alive.items():
                        choices = offer_augments(self.round_num)
                        if choices:
                            self.augment_choices[pid] = choices
                            ws = self.websockets.get(pid)
                            if ws:
                                await self._send(ws, {"type": "augment_offer", "choices": choices, "round": self.round_num})

            # 준비 단계
            async with self.lock:
                self.phase = "prep"
            phase_info = "PvE" if is_pve else "PvP"
            await self._broadcast({"type": "phase", "phase": "prep", "round": self.round_num, "info": phase_info})

            async with self.lock:
                for pid in [p for p, v in self.players.items() if v["alive"]]:
                    await self._send_state(pid)

            # 30초 타이머
            prep_start = time.time()
            while True:
                await asyncio.sleep(1)
                elapsed = time.time() - prep_start
                remaining = max(0, int(PREP_TIME - elapsed))
                await self._broadcast({"type": "timer", "remaining": remaining})
                async with self.lock:
                    alive = {pid: p for pid, p in self.players.items() if p["alive"]}
                    all_ready = all(p["ready"] for p in alive.values())
                if all_ready or elapsed >= PREP_TIME:
                    break

            # 전투 단계
            async with self.lock:
                self.phase = "combat"
                alive_ids = [pid for pid, p in self.players.items() if p["alive"]]
            await self._broadcast({"type": "phase", "phase": "combat", "round": self.round_num})

            if is_pve:
                # PvE 전투
                async with self.lock:
                    for pid in alive_ids:
                        player = self.players[pid]
                        won, dmg, events = simulate_pve(player, self.round_num)
                        if not won:
                            player["hp"] = max(0, player["hp"] - dmg)
                        items_dropped = drop_items(player, count=random.randint(1, 2))
                        events.append({"type": "info", "msg": f"아이템 획득: {', '.join(items_dropped)}"})
                        ws = self.websockets.get(pid)
                        if ws:
                            await self._send(ws, {"type": "combat_result", "opponent": "크리프",
                                                  "winner_id": pid if won else -1, "my_id": pid,
                                                  "damage": dmg, "events": events})
            else:
                # PvP 전투
                pairs = pair_players(alive_ids)
                for pid_a, pid_b, is_ghost in pairs:
                    async with self.lock:
                        pa = copy.deepcopy(self.players[pid_a])
                        pb = copy.deepcopy(self.players[pid_b])

                    winner_id, loser_id, damage, events = simulate_combat(pa, pb)

                    async with self.lock:
                        if is_ghost:
                            if loser_id == pid_a:
                                self.players[pid_a]["hp"] = max(0, self.players[pid_a]["hp"] - damage)
                                s = self.players[pid_a]["streak"]
                                self.players[pid_a]["streak"] = (s - 1) if s <= 0 else -1
                            elif winner_id == pid_a:
                                s = self.players[pid_a]["streak"]
                                self.players[pid_a]["streak"] = (s + 1) if s >= 0 else 1
                        else:
                            if loser_id is not None:
                                self.players[loser_id]["hp"] = max(0, self.players[loser_id]["hp"] - damage)
                            if winner_id is not None:
                                s = self.players[winner_id]["streak"]
                                self.players[winner_id]["streak"] = (s + 1) if s >= 0 else 1
                            if loser_id is not None:
                                s = self.players[loser_id]["streak"]
                                self.players[loser_id]["streak"] = (s - 1) if s <= 0 else -1

                    ghost_tag = " (유령)" if is_ghost else ""
                    send_to = [pid_a] if is_ghost else [pid_a, pid_b]
                    for pid in send_to:
                        opp = pid_b if pid == pid_a else pid_a
                        async with self.lock:
                            opp_name = self.players[opp]["name"] + ghost_tag
                        ws = self.websockets.get(pid)
                        if ws:
                            await self._send(ws, {
                                "type": "combat_result", "opponent": opp_name,
                                "winner_id": winner_id, "my_id": pid,
                                "damage": damage, "events": events,
                            })

            # 탈락 체크
            async with self.lock:
                for pid, player in self.players.items():
                    if player["hp"] <= 0 and player["alive"]:
                        player["alive"] = False
                        alive_count = sum(1 for p in self.players.values() if p["alive"])
                        ws = self.websockets.get(pid)
                        if ws:
                            await self._send(ws, {"type": "eliminated", "rank": alive_count + 1})
                        print(f"[탈락] {player['name']}")

            await self._broadcast_standings()
            await asyncio.sleep(4)

            async with self.lock:
                alive_count = sum(1 for p in self.players.values() if p["alive"])
            if alive_count <= 1:
                break

        # 게임 종료
        async with self.lock:
            self.phase = "game_over"
            alive = [p for p in self.players.values() if p["alive"]]
            winner = alive[0]["name"] if alive else "없음"
        await self._broadcast_standings()
        await self._broadcast({"type": "game_over", "winner": winner})
        print(f"\n{'='*50}\n  게임 종료! 승자: {winner}\n{'='*50}")

    # ------ 상태 전송 ------
    async def _send_state(self, pid):
        ws = self.websockets.get(pid)
        if not ws:
            return
        player = self.players[pid]
        board_units = get_board_units(player)
        synergies = calculate_synergies(board_units)
        opponents = []
        for opid, op in self.players.items():
            if opid != pid:
                opponents.append({"name": op["name"], "hp": op["hp"], "level": op["level"],
                                  "alive": op["alive"], "ready": op.get("ready", False)})
        await self._send(ws, {
            "type": "state", "player": player, "synergies": synergies,
            "opponents": opponents, "round": self.round_num,
        })

    async def _broadcast_lobby(self):
        players = [{"id": pid, "name": p["name"], "ready": p.get("ready", False)}
                   for pid, p in self.players.items()]
        await self._broadcast({
            "type": "lobby", "players": players, "count": len(self.players), "host_id": self.host_id,
        })

    async def _broadcast_standings(self):
        async with self.lock:
            standings = sorted(self.players.values(), key=lambda p: (-int(p["alive"]), -p["hp"]))
            data = [{"name": p["name"], "hp": p["hp"], "alive": p["alive"], "level": p["level"]}
                    for p in standings]
        await self._broadcast({"type": "standings", "standings": data})


# ======================================================================
#  HTTP 핸들러
# ======================================================================

async def handle_index(request):
    return web.FileResponse(os.path.join(STATIC, "index.html"))


# ======================================================================
#  서버 시작
# ======================================================================

def main():
    game = GameServer()
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/ws", game.ws_handler)
    app.router.add_static("/static", STATIC)

    host_ip = get_local_ip()
    print("=" * 55)
    print("  ⚔  TFT 시즌3 갤럭시 - LAN 오토배틀러  ⚔")
    print(f"  브라우저에서 접속: http://{host_ip}:{PORT}")
    print(f"  같은 PC:         http://localhost:{PORT}")
    print(f"  최대 {MAX_PLAYERS}명 대전 가능")
    print("=" * 55)
    web.run_app(app, host="0.0.0.0", port=PORT, print=None)


if __name__ == "__main__":
    main()
