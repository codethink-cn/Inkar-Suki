from src.tools.config import Config
from src.tools.utils.request import post_url, get_api
from src.tools.basic.jx3 import gen_ts, gen_xsk, format_body

from src.plugins.jx3.bind import getPlayerLocalData, Player

import json

ticket = Config.jx3.api.ticket
device_id = ticket.split("::")[-1]

def merge_dict_lists(list1, list2):
    name_to_dict = {d["name"]: d for d in list1}
    for d in list2:
        if d["name"] in name_to_dict:
            name_to_dict[d["name"]]["time"] = d["time"]
        else:
            list1.append(d)
    return list1

class JX3Serendipity:
    def __init__(self):
        self.tl = []
        self.my = []

    def get_serendipity_level(self, serendipity_name: str) -> int:
        if serendipity_name.find("宠物奇缘") != -1:
            serendipity_level = 3
        elif serendipity_name in ["昆吾余火", "浮光织梦", "塞外西风", "入蛟宫", "追魂骨", "千秋铸", "万灵当歌", "流年如虹", "侠行囧途", "争铸吴钩", "兔江湖", "济苍生", "塞外宝驹", "阴阳两界", "三尺青锋", "三山四海"]:
            serendipity_level = 2
        else:
            serendipity_level = 1
        return serendipity_level

    async def get_tuilan_data(self, server: str, name: str):
        role: Player = await getPlayerLocalData(roleName=name, serverName=server)
        data = role.format_jx3api()
        if data["code"] != 200:
            return False
        global_role_id = data["data"]["globalRoleId"]
        param = {
            "name": "完成奇遇",
            "gameRoleId": global_role_id,
            "size": 200,
            "ts": gen_ts()
        }
        param = format_body(param)
        headers = {
            "Host": "m.pvp.xoyo.com",
            "accept": "application/json",
            "deviceid": device_id,
            "platform": "ios",
            "gamename": "jx3",
            "clientkey": "1",
            "cache-control": "no-cache",
            "apiversion": "1",
            "sign": "true",
            "token": ticket,
            "Content-Type": "application/json",
            "Connection": "Keep-Alive",
            "User-Agent": "SeasunGame/178 CFNetwork/1240.0.2 Darwin/20.5.0",
            "X-Sk": gen_xsk(param)
        }
        tl_data = await post_url("https://m.pvp.xoyo.com/achievement/list/achievements", data=param, headers=headers)
        tl_data = json.loads(tl_data)
        serendipities = []
        for serendipity in tl_data["data"]["data"]:
            if serendipity["isFinished"]:
                serendipity_name = serendipity["name"]
                serendipity_level = self.get_serendipity_level(serendipity_name)
                if serendipity_level == 3:
                    serendipity_name = serendipity_name.replace("宠物奇缘·", "")
                serendipities.append(
                    {
                        "name": serendipity_name,
                        "level": serendipity_level,
                        "time": 0
                    }
                )
        self.tl = serendipities

    async def get_my_data(self, server: str, name: str):
        final_url = f"https://pull.j3cx.com/api/serendipity?server={server}&role={name}&pageSize=50"
        data = await get_api(final_url)
        serendipities = []
        data = data["data"]["data"]
        if data == None:
            self.my = serendipities
            return
        for serendipity in data:
            serendipity_name = serendipity["serendipity"]
            serendipity_level = self.get_serendipity_level(serendipity_name)
            new = {
                "name": serendipity_name,
                "level": serendipity_level,
                "time": serendipity["time"]
            }
            serendipities.append(new)
        self.my = serendipities
    
    async def integration(self, server: str, name: str):
        await self.get_tuilan_data(server, name)
        await self.get_my_data(server, name)
        return merge_dict_lists(self.tl, self.my)