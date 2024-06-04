from src.tools.basic import *

import math

gamemode = {
    "金东": 8,
    "金": 9,
    "玉东": 11,
    "玉": 12,
    "王东": 15,
    "王座": 16,
    "三金东": 21,
    "三金": 22,
    "三玉东": 23,
    "三玉": 24,
    "三王东": 25,
    "三王座": 26,
}

koromo_api_sp = "https://5-data.amae-koromo.com/api/v2/pl4/search_player/{player}?limit=20&tag=all" 

koromo_api_pr = "https://5-data.amae-koromo.com/api/v2/pl4/player_records/{player_id}/{end_timestamp}/{start_timestamp}?limit=5&mode={mode}&descending=true"

koromo_api_pes = "https://5-data.amae-koromo.com/api/v2/pl4/player_extended_stats/13042014/1262304000000/1717424339999?mode=9"

def sort_list_of_dicts(list_of_dicts, key_name):
    sorted_list = sorted(list_of_dicts, key=lambda x: x[key_name])
    return sorted_list

def getRank(raw_data):
    if type(raw_data) == type(dict):
        id = raw_data["level"]["id"]
    elif type(raw_data) == type(1): # Accept both `int` and `dict`
        id = raw_data
    major = id % 10000
    minor = math.floor(major / 100)
    rank = "初士杰豪圣"[minor-1] if minor != 6 else "魂"
    label = rank + str(major % 100)
    return label

async def find_player(keyword: str):
    final_url = koromo_api_sp.format(player=keyword)
    data = await get_api(final_url)
    msg = "查找到下列玩家：\n"
    if len(data) == 0:
        return "未找到任何玩家！"
    for i in data:
        msg += f"[{getRank(i)}] " + i["nickname"] + "\n"
    return msg[:-1]

async def get_id_by_name(keyword: str):
    final_url = koromo_api_sp.format(player=keyword)
    data = await get_api(final_url)
    if len(data) != 1:
        return ["未找到任何玩家，或者该ID不准确，请检查后重试！"]
    else:
        return data[0]["id"]

def get_mode_name(mode: int):
    for i in gamemode:
        if mode == gamemode[i]:
            return i

def get_player_sort(player: int, sorted_data: dict):
    for i in sorted_data:
        if player == i["accountId"]:
            return "一二三四"[sorted_data.index(i)]

template_majsoul_record = """
<tr>
    <td>$level</td>
    <td>$num</td>
    <td>$1st（$sc1）<br>$gr1</td>
    <td>$2nd（$sc2）<br>$gr2</td>
    <td>$3rd（$sc3）<br>$gr3</td>
    <td>$4th（$sc4）<br>$gr4</td>
    <td>$time</td>
</tr>"""
    

async def get_records(name: str = None, mode: str = "16.12.9.15.11.8"):
    if name is None:
        return "请输入玩家名！"
    pid = await get_id_by_name(name)
    if type(pid) == type([]):
        return pid[0]
    final_url = koromo_api_pr.format(player_id=pid, end_timestamp=str(getCurrentTime()*1000), start_timestamp="1262304000000", mode=mode)
    data = await get_api(final_url)
    if data == {}:
        return "PID输入错误，或该玩家没有任何记录！"
    else:
        tables = []
        for i in data:
            level = get_mode_name(i["modeId"])
            sorted_players = list(reversed(sort_list_of_dicts(i["players"], "score")))
            place = get_player_sort(pid, sorted_players)
            done_time = convert_time(i["endTime"])
            template = template_majsoul_record.replace("$level", level).replace("$num", place).replace("$time", done_time)
            template = template.replace("$1st", "[" + getRank(sorted_players[0]["level"]) + "] " + sorted_players[0]["nickname"]).replace("$sc1", str(sorted_players[0]["score"])).replace("$gr1", str(sorted_players[0]["gradingScore"]))
            template = template.replace("$2nd", "[" + getRank(sorted_players[1]["level"]) + "] " + sorted_players[1]["nickname"]).replace("$sc2", str(sorted_players[1]["score"])).replace("$gr2", str(sorted_players[1]["gradingScore"]))
            template = template.replace("$3rd", "[" + getRank(sorted_players[2]["level"]) + "] " + sorted_players[2]["nickname"]).replace("$sc3", str(sorted_players[2]["score"])).replace("$gr3", str(sorted_players[2]["gradingScore"]))
            template = template.replace("$4th", "[" + getRank(sorted_players[3]["level"]) + "] " + sorted_players[3]["nickname"]).replace("$sc4", str(sorted_players[3]["score"])).replace("$gr4", str(sorted_players[3]["gradingScore"]))
            tables.append(template)
        html = read(VIEWS + "/majsoul/record/record.html")
        html = html.replace("$player_name", name).replace("$tablecontent", "\n".join(tables))
        final_html = CACHE + "/" + get_uuid() + ".html"
        write(final_html, html)
        final_path = await generate(final_html, False, ".background-container", False)
        return [Path(final_path).as_uri()]