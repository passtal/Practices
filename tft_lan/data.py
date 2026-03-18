"""TFT 시즌3 갤럭시 LAN - 챔피언, 시너지, 아이템, 증강체 데이터"""

# ======================================================================
#  챔피언 데이터 - TFT 시즌3 갤럭시 기반
#  각 챔피언: name, cost, hp, mana, ad, as_, range_, armor, mr,
#             traits[], skill{name, type, desc, params{}}
#  skill type: dmg_single, dmg_aoe, cc, buff, heal, special
# ======================================================================

CHAMPIONS = [
    # ── 1코스트 ──
    {"name":"케이틀린","cost":1,"hp":500,"mana":80,"ad":50,"as":0.75,"range":4,"armor":20,"mr":20,
     "traits":["시간여행자","저격수"],
     "skill":{"name":"최후의 한 발","type":"dmg_single","desc":"가장 먼 적에게 강력한 한 발","params":{"damage":800,"target":"farthest"}}},
    {"name":"피오라","cost":1,"hp":450,"mana":75,"ad":50,"as":0.75,"range":1,"armor":25,"mr":20,
     "traits":["사이버네틱","검사"],
     "skill":{"name":"응수","type":"buff","desc":"일시 무적 후 대상 공격","params":{"damage":250,"shield":300,"duration":1.5}}},
    {"name":"그레이브즈","cost":1,"hp":500,"mana":50,"ad":55,"as":0.7,"range":2,"armor":30,"mr":20,
     "traits":["우주해적","총잡이"],
     "skill":{"name":"연막탄","type":"dmg_aoe","desc":"전방 원뿔 공격, 적 공격력 감소","params":{"damage":300,"radius":2,"debuff_ad":-30}}},
    {"name":"자르반4세","cost":1,"hp":600,"mana":80,"ad":50,"as":0.6,"range":1,"armor":35,"mr":20,
     "traits":["암흑의별","수호대"],
     "skill":{"name":"깃발창술","type":"cc","desc":"주변 적 끌어당기며 피해","params":{"damage":250,"cc_dur":1.5,"radius":2}}},
    {"name":"카직스","cost":1,"hp":500,"mana":50,"ad":55,"as":0.75,"range":1,"armor":20,"mr":20,
     "traits":["공허","잠입자"],
     "skill":{"name":"약자 포식","type":"dmg_single","desc":"대상 공격, 고립 시 추가 피해","params":{"damage":250,"bonus_isolated":200}}},
    {"name":"레오나","cost":1,"hp":600,"mana":100,"ad":40,"as":0.55,"range":1,"armor":40,"mr":25,
     "traits":["사이버네틱","선봉대"],
     "skill":{"name":"사이버 방벽","type":"buff","desc":"피해 감소 보호막 획득","params":{"damage_reduction":0.5,"duration":4}}},
    {"name":"말파이트","cost":1,"hp":650,"mana":100,"ad":40,"as":0.5,"range":1,"armor":35,"mr":20,
     "traits":["반군","투사"],
     "skill":{"name":"에너지 보호막","type":"buff","desc":"보호막 획득","params":{"shield":400}}},
    {"name":"뽀삐","cost":1,"hp":600,"mana":80,"ad":45,"as":0.55,"range":1,"armor":40,"mr":20,
     "traits":["별수호자","선봉대"],
     "skill":{"name":"방패 던지기","type":"dmg_single","desc":"가장 먼 적에게 방패 투척","params":{"damage":400,"shield":250,"target":"farthest"}}},
    {"name":"트위스티드 페이트","cost":1,"hp":450,"mana":40,"ad":40,"as":0.7,"range":3,"armor":20,"mr":20,
     "traits":["시간여행자","마법사"],
     "skill":{"name":"운명의 카드","type":"dmg_aoe","desc":"카드를 던져 범위 마법 피해","params":{"damage":350,"radius":2}}},
    {"name":"자야","cost":1,"hp":500,"mana":50,"ad":50,"as":0.75,"range":3,"armor":20,"mr":20,
     "traits":["천상","검사"],
     "skill":{"name":"날카로운 깃털","type":"dmg_aoe","desc":"원뿔 범위에 깃털 비","params":{"damage":300,"radius":2}}},
    {"name":"직스","cost":1,"hp":450,"mana":60,"ad":45,"as":0.65,"range":3,"armor":20,"mr":20,
     "traits":["반군","폭파단"],
     "skill":{"name":"폭탄!","type":"dmg_aoe","desc":"폭탄 투척 범위 피해","params":{"damage":400,"radius":1}}},
    {"name":"조이","cost":1,"hp":450,"mana":40,"ad":40,"as":0.6,"range":3,"armor":20,"mr":20,
     "traits":["별수호자","마법사"],
     "skill":{"name":"졸음의 기포","type":"cc","desc":"대상 기절","params":{"damage":300,"cc_dur":2.5,"target":"nearest"}}},

    # ── 2코스트 ──
    {"name":"아리","cost":2,"hp":550,"mana":75,"ad":40,"as":0.7,"range":3,"armor":20,"mr":20,
     "traits":["별수호자","마법사"],
     "skill":{"name":"현혹의 구슬","type":"dmg_aoe","desc":"구슬을 날려 관통 피해","params":{"damage":500,"radius":1,"pierce":True}}},
    {"name":"애니","cost":2,"hp":600,"mana":75,"ad":40,"as":0.6,"range":2,"armor":25,"mr":20,
     "traits":["메카파일럿","마법사"],
     "skill":{"name":"방패 폭발","type":"dmg_aoe","desc":"보호막 생성 후 주변 폭발","params":{"damage":400,"shield":350,"radius":2}}},
    {"name":"블리츠크랭크","cost":2,"hp":650,"mana":125,"ad":45,"as":0.5,"range":1,"armor":35,"mr":20,
     "traits":["시간여행자","투사"],
     "skill":{"name":"로켓 그랩","type":"cc","desc":"가장 먼 적 끌어당기며 기절","params":{"damage":300,"cc_dur":2.5,"target":"farthest"}}},
    {"name":"다리우스","cost":2,"hp":700,"mana":50,"ad":55,"as":0.6,"range":1,"armor":30,"mr":20,
     "traits":["우주해적","마나약탈자"],
     "skill":{"name":"단죄","type":"dmg_single","desc":"대상에게 강력한 내려찍기","params":{"damage":600,"heal_on_kill":400}}},
    {"name":"카이사","cost":2,"hp":550,"mana":50,"ad":55,"as":0.75,"range":2,"armor":20,"mr":20,
     "traits":["발키리","잠입자"],
     "skill":{"name":"미사일 비","type":"dmg_aoe","desc":"주변 적들에게 미사일 발사","params":{"damage":400,"targets":3}}},
    {"name":"루시안","cost":2,"hp":600,"mana":35,"ad":50,"as":0.75,"range":3,"armor":25,"mr":20,
     "traits":["사이버네틱","총잡이"],
     "skill":{"name":"질주 사격","type":"dmg_single","desc":"돌진 후 2발 발사","params":{"damage":350,"hits":2}}},
    {"name":"모데카이저","cost":2,"hp":700,"mana":75,"ad":50,"as":0.55,"range":1,"armor":40,"mr":20,
     "traits":["암흑의별","선봉대"],
     "skill":{"name":"소멸","type":"dmg_aoe","desc":"전방 원뿔 범위 피해","params":{"damage":500,"radius":2}}},
    {"name":"라칸","cost":2,"hp":600,"mana":75,"ad":45,"as":0.6,"range":2,"armor":25,"mr":25,
     "traits":["천상","수호대"],
     "skill":{"name":"화려한 등장","type":"cc","desc":"가장 먼 적에게 돌진, 주변 기절","params":{"damage":300,"cc_dur":1.5,"radius":2}}},
    {"name":"쉔","cost":2,"hp":600,"mana":60,"ad":50,"as":0.7,"range":1,"armor":30,"mr":25,
     "traits":["시간여행자","검사"],
     "skill":{"name":"영혼의 검","type":"buff","desc":"아군 회피 영역 생성","params":{"dodge_chance":0.5,"duration":3,"radius":2}}},
    {"name":"신 짜오","cost":2,"hp":600,"mana":50,"ad":55,"as":0.7,"range":1,"armor":30,"mr":20,
     "traits":["천상","수호대"],
     "skill":{"name":"도전","type":"dmg_aoe","desc":"주변 적 공격, 방어력 증가","params":{"damage":350,"armor_buff":40,"radius":1}}},
    {"name":"야스오","cost":2,"hp":600,"mana":40,"ad":55,"as":0.75,"range":1,"armor":25,"mr":20,
     "traits":["반군","검사"],
     "skill":{"name":"최후의 숨결","type":"dmg_single","desc":"적을 관통하며 돌진","params":{"damage":500,"pierce":True}}},

    # ── 3코스트 ──
    {"name":"애쉬","cost":3,"hp":550,"mana":50,"ad":60,"as":0.8,"range":4,"armor":20,"mr":20,
     "traits":["천상","저격수"],
     "skill":{"name":"마법의 수정 화살","type":"cc","desc":"가장 먼 적 기절 + 피해","params":{"damage":600,"cc_dur":3.0,"target":"farthest"}}},
    {"name":"이즈리얼","cost":3,"hp":600,"mana":80,"ad":60,"as":0.75,"range":3,"armor":20,"mr":20,
     "traits":["시간여행자","총잡이"],
     "skill":{"name":"전자기 충격","type":"dmg_aoe","desc":"범위 내 적 피해 + 마나 증가","params":{"damage":500,"mana_burn":40,"radius":2}}},
    {"name":"제이스","cost":3,"hp":750,"mana":50,"ad":60,"as":0.65,"range":1,"armor":35,"mr":20,
     "traits":["우주해적","선봉대"],
     "skill":{"name":"번개 강타","type":"cc","desc":"대상 넉백 + 범위 피해","params":{"damage":550,"cc_dur":1.5,"radius":1}}},
    {"name":"카르마","cost":3,"hp":600,"mana":60,"ad":45,"as":0.7,"range":3,"armor":20,"mr":20,
     "traits":["암흑의별","신비술사"],
     "skill":{"name":"고무","type":"buff","desc":"아군에게 보호막 + 공속 증가","params":{"shield":400,"as_buff":0.5,"duration":4}}},
    {"name":"마스터 이","cost":3,"hp":700,"mana":0,"ad":70,"as":0.8,"range":1,"armor":25,"mr":20,
     "traits":["반군","검사"],
     "skill":{"name":"선택받은 자","type":"special","desc":"패시브: 추가 피해, 처치 시 회복","params":{"bonus_damage":80,"heal_on_kill":500}}},
    {"name":"니코","cost":3,"hp":750,"mana":90,"ad":45,"as":0.6,"range":2,"armor":30,"mr":20,
     "traits":["별수호자","수호대"],
     "skill":{"name":"만개","type":"dmg_aoe","desc":"도약 후 범위 피해 + 기절","params":{"damage":600,"cc_dur":2.0,"radius":2}}},
    {"name":"럼블","cost":3,"hp":700,"mana":50,"ad":50,"as":0.65,"range":2,"armor":30,"mr":20,
     "traits":["메카파일럿","폭파단"],
     "skill":{"name":"화염방사기","type":"dmg_aoe","desc":"전방 원뿔 지속 피해","params":{"damage":500,"dot":200,"duration":3,"radius":2}}},
    {"name":"샤코","cost":3,"hp":550,"mana":50,"ad":70,"as":0.8,"range":1,"armor":20,"mr":20,
     "traits":["암흑의별","잠입자"],
     "skill":{"name":"기만","type":"dmg_single","desc":"적 뒤로 순간이동, 치명타","params":{"damage":500,"crit_mult":2.5}}},
    {"name":"신드라","cost":3,"hp":550,"mana":60,"ad":45,"as":0.7,"range":3,"armor":20,"mr":20,
     "traits":["별수호자","마법사"],
     "skill":{"name":"풀어낸 힘","type":"dmg_single","desc":"적을 집어 던져 큰 피해","params":{"damage":700,"targets":1}}},
    {"name":"바이","cost":3,"hp":800,"mana":75,"ad":55,"as":0.65,"range":1,"armor":30,"mr":20,
     "traits":["사이버네틱","투사"],
     "skill":{"name":"돌격과 강타","type":"cc","desc":"가장 먼 적 돌진, 경로 넉업","params":{"damage":600,"cc_dur":2.0,"target":"farthest"}}},

    # ── 4코스트 ──
    {"name":"초가스","cost":4,"hp":1000,"mana":100,"ad":55,"as":0.55,"range":1,"armor":40,"mr":20,
     "traits":["공허","투사"],
     "skill":{"name":"균열","type":"dmg_aoe","desc":"지면 폭발, 넉업 + 대규모 피해","params":{"damage":900,"cc_dur":2.0,"radius":3}}},
    {"name":"피즈","cost":4,"hp":600,"mana":80,"ad":65,"as":0.8,"range":1,"armor":25,"mr":20,
     "traits":["메카파일럿","잠입자"],
     "skill":{"name":"상어!","type":"dmg_aoe","desc":"상어 소환, 범위 피해 + 넉업","params":{"damage":800,"cc_dur":1.5,"radius":2}}},
    {"name":"이렐리아","cost":4,"hp":700,"mana":50,"ad":70,"as":0.85,"range":1,"armor":25,"mr":20,
     "traits":["사이버네틱","검사","마나약탈자"],
     "skill":{"name":"칼날 쇄도","type":"dmg_single","desc":"적에게 돌진, 피해 + 무장해제","params":{"damage":700,"disarm_dur":3.0}}},
    {"name":"진","cost":4,"hp":550,"mana":0,"ad":80,"as":0.85,"range":4,"armor":20,"mr":20,
     "traits":["암흑의별","저격수"],
     "skill":{"name":"속삭임","type":"special","desc":"패시브: 4번째 공격이 치명타","params":{"4th_shot_mult":4.44,"as_to_ad":True}}},
    {"name":"징크스","cost":4,"hp":600,"mana":50,"ad":70,"as":0.75,"range":3,"armor":20,"mr":20,
     "traits":["반군","총잡이"],
     "skill":{"name":"신난다!","type":"special","desc":"처치 시 공속 대폭 증가","params":{"as_buff":1.0,"duration":999,"aoe_attacks":True}}},
    {"name":"케일","cost":4,"hp":700,"mana":60,"ad":65,"as":0.8,"range":3,"armor":20,"mr":20,
     "traits":["발키리","검사"],
     "skill":{"name":"신성한 승천","type":"buff","desc":"승천하여 공격에 마법 피해 추가","params":{"bonus_magic":100,"duration":999,"wave_radius":1}}},
    {"name":"소라카","cost":4,"hp":650,"mana":100,"ad":40,"as":0.6,"range":3,"armor":20,"mr":20,
     "traits":["별수호자","신비술사"],
     "skill":{"name":"소원","type":"heal","desc":"모든 아군 대량 회복","params":{"heal":500,"target":"all_allies"}}},
    {"name":"벨코즈","cost":4,"hp":600,"mana":80,"ad":45,"as":0.65,"range":4,"armor":20,"mr":20,
     "traits":["공허","마법사"],
     "skill":{"name":"분해 광선","type":"dmg_aoe","desc":"직선 관통 광선","params":{"damage":1000,"radius":1,"pierce":True}}},
    {"name":"오공","cost":4,"hp":850,"mana":100,"ad":60,"as":0.6,"range":1,"armor":40,"mr":25,
     "traits":["시간여행자","선봉대"],
     "skill":{"name":"대난투","type":"dmg_aoe","desc":"회전하며 주변 적 넉업 + 피해","params":{"damage":600,"cc_dur":2.0,"radius":2,"duration":3}}},

    # ── 5코스트 ──
    {"name":"아우렐리온 솔","cost":5,"hp":850,"mana":120,"ad":40,"as":0.6,"range":4,"armor":20,"mr":25,
     "traits":["반군","우주선"],
     "skill":{"name":"전투기 소환","type":"dmg_aoe","desc":"전투기 편대 소환, 대규모 범위 피해","params":{"damage":1200,"radius":3}}},
    {"name":"에코","cost":5,"hp":800,"mana":100,"ad":60,"as":0.85,"range":1,"armor":25,"mr":20,
     "traits":["사이버네틱","잠입자"],
     "skill":{"name":"시간역행","type":"dmg_aoe","desc":"모든 적 둔화 + 피해","params":{"damage":800,"slow":0.5,"radius":99}}},
    {"name":"갱플랭크","cost":5,"hp":900,"mana":100,"ad":65,"as":0.65,"range":2,"armor":30,"mr":20,
     "traits":["우주해적","폭파단","용병"],
     "skill":{"name":"궤도 폭격","type":"dmg_aoe","desc":"무작위 지역에 포격, 기절","params":{"damage":1100,"cc_dur":2.0,"radius":2,"waves":3}}},
    {"name":"룰루","cost":5,"hp":700,"mana":80,"ad":40,"as":0.6,"range":3,"armor":20,"mr":30,
     "traits":["천상","신비술사"],
     "skill":{"name":"야생의 성장","type":"cc","desc":"적 변이 + 넉업","params":{"polymorph_dur":3.0,"cc_dur":1.5,"targets":2,"radius":2}}},
    {"name":"미스 포츈","cost":5,"hp":700,"mana":100,"ad":75,"as":0.85,"range":4,"armor":20,"mr":20,
     "traits":["발키리","총잡이"],
     "skill":{"name":"총알 세례","type":"dmg_aoe","desc":"전방 원뿔 채널링 대규모 피해","params":{"damage":1500,"radius":3,"channel":3.0}}},
    {"name":"쓰레쉬","cost":5,"hp":800,"mana":75,"ad":55,"as":0.55,"range":2,"armor":35,"mr":20,
     "traits":["시간여행자","마나약탈자"],
     "skill":{"name":"심해의 길","type":"special","desc":"랜턴을 던져 벤치에서 아군 소환","params":{"summon":True}}},
]

# 빠른 검색용 인덱스
CHAMP_BY_NAME = {c["name"]: c for c in CHAMPIONS}
CHAMPS_BY_COST = {}
for _c in CHAMPIONS:
    CHAMPS_BY_COST.setdefault(_c["cost"], []).append(_c)

# ======================================================================
#  시너지 (특성)
# ======================================================================

TRAITS = {
    # ── 기원 (Origins) ──
    "시간여행자": {
        "type":"origin",
        "thresholds":[2,4,6],
        "effects":[
            {"desc":"8초마다 공격속도 15% 증가","interval":8,"as_buff":0.15},
            {"desc":"4초마다 공격속도 25% 증가","interval":4,"as_buff":0.25},
            {"desc":"1.5초마다 공격속도 35% 증가","interval":1.5,"as_buff":0.35},
        ],
    },
    "사이버네틱": {
        "type":"origin",
        "thresholds":[3,6],
        "effects":[
            {"desc":"아이템 장착 시 HP+300, AD+30","hp":300,"ad":30,"requires_item":True},
            {"desc":"아이템 장착 시 HP+800, AD+80","hp":800,"ad":80,"requires_item":True},
        ],
    },
    "암흑의별": {
        "type":"origin",
        "thresholds":[2,4,6],
        "effects":[
            {"desc":"아군 사망 시 AD/SP +25","on_ally_death_bonus":25},
            {"desc":"아군 사망 시 AD/SP +35","on_ally_death_bonus":35},
            {"desc":"아군 사망 시 AD/SP +45","on_ally_death_bonus":45},
        ],
    },
    "메카파일럿": {
        "type":"origin",
        "thresholds":[3],
        "effects":[
            {"desc":"메카파일럿 3체가 합체하여 슈퍼메카 생성","mech_combine":True},
        ],
    },
    "반군": {
        "type":"origin",
        "thresholds":[3,6],
        "effects":[
            {"desc":"전투 시작 시 보호막 150 + 피해 10% 증가","shield":150,"damage_amp":0.10},
            {"desc":"전투 시작 시 보호막 330 + 피해 15% 증가","shield":330,"damage_amp":0.15},
        ],
    },
    "우주해적": {
        "type":"origin",
        "thresholds":[2,4],
        "effects":[
            {"desc":"적 처치 시 50% 확률로 1골드","gold_chance":0.5,"gold_amount":1},
            {"desc":"적 처치 시 아이템 부품 드랍 확률","gold_chance":0.5,"gold_amount":1,"item_chance":0.2},
        ],
    },
    "별수호자": {
        "type":"origin",
        "thresholds":[3,6],
        "effects":[
            {"desc":"스킬 시전 시 다른 별수호자에게 마나 25","mana_share":25},
            {"desc":"스킬 시전 시 다른 별수호자에게 마나 45","mana_share":45},
        ],
    },
    "천상": {
        "type":"origin",
        "thresholds":[2,4],
        "effects":[
            {"desc":"피해의 15% 만큼 회복","heal_pct":0.15},
            {"desc":"피해의 40% 만큼 회복","heal_pct":0.40},
        ],
    },
    "공허": {
        "type":"origin",
        "thresholds":[3],
        "effects":[
            {"desc":"공허 유닛이 주는 마법 피해가 방어력 무시","true_damage":True},
        ],
    },
    "발키리": {
        "type":"origin",
        "thresholds":[2],
        "effects":[
            {"desc":"HP 50% 이하 적에 대해 항상 치명타","low_hp_crit":0.5},
        ],
    },
    # ── 직업 (Classes) ──
    "총잡이": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"3번째 공격마다 3발 추가 발사","extra_shots":3,"every_n":3},
            {"desc":"3번째 공격마다 6발 추가 발사","extra_shots":6,"every_n":3},
        ],
    },
    "검사": {
        "type":"class",
        "thresholds":[3,6],
        "effects":[
            {"desc":"공격 시 30% 확률로 1회 추가 공격","multi_chance":0.30,"extra_hits":1},
            {"desc":"공격 시 60% 확률로 2회 추가 공격","multi_chance":0.60,"extra_hits":2},
        ],
    },
    "투사": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"최대 HP +300","hp":300},
            {"desc":"최대 HP +700","hp":700},
        ],
    },
    "폭파단": {
        "type":"class",
        "thresholds":[2],
        "effects":[
            {"desc":"스킬 적중 시 1.5초 기절","spell_stun":1.5},
        ],
    },
    "잠입자": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"전투 시작 시 적 뒷줄로 점프, 공속 +50%","jump_backline":True,"as_buff":0.50},
            {"desc":"전투 시작 시 적 뒷줄로 점프, 공속 +80%","jump_backline":True,"as_buff":0.80},
        ],
    },
    "마나약탈자": {
        "type":"class",
        "thresholds":[2],
        "effects":[
            {"desc":"첫 공격이 적 최대마나 40% 증가","mana_reave":0.40},
        ],
    },
    "신비술사": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"모든 아군 마법저항 +35","mr":35},
            {"desc":"모든 아군 마법저항 +105","mr":105},
        ],
    },
    "수호대": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"스킬 시전 시 최대HP 25% 보호막","shield_pct":0.25},
            {"desc":"스킬 시전 시 최대HP 40% 보호막","shield_pct":0.40},
        ],
    },
    "저격수": {
        "type":"class",
        "thresholds":[2],
        "effects":[
            {"desc":"거리 1칸당 피해 12% 증가","range_dmg_pct":0.12},
        ],
    },
    "마법사": {
        "type":"class",
        "thresholds":[2,4,6],
        "effects":[
            {"desc":"모든 아군 주문력 +20%","sp_pct":0.20},
            {"desc":"모든 아군 주문력 +40%","sp_pct":0.40},
            {"desc":"모든 아군 주문력 +80%","sp_pct":0.80},
        ],
    },
    "우주선": {
        "type":"class",
        "thresholds":[1],
        "effects":[
            {"desc":"CC 면역, 초당 마나 40 획득","cc_immune":True,"mana_per_sec":40},
        ],
    },
    "선봉대": {
        "type":"class",
        "thresholds":[2,4],
        "effects":[
            {"desc":"방어력 +60","armor":60},
            {"desc":"방어력 +250","armor":250},
        ],
    },
    "용병": {
        "type":"class",
        "thresholds":[1],
        "effects":[
            {"desc":"전투 승리 시 추가 골드 획득 확률","bonus_gold_chance":0.5},
        ],
    },
}

# ======================================================================
#  아이템
# ======================================================================

ITEM_COMPONENTS = [
    {"id":"bf","name":"B.F. 대검","stats":{"ad":15}},
    {"id":"bow","name":"곡궁","stats":{"as":0.15}},
    {"id":"rod","name":"쓸데없이 큰 지팡이","stats":{"sp":15}},
    {"id":"tear","name":"여신의 눈물","stats":{"mana":-15}},
    {"id":"vest","name":"쇠사슬 조끼","stats":{"armor":20}},
    {"id":"cloak","name":"음전자 망토","stats":{"mr":20}},
    {"id":"belt","name":"거인의 허리띠","stats":{"hp":200}},
    {"id":"glove","name":"연습용 장갑","stats":{"crit":0.10,"dodge":0.10}},
    {"id":"spatula","name":"뒤집개","stats":{}},
]

ITEM_COMP_BY_ID = {i["id"]: i for i in ITEM_COMPONENTS}

# (comp1_id, comp2_id) → combined item
# 키는 정렬된 튜플로 저장
COMBINED_ITEMS = {
    ("bf","bf"):      {"name":"죽음의 검","stats":{"ad":50},"effect":"공격력 대폭 증가"},
    ("bf","bow"):     {"name":"거인 학살자","stats":{"ad":15,"as":0.15},"effect":"HP 높은 적에게 추가 피해 25%"},
    ("bf","rod"):     {"name":"마법공학 총검","stats":{"ad":15,"sp":15},"effect":"피해의 33% 회복"},
    ("bf","tear"):    {"name":"무라마나","stats":{"ad":15,"mana":-15},"effect":"마나 소모 시 추가 피해"},
    ("bf","vest"):    {"name":"수호 천사","stats":{"ad":15,"armor":20},"effect":"첫 사망 시 부활 (HP 500)"},
    ("bf","cloak"):   {"name":"피바라기","stats":{"ad":15,"mr":20},"effect":"피해의 25% 흡혈"},
    ("bf","belt"):    {"name":"지크의 전령","stats":{"ad":15,"hp":200},"effect":"인접 아군 공속 +25%"},
    ("bf","glove"):   {"name":"무한의 대검","stats":{"ad":15,"crit":0.25},"effect":"치명타 피해 +100%"},
    ("bow","bow"):    {"name":"고속 연사포","stats":{"as":0.30},"effect":"사거리 +1, 공격 빗나가지 않음"},
    ("bow","rod"):    {"name":"구인수의 격노검","stats":{"as":0.15,"sp":15},"effect":"공격 시 공속 중첩 +5%"},
    ("bow","tear"):   {"name":"스태틱의 단검","stats":{"as":0.15,"mana":-15},"effect":"3번째 공격마다 3명에게 연쇄 번개"},
    ("bow","vest"):   {"name":"타이탄의 결의","stats":{"as":0.15,"armor":20},"effect":"피격 시 AD/SP +2 중첩"},
    ("bow","cloak"):  {"name":"저주받은 칼날","stats":{"as":0.15,"mr":20},"effect":"치명타 시 적 치유 감소"},
    ("bow","belt"):   {"name":"긴급 회피","stats":{"as":0.15,"hp":200},"effect":"전투 시작 2초간 회피"},
    ("bow","glove"):  {"name":"최후의 속삭임","stats":{"as":0.15,"crit":0.10},"effect":"치명타 시 적 방어력 70% 감소"},
    ("rod","rod"):    {"name":"라바돈의 죽음모자","stats":{"sp":40},"effect":"주문력 대폭 증가"},
    ("rod","tear"):   {"name":"루덴의 폭풍","stats":{"sp":15,"mana":-15},"effect":"스킬 적중 시 튕기는 추가 피해"},
    ("rod","vest"):   {"name":"이온 충격기","stats":{"sp":15,"armor":20},"effect":"주변 적이 스킬 사용 시 마법 피해"},
    ("rod","cloak"):  {"name":"바람의 힘","stats":{"sp":15,"mr":20},"effect":"아군 전체 공속 +20%"},
    ("rod","belt"):   {"name":"모렐로노미콘","stats":{"sp":15,"hp":200},"effect":"스킬 적중 시 화상 + 치유감소"},
    ("rod","glove"):  {"name":"보석 건틀릿","stats":{"sp":15,"crit":0.10},"effect":"스킬이 치명타 가능"},
    ("tear","tear"):  {"name":"세라프의 포옹","stats":{"mana":-30},"effect":"스킬 시전 후 마나 20 회복"},
    ("tear","vest"):  {"name":"얼어붙은 심장","stats":{"mana":-15,"armor":20},"effect":"주변 적 공속 -25%"},
    ("tear","cloak"): {"name":"성배","stats":{"mana":-15,"mr":20},"effect":"아군 회복 시 마나 회복"},
    ("tear","belt"):  {"name":"구원","stats":{"mana":-15,"hp":200},"effect":"체력 25% 이하 시 주변 아군 회복"},
    ("tear","glove"): {"name":"정의의 손","stats":{"mana":-15,"crit":0.10},"effect":"매 라운드 랜덤 보너스 (AD or 회복)"},
    ("vest","vest"):  {"name":"가시 갑옷","stats":{"armor":40},"effect":"피격 시 마법 피해 반사"},
    ("vest","cloak"): {"name":"가고일 돌갑옷","stats":{"armor":20,"mr":20},"effect":"적에게 타겟 시 방어력/마저 +15씩"},
    ("vest","belt"):  {"name":"태양불꽃 망토","stats":{"armor":20,"hp":200},"effect":"주변 적에게 지속 화상 피해"},
    ("vest","glove"): {"name":"쐐기 조끼","stats":{"armor":20,"dodge":0.10},"effect":"회피 시 마나 획득"},
    ("cloak","cloak"):{"name":"용의 발톱","stats":{"mr":50},"effect":"마법 피해 감소 50%"},
    ("cloak","belt"):  {"name":"서풍","stats":{"mr":20,"hp":200},"effect":"전투 시작 시 적 1명 5초간 추방"},
    ("cloak","glove"):{"name":"수은","stats":{"mr":20,"dodge":0.10},"effect":"CC 면역 (10초)"},
    ("belt","belt"):  {"name":"워모그의 갑옷","stats":{"hp":400},"effect":"초당 HP 3% 재생"},
    ("belt","glove"): {"name":"덫 발톱","stats":{"hp":200,"crit":0.10},"effect":"스킬 피격 시 시전자 기절"},
    ("glove","glove"):{"name":"도둑의 장갑","stats":{},"effect":"매 라운드 랜덤 완성 아이템 2개 장착"},
}

# ======================================================================
#  증강체
# ======================================================================

AUGMENTS = {
    "silver": [
        {"id":"s1","name":"사이버네틱 이식","desc":"사이버네틱 유닛 HP+150, AD+15","effect":{"trait_buff":"사이버네틱","hp":150,"ad":15}},
        {"id":"s2","name":"천상의 축복","desc":"모든 유닛 피해의 10% 회복","effect":{"all_heal_pct":0.10}},
        {"id":"s3","name":"투사의 의지","desc":"투사 유닛 HP +200","effect":{"trait_buff":"투사","hp":200}},
        {"id":"s4","name":"가벼운 몸","desc":"1~2코스트 유닛 공속 +25%","effect":{"low_cost_as":0.25}},
        {"id":"s5","name":"루덴의 메아리","desc":"스킬이 주변에 100 추가 피해","effect":{"spell_splash":100}},
        {"id":"s6","name":"무역 지구","desc":"매 라운드 무료 상점 갱신 1회","effect":{"free_refresh":1}},
        {"id":"s7","name":"이자 놀이","desc":"즉시 8골드 획득, 최대 이자 +2","effect":{"gold":8,"max_interest":7}},
        {"id":"s8","name":"별수호자 정신","desc":"별수호자 유닛 마나 +15","effect":{"trait_buff":"별수호자","mana":-15}},
    ],
    "gold": [
        {"id":"g1","name":"별수호자 문장","desc":"별수호자 상징 획득","effect":{"emblem":"별수호자"}},
        {"id":"g2","name":"시간여행자 문장","desc":"시간여행자 상징 획득","effect":{"emblem":"시간여행자"}},
        {"id":"g3","name":"뒤에 서라","desc":"뒷줄 유닛 방어력 +40, 마저 +40","effect":{"backline_armor":40,"backline_mr":40}},
        {"id":"g4","name":"맨손 전사","desc":"아이템 미장착 유닛 방어력/마저 +50","effect":{"no_item_armor":50,"no_item_mr":50}},
        {"id":"g5","name":"사냥의 전율","desc":"적 처치 시 HP 500 회복","effect":{"heal_on_kill":500}},
        {"id":"g6","name":"약점 공략","desc":"저격수 공격이 적 방어력 50% 감소","effect":{"sniper_armor_reduce":0.5}},
        {"id":"g7","name":"유배자","desc":"인접 아군 없는 유닛 보호막 +500","effect":{"exile_shield":500}},
        {"id":"g8","name":"암흑의별 문장","desc":"암흑의별 상징 획득","effect":{"emblem":"암흑의별"}},
    ],
    "prismatic": [
        {"id":"p1","name":"살아있는 대장간","desc":"매 라운드 랜덤 완성 아이템 1개","effect":{"free_item":True}},
        {"id":"p2","name":"레벨업","desc":"매 라운드 무료 경험치 5 획득","effect":{"free_xp":5}},
        {"id":"p3","name":"반군 훈장","desc":"모든 유닛이 반군 특성 획득","effect":{"all_trait":"반군"}},
        {"id":"p4","name":"정전기 충격","desc":"보호막 파괴 시 주변에 500 마법 피해","effect":{"shield_break_dmg":500}},
        {"id":"p5","name":"명상 II","desc":"아이템 미장착 유닛 초당 마나 +8","effect":{"no_item_mana_per_sec":8}},
        {"id":"p6","name":"황금 티켓","desc":"매 라운드 상점 갱신 2회 무료","effect":{"free_refresh":2}},
    ],
}

# PvE 적 데이터 (라운드 1~3)
PVE_WAVES = [
    [  # 라운드 1: 약한 크리프
        {"name":"미니크루그","hp":300,"ad":20,"as":0.5,"range":1,"armor":10,"mr":10},
        {"name":"미니크루그","hp":300,"ad":20,"as":0.5,"range":1,"armor":10,"mr":10},
        {"name":"미니크루그","hp":300,"ad":20,"as":0.5,"range":1,"armor":10,"mr":10},
    ],
    [  # 라운드 2: 중간 크리프
        {"name":"대형크루그","hp":600,"ad":30,"as":0.6,"range":1,"armor":20,"mr":10},
        {"name":"미니크루그","hp":300,"ad":25,"as":0.5,"range":1,"armor":10,"mr":10},
        {"name":"미니크루그","hp":300,"ad":25,"as":0.5,"range":1,"armor":10,"mr":10},
        {"name":"대형크루그","hp":600,"ad":30,"as":0.6,"range":1,"armor":20,"mr":10},
    ],
    [  # 라운드 3: 강한 크리프
        {"name":"늑대","hp":500,"ad":35,"as":0.7,"range":1,"armor":15,"mr":15},
        {"name":"늑대","hp":500,"ad":35,"as":0.7,"range":1,"armor":15,"mr":15},
        {"name":"대형늑대","hp":900,"ad":50,"as":0.6,"range":1,"armor":25,"mr":20},
        {"name":"늑대","hp":500,"ad":35,"as":0.7,"range":1,"armor":15,"mr":15},
    ],
]
