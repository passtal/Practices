"""TFT 시즌3 갤럭시 LAN - 게임 엔진 + 전투 시뮬레이션"""

import random, copy, math, time
from config import *
from data import (
    CHAMPIONS, CHAMP_BY_NAME, CHAMPS_BY_COST, TRAITS,
    ITEM_COMPONENTS, ITEM_COMP_BY_ID, COMBINED_ITEMS,
    AUGMENTS, PVE_WAVES,
)


# ======================================================================
#  유닛 생성
# ======================================================================

def create_unit(template, star=1):
    m = STAR_MULT.get(star, 1.0)
    return {
        "name": template["name"],
        "cost": template["cost"],
        "hp": int(template["hp"] * m),
        "max_hp": int(template["hp"] * m),
        "mana": 0,
        "max_mana": template["mana"],
        "ad": int(template["ad"] * m),
        "as": round(template["as"], 2),
        "range": template["range"],
        "armor": int(template["armor"] * m),
        "mr": int(template["mr"] * m),
        "traits": list(template["traits"]),
        "skill": template["skill"],
        "star": star,
        "items": [],
        "uid": f"{template['name']}_{star}_{random.randint(1000,9999)}",
    }


def create_player(pid, name):
    return {
        "id": pid,
        "name": name,
        "hp": STARTING_HP,
        "gold": STARTING_GOLD,
        "level": 1,
        "xp": 0,
        "streak": 0,
        "alive": True,
        "ready": False,
        "bench": [None] * BENCH_SIZE,
        "board": [[None] * BOARD_COLS for _ in range(BOARD_ROWS)],
        "shop": [],
        "item_inventory": [],
        "augments": [],
        "free_refreshes": 0,
    }


# ======================================================================
#  유닛 풀
# ======================================================================

def init_unit_pool():
    pool = {}
    for c in CHAMPIONS:
        pool[c["name"]] = POOL_SIZE.get(c["cost"], 10)
    return pool


# ======================================================================
#  상점
# ======================================================================

def generate_shop(player, pool):
    lv = min(player["level"], MAX_LEVEL)
    odds = SHOP_ODDS.get(lv, SHOP_ODDS[1])
    shop = []
    for _ in range(SHOP_SIZE):
        r = random.random()
        cum = 0
        cost = 1
        for idx, p in enumerate(odds):
            cum += p
            if r < cum:
                cost = idx + 1
                break
        avail = [c for c in CHAMPS_BY_COST.get(cost, []) if pool.get(c["name"], 0) > 0]
        if not avail:
            avail = [c for c in CHAMPIONS if pool.get(c["name"], 0) > 0]
        if not avail:
            shop.append(None)
            continue
        weights = [pool[c["name"]] for c in avail]
        chosen = random.choices(avail, weights=weights, k=1)[0]
        shop.append({"name": chosen["name"], "cost": chosen["cost"], "traits": list(chosen["traits"])})
    return shop


def return_shop_to_pool(player, pool):
    for item in player.get("shop", []):
        if item:
            pool[item["name"]] = pool.get(item["name"], 0) + 1


# ======================================================================
#  보드 유틸
# ======================================================================

def get_board_units(player):
    units = []
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if player["board"][r][c]:
                units.append(player["board"][r][c])
    return units


def count_board_units(player):
    return sum(1 for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if player["board"][r][c])


# ======================================================================
#  시너지 계산
# ======================================================================

def calculate_synergies(board_units):
    trait_counts = {}
    for u in board_units:
        for t in u["traits"]:
            trait_counts[t] = trait_counts.get(t, 0) + 1
    active = {}
    for trait, count in trait_counts.items():
        if trait not in TRAITS:
            continue
        syn = TRAITS[trait]
        tier = 0
        for i, th in enumerate(syn["thresholds"]):
            if count >= th:
                tier = i + 1
        if tier > 0:
            eff = syn["effects"][tier - 1]
            active[trait] = {
                "count": count,
                "tier": tier,
                "needed": syn["thresholds"][tier - 1],
                "desc": eff["desc"],
                "effect": eff,
            }
    return active


# ======================================================================
#  스타 합성
# ======================================================================

def try_star_upgrade(player, pool):
    upgraded = True
    while upgraded:
        upgraded = False
        locs = {}
        for i, u in enumerate(player["bench"]):
            if u:
                key = (u["name"], u["star"])
                locs.setdefault(key, []).append(("bench", i))
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                u = player["board"][r][c]
                if u:
                    key = (u["name"], u["star"])
                    locs.setdefault(key, []).append(("board", r, c))
        for (name, star), positions in locs.items():
            if len(positions) >= STAR_UPGRADE_COUNT and star < MAX_STARS:
                upgraded = True
                tmpl = CHAMP_BY_NAME[name]
                new_unit = create_unit(tmpl, star + 1)
                # 아이템 합치기
                all_items = []
                for pos in positions:
                    if pos[0] == "bench":
                        u = player["bench"][pos[1]]
                    else:
                        u = player["board"][pos[1]][pos[2]]
                    if u:
                        all_items.extend(u.get("items", []))
                new_unit["items"] = all_items[:MAX_ITEMS_PER_UNIT]
                board_locs = [p for p in positions if p[0] == "board"]
                bench_locs = [p for p in positions if p[0] == "bench"]
                keep = board_locs[0] if board_locs else bench_locs[0]
                removes = [p for p in positions if p != keep][:2]
                if keep[0] == "board":
                    player["board"][keep[1]][keep[2]] = new_unit
                else:
                    player["bench"][keep[1]] = new_unit
                for p in removes:
                    if p[0] == "board":
                        player["board"][p[1]][p[2]] = None
                    else:
                        player["bench"][p[1]] = None
                # 초과 아이템 인벤토리로
                for item in all_items[MAX_ITEMS_PER_UNIT:]:
                    player["item_inventory"].append(item)
                break


# ======================================================================
#  플레이어 액션
# ======================================================================

def buy_unit(player, shop_idx, pool):
    if shop_idx < 0 or shop_idx >= len(player["shop"]):
        return False, "잘못된 번호"
    item = player["shop"][shop_idx]
    if not item:
        return False, "이미 구매함"
    if player["gold"] < item["cost"]:
        return False, "골드 부족"
    slot = next((i for i in range(BENCH_SIZE) if player["bench"][i] is None), None)
    if slot is None:
        return False, "벤치 가득 참"
    player["gold"] -= item["cost"]
    tmpl = CHAMP_BY_NAME[item["name"]]
    player["bench"][slot] = create_unit(tmpl, 1)
    player["shop"][shop_idx] = None
    pool[item["name"]] = max(0, pool.get(item["name"], 0) - 1)
    try_star_upgrade(player, pool)
    return True, f"{item['name']} 구매"


def sell_unit(player, source, idx_or_rc, pool):
    """source='bench' idx=int, source='board' idx=(r,c)"""
    if source == "bench":
        u = player["bench"][idx_or_rc]
        if not u:
            return False, "빈 슬롯"
        player["gold"] += u["cost"] * u["star"]
        for it in u.get("items", []):
            player["item_inventory"].append(it)
        count = 3 ** (u["star"] - 1)
        pool[u["name"]] = pool.get(u["name"], 0) + count
        player["bench"][idx_or_rc] = None
        return True, f"{u['name']} 판매 (+{u['cost']*u['star']}G)"
    else:
        r, c = idx_or_rc
        if r < 0 or r >= BOARD_ROWS or c < 0 or c >= BOARD_COLS:
            return False, "잘못된 좌표"
        u = player["board"][r][c]
        if not u:
            return False, "빈 칸"
        player["gold"] += u["cost"] * u["star"]
        for it in u.get("items", []):
            player["item_inventory"].append(it)
        count = 3 ** (u["star"] - 1)
        pool[u["name"]] = pool.get(u["name"], 0) + count
        player["board"][r][c] = None
        return True, f"{u['name']} 판매 (+{u['cost']*u['star']}G)"


def place_unit(player, bench_idx, row, col):
    if bench_idx < 0 or bench_idx >= BENCH_SIZE:
        return False, "잘못된 벤치"
    if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
        return False, "잘못된 좌표"
    u = player["bench"][bench_idx]
    if not u:
        return False, "빈 벤치"
    existing = player["board"][row][col]
    if existing:
        player["board"][row][col] = u
        player["bench"][bench_idx] = existing
        return True, "교체 완료"
    cap = LEVEL_UNIT_CAP.get(player["level"], 9)
    if count_board_units(player) >= cap:
        return False, f"배치 한도 초과 (Lv{player['level']}: {cap})"
    player["board"][row][col] = u
    player["bench"][bench_idx] = None
    return True, "배치 완료"


def move_board_unit(player, fr, fc, tr, tc):
    if fr < 0 or fr >= BOARD_ROWS or fc < 0 or fc >= BOARD_COLS:
        return False, "잘못된 출발 좌표"
    if tr < 0 or tr >= BOARD_ROWS or tc < 0 or tc >= BOARD_COLS:
        return False, "잘못된 도착 좌표"
    src = player["board"][fr][fc]
    if not src:
        return False, "빈 칸"
    dst = player["board"][tr][tc]
    player["board"][tr][tc] = src
    player["board"][fr][fc] = dst
    return True, "이동 완료"


def remove_to_bench(player, row, col):
    if row < 0 or row >= BOARD_ROWS or col < 0 or col >= BOARD_COLS:
        return False, "잘못된 좌표"
    u = player["board"][row][col]
    if not u:
        return False, "빈 칸"
    slot = next((i for i in range(BENCH_SIZE) if player["bench"][i] is None), None)
    if slot is None:
        return False, "벤치 가득 참"
    player["bench"][slot] = u
    player["board"][row][col] = None
    return True, "벤치로 이동"


def refresh_shop(player, pool):
    cost = REFRESH_COST
    if player.get("free_refreshes", 0) > 0:
        cost = 0
        player["free_refreshes"] -= 1
    elif player["gold"] < REFRESH_COST:
        return False, "골드 부족"
    return_shop_to_pool(player, pool)
    if cost > 0:
        player["gold"] -= cost
    player["shop"] = generate_shop(player, pool)
    return True, "상점 갱신"


def level_up(player):
    if player["gold"] < LEVEL_UP_COST:
        return False, "골드 부족"
    if player["level"] >= MAX_LEVEL:
        return False, "최대 레벨"
    player["gold"] -= LEVEL_UP_COST
    player["xp"] += LEVEL_UP_XP
    nxt = player["level"] + 1
    if nxt <= MAX_LEVEL and player["xp"] >= LEVEL_XP_REQUIRED.get(nxt, 9999):
        player["level"] = nxt
        return True, f"레벨업! Lv.{nxt}"
    return True, f"경험치 +{LEVEL_UP_XP}"


def grant_round_income(player, rnd):
    base = calc_base_gold(rnd)
    interest = calc_interest(player["gold"])
    streak = calc_streak_gold(player["streak"])
    total = base + interest + streak
    player["gold"] += total
    return {"base": base, "interest": interest, "streak": streak, "total": total}


def grant_round_xp(player, rnd):
    if rnd >= 2 and player["level"] < MAX_LEVEL:
        player["xp"] += 2
        nxt = player["level"] + 1
        if player["xp"] >= LEVEL_XP_REQUIRED.get(nxt, 9999):
            player["level"] = nxt


def equip_item(player, item_idx, target_source, target_idx):
    """아이템 인벤토리에서 유닛에 장착"""
    if item_idx < 0 or item_idx >= len(player["item_inventory"]):
        return False, "잘못된 아이템"
    item = player["item_inventory"][item_idx]
    if target_source == "bench":
        u = player["bench"][target_idx]
    elif target_source == "board":
        r, c = target_idx
        u = player["board"][r][c]
    else:
        return False, "잘못된 대상"
    if not u:
        return False, "유닛 없음"
    if len(u["items"]) >= MAX_ITEMS_PER_UNIT:
        return False, "아이템 슬롯 가득 참"
    # 아이템 조합 체크
    comp_item = item
    if comp_item.get("type") == "component":
        # 기존 부품과 조합 시도
        for i, existing in enumerate(u["items"]):
            if existing.get("type") == "component":
                key = tuple(sorted([comp_item["id"], existing["id"]]))
                if key in COMBINED_ITEMS:
                    combined = COMBINED_ITEMS[key]
                    u["items"][i] = {"type": "combined", "name": combined["name"],
                                     "stats": combined["stats"], "effect": combined["effect"]}
                    player["item_inventory"].pop(item_idx)
                    return True, f"{combined['name']} 조합 완성!"
        # 조합 불가 → 부품 그대로 장착
    u["items"].append(item)
    player["item_inventory"].pop(item_idx)
    return True, f"아이템 장착"


def drop_items(player, count=1):
    """PvE 보상: 아이템 부품 드랍"""
    drops = []
    for _ in range(count):
        comp = random.choice(ITEM_COMPONENTS)
        item = {"type": "component", "id": comp["id"], "name": comp["name"], "stats": dict(comp["stats"])}
        player["item_inventory"].append(item)
        drops.append(comp["name"])
    return drops


# ======================================================================
#  증강 선택
# ======================================================================

def offer_augments(round_num):
    if round_num == AUGMENT_ROUNDS[0]:
        tier = "silver"
    elif round_num == AUGMENT_ROUNDS[1]:
        tier = "gold"
    elif round_num == AUGMENT_ROUNDS[2]:
        tier = "prismatic"
    else:
        return None
    pool = list(AUGMENTS[tier])
    random.shuffle(pool)
    return pool[:3]


def apply_augment(player, augment):
    player["augments"].append(augment)
    eff = augment["effect"]
    if "gold" in eff:
        player["gold"] += eff["gold"]
    if "free_refresh" in eff:
        player["free_refreshes"] += eff["free_refresh"]
    if "free_xp" in eff:
        player["xp"] += eff["free_xp"]


# ======================================================================
#  전투 시뮬레이션
# ======================================================================

def _dist(a, b):
    return max(abs(a["row"] - b["row"]), abs(a["col"] - b["col"]))


def _apply_item_stats(cu, unit):
    for item in unit.get("items", []):
        stats = item.get("stats", {})
        cu["ad"] += stats.get("ad", 0)
        cu["as"] += stats.get("as", 0)
        cu["sp"] += stats.get("sp", 0)
        cu["armor"] += stats.get("armor", 0)
        cu["mr"] += stats.get("mr", 0)
        cu["hp"] += stats.get("hp", 0)
        cu["max_hp"] += stats.get("hp", 0)
        cu["max_mana"] += stats.get("mana", 0)  # mana는 음수=마나 감소
        cu["crit"] += stats.get("crit", 0)
        has_ga = any(i.get("name") == "수호 천사" for i in unit.get("items", []))
        if has_ga:
            cu["guardian_angel"] = True


def _make_combat_unit(unit, owner, team, row, col):
    cu = {
        "name": unit["name"], "owner": owner, "team": team,
        "hp": unit["hp"], "max_hp": unit["hp"],
        "mana": 0, "max_mana": max(10, unit.get("max_mana", unit.get("mana", 80))),
        "ad": unit["ad"], "as": unit["as"], "sp": 0,
        "range": unit["range"], "armor": unit["armor"], "mr": unit["mr"],
        "crit": 0.25, "traits": list(unit["traits"]),
        "skill": unit.get("skill"), "star": unit.get("star", 1),
        "items": unit.get("items", []),
        "row": row, "col": col,
        "shield": 0, "stunned": 0, "attack_count": 0,
        "guardian_angel": False, "ga_used": False,
        "action_cd": 0, "dead": False,
    }
    _apply_item_stats(cu, unit)
    cu["max_mana"] = max(10, cu["max_mana"])
    return cu


def _find_target(cu, enemies):
    alive = [e for e in enemies if not e["dead"]]
    if not alive:
        return None
    return min(alive, key=lambda e: _dist(cu, e))


def _calc_damage(attacker, defender, base_dmg, is_spell=False):
    if is_spell:
        raw = base_dmg + attacker["sp"] * 0.5
        resist = defender["mr"]
    else:
        raw = base_dmg
        resist = defender["armor"]
    reduction = resist / (resist + 100) if resist > 0 else 0
    return max(1, int(raw * (1 - reduction)))


def _deal_damage(attacker, defender, amount, events, is_spell=False):
    absorbed = min(defender["shield"], amount)
    defender["shield"] -= absorbed
    actual = amount - absorbed
    defender["hp"] -= actual
    if defender["hp"] <= 0:
        if defender.get("guardian_angel") and not defender.get("ga_used"):
            defender["hp"] = 500
            defender["ga_used"] = True
            events.append({"type": "revive", "unit": defender["name"], "owner": defender["owner"]})
        else:
            defender["dead"] = True
            events.append({
                "type": "kill", "killer": attacker["name"], "killer_owner": attacker["owner"],
                "victim": defender["name"], "victim_owner": defender["owner"],
                "k_star": attacker["star"], "v_star": defender["star"],
            })
    return actual


def _move_toward(cu, target, all_units):
    dr = 0 if target["row"] == cu["row"] else (1 if target["row"] > cu["row"] else -1)
    dc = 0 if target["col"] == cu["col"] else (1 if target["col"] > cu["col"] else -1)
    occupied = {(u["row"], u["col"]) for u in all_units if not u["dead"] and u is not cu}
    for ddr, ddc in [(dr, dc), (dr, 0), (0, dc)]:
        if ddr == 0 and ddc == 0:
            continue
        nr, nc = cu["row"] + ddr, cu["col"] + ddc
        if 0 <= nr < BOARD_ROWS * 2 and 0 <= nc < BOARD_COLS and (nr, nc) not in occupied:
            cu["row"], cu["col"] = nr, nc
            return


def _cast_skill(cu, enemies, allies, events):
    skill = cu.get("skill")
    if not skill:
        return
    params = skill.get("params", {})
    s_type = skill.get("type", "dmg_single")
    base_dmg = params.get("damage", 0)

    alive_enemies = [e for e in enemies if not e["dead"]]
    if not alive_enemies:
        return

    events.append({"type": "cast", "unit": cu["name"], "owner": cu["owner"],
                    "skill": skill["name"], "star": cu["star"]})

    if s_type == "dmg_single":
        tgt_type = params.get("target", "nearest")
        if tgt_type == "farthest":
            target = max(alive_enemies, key=lambda e: _dist(cu, e))
        else:
            target = min(alive_enemies, key=lambda e: _dist(cu, e))
        dmg = _calc_damage(cu, target, base_dmg, is_spell=True)
        _deal_damage(cu, target, dmg, events, is_spell=True)

    elif s_type == "dmg_aoe":
        radius = params.get("radius", 2)
        target = min(alive_enemies, key=lambda e: _dist(cu, e))
        targets = [e for e in alive_enemies if _dist(target, e) <= radius][:6]
        for t in targets:
            dmg = _calc_damage(cu, t, base_dmg, is_spell=True)
            _deal_damage(cu, t, dmg, events, is_spell=True)

    elif s_type == "cc":
        dur = params.get("cc_dur", 1.5)
        tgt_type = params.get("target", "nearest")
        if tgt_type == "farthest":
            target = max(alive_enemies, key=lambda e: _dist(cu, e))
        else:
            target = min(alive_enemies, key=lambda e: _dist(cu, e))
        radius = params.get("radius", 0)
        targets_list = [target]
        if radius > 0:
            targets_list = [e for e in alive_enemies if _dist(target, e) <= radius][:4]
        for t in targets_list:
            dmg = _calc_damage(cu, t, base_dmg, is_spell=True)
            _deal_damage(cu, t, dmg, events, is_spell=True)
            t["stunned"] = max(t["stunned"], int(dur * 10))

    elif s_type == "buff":
        shield_amt = params.get("shield", 0)
        if shield_amt:
            cu["shield"] += int(shield_amt * STAR_MULT.get(cu["star"], 1))
        as_buff = params.get("as_buff", 0)
        if as_buff:
            cu["as"] += as_buff
        armor_buff = params.get("armor_buff", 0)
        if armor_buff:
            cu["armor"] += armor_buff
        dur = params.get("duration", 3)
        dmg_red = params.get("damage_reduction", 0)
        if dmg_red:
            cu["armor"] += int(dmg_red * 200)

    elif s_type == "heal":
        heal_amt = int(params.get("heal", 0) * STAR_MULT.get(cu["star"], 1))
        tgt = params.get("target", "self")
        if tgt == "all_allies":
            alive_allies = [a for a in allies if not a["dead"]]
            for a in alive_allies:
                a["hp"] = min(a["max_hp"], a["hp"] + heal_amt)
        else:
            cu["hp"] = min(cu["max_hp"], cu["hp"] + heal_amt)

    elif s_type == "special":
        if params.get("bonus_damage"):
            cu["ad"] += params["bonus_damage"]
        if params.get("as_buff"):
            cu["as"] += params["as_buff"]
        if params.get("4th_shot_mult"):
            pass  # Jhin passive handled in attack logic
        if params.get("summon"):
            pass  # Thresh summon - simplified
        if params.get("aoe_attacks"):
            cu["aoe_attacks"] = True
        heal = params.get("heal_on_kill", 0)
        if heal:
            cu["heal_on_kill"] = heal


def _apply_synergy_buffs(team, synergies):
    for cu in team:
        for trait, info in synergies.items():
            eff = info["effect"]
            # 선봉대
            if "armor" in eff and trait == "선봉대":
                if "선봉대" in cu["traits"]:
                    cu["armor"] += eff["armor"]
            # 투사
            if "hp" in eff and trait == "투사":
                if "투사" in cu["traits"]:
                    cu["hp"] += eff["hp"]
                    cu["max_hp"] += eff["hp"]
            # 마법사
            if "sp_pct" in eff:
                cu["sp"] += int(cu["sp"] * eff["sp_pct"]) + int(eff["sp_pct"] * 50)
            # 신비술사
            if "mr" in eff and trait == "신비술사":
                cu["mr"] += eff["mr"]
            # 반군
            if "shield" in eff and trait == "반군":
                if "반군" in cu["traits"]:
                    cu["shield"] += eff["shield"]
            # 사이버네틱
            if trait == "사이버네틱" and eff.get("requires_item"):
                if "사이버네틱" in cu["traits"] and cu["items"]:
                    cu["hp"] += eff.get("hp", 0)
                    cu["max_hp"] += eff.get("hp", 0)
                    cu["ad"] += eff.get("ad", 0)
            # 잠입자
            if trait == "잠입자" and eff.get("as_buff"):
                if "잠입자" in cu["traits"]:
                    cu["as"] += eff["as_buff"]


def simulate_combat(player_a, player_b):
    """전투 시뮬레이션. Returns (winner_id, loser_id, damage, events)"""
    a_units = get_board_units(player_a)
    b_units = get_board_units(player_b)

    if not a_units and not b_units:
        return None, None, 0, [{"type": "info", "msg": "양쪽 유닛 없음 - 무승부"}]
    if not a_units:
        dmg = sum(u.get("star", 1) for u in b_units) + player_b["level"]
        return player_b["id"], player_a["id"], dmg, [{"type": "info", "msg": f"{player_a['name']} 보드 비어있음"}]
    if not b_units:
        dmg = sum(u.get("star", 1) for u in a_units) + player_a["level"]
        return player_a["id"], player_b["id"], dmg, [{"type": "info", "msg": f"{player_b['name']} 보드 비어있음"}]

    syn_a = calculate_synergies(a_units)
    syn_b = calculate_synergies(b_units)

    team_a = []
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            u = player_a["board"][r][c]
            if u:
                team_a.append(_make_combat_unit(u, player_a["name"], "a", BOARD_ROWS - 1 - r, c))
    team_b = []
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            u = player_b["board"][r][c]
            if u:
                team_b.append(_make_combat_unit(u, player_b["name"], "b", BOARD_ROWS + r, c))

    _apply_synergy_buffs(team_a, syn_a)
    _apply_synergy_buffs(team_b, syn_b)

    # 잠입자 점프
    all_combat = team_a + team_b
    for cu in all_combat:
        if "잠입자" not in cu["traits"]:
            continue
        enemies = team_b if cu["team"] == "a" else team_a
        alive_enemies = [e for e in enemies if not e["dead"]]
        if not alive_enemies:
            continue
        farthest = max(alive_enemies, key=lambda e: e["row"]) if cu["team"] == "a" else min(alive_enemies, key=lambda e: e["row"])
        occupied = {(u["row"], u["col"]) for u in all_combat if not u["dead"]}
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = farthest["row"] + dr, farthest["col"] + dc
                if 0 <= nr < BOARD_ROWS * 2 and 0 <= nc < BOARD_COLS and (nr, nc) not in occupied:
                    cu["row"], cu["col"] = nr, nc
                    break
            else:
                continue
            break

    events = []
    for tick in range(600):
        alive_a = [u for u in team_a if not u["dead"]]
        alive_b = [u for u in team_b if not u["dead"]]
        if not alive_a or not alive_b:
            break

        all_alive = alive_a + alive_b
        for u in all_alive:
            if u["stunned"] > 0:
                u["stunned"] -= 1
                continue
            u["action_cd"] -= 1

        ready = [u for u in all_alive if u["action_cd"] <= 0 and u["stunned"] <= 0]
        random.shuffle(ready)
        ready.sort(key=lambda u: -u["as"])

        for u in ready:
            if u["dead"]:
                continue
            enemies = [e for e in (alive_b if u["team"] == "a" else alive_a) if not e["dead"]]
            allies = [a for a in (alive_a if u["team"] == "a" else alive_b) if not a["dead"]]
            if not enemies:
                break

            target = _find_target(u, enemies)
            if not target:
                break
            dist = _dist(u, target)

            if dist <= u["range"]:
                # 기본 공격
                dmg = _calc_damage(u, target, u["ad"], is_spell=False)
                is_crit = random.random() < u["crit"]
                if is_crit:
                    dmg = int(dmg * 1.5)
                actual = _deal_damage(u, target, dmg, events)
                u["attack_count"] += 1
                u["mana"] = min(u["max_mana"], u["mana"] + 10)

                # 진 패시브: 4번째 공격
                if u.get("skill", {}).get("params", {}).get("4th_shot_mult") and u["attack_count"] % 4 == 0:
                    bonus = int(u["ad"] * u["skill"]["params"]["4th_shot_mult"])
                    _deal_damage(u, target, bonus, events)
                    events.append({"type": "info", "msg": f"{u['owner']}의 {u['name']} 4번째 공격!"})

                # 마나 가득 → 스킬 사용
                if u["mana"] >= u["max_mana"] and u["max_mana"] > 0:
                    u["mana"] = 0
                    _cast_skill(u, enemies, allies, events)
            else:
                _move_toward(u, target, all_alive)

            u["action_cd"] = max(2, int(8 / max(0.1, u["as"])))

    survivors_a = [u for u in team_a if not u["dead"]]
    survivors_b = [u for u in team_b if not u["dead"]]

    if survivors_a and not survivors_b:
        dmg = sum(u["star"] for u in survivors_a) + player_a["level"]
        return player_a["id"], player_b["id"], dmg, events
    elif survivors_b and not survivors_a:
        dmg = sum(u["star"] for u in survivors_b) + player_b["level"]
        return player_b["id"], player_a["id"], dmg, events
    return None, None, 0, events


def simulate_pve(player, round_num):
    """PvE 전투 시뮬레이션"""
    wave_idx = min(round_num - 1, len(PVE_WAVES) - 1)
    creeps = PVE_WAVES[wave_idx]

    a_units = get_board_units(player)
    if not a_units:
        return False, 0, [{"type": "info", "msg": "유닛이 보드에 없습니다"}]

    # 간단한 PvE: 플레이어 유닛 총 전투력 vs 크리프 총 체력
    player_power = sum(u["ad"] * u["as"] * u["hp"] for u in a_units)
    creep_power = sum(c["ad"] * c["as"] * c["hp"] for c in creeps)

    events = []
    if player_power > creep_power * 0.5:
        events.append({"type": "info", "msg": f"PvE 승리! 크리프를 처치했습니다."})
        return True, 0, events
    else:
        dmg = max(1, len(creeps) * 2)
        events.append({"type": "info", "msg": f"PvE 패배... (-{dmg}HP)"})
        return False, dmg, events


def pair_players(alive_ids):
    players = list(alive_ids)
    random.shuffle(players)
    pairs = []
    if len(players) == 2:
        pairs.append((players[0], players[1], False))
    elif len(players) == 3:
        pairs.append((players[0], players[1], False))
        ghost_opp = random.choice([players[0], players[1]])
        pairs.append((players[2], ghost_opp, True))
    elif len(players) >= 4:
        pairs.append((players[0], players[1], False))
        pairs.append((players[2], players[3], False))
    return pairs
