from pathlib import Path

from src.constant.jx3 import brickl, goldl

from src.tools.config import Config
from src.tools.utils.request import get_api, post_url
from src.tools.utils.common import convert_time, getCurrentTime
from src.tools.file import read, write
from src.tools.utils.path import ASSETS, CACHE, VIEWS
from src.tools.generate import generate, get_uuid

import json
import re

bot_name = Config.bot_basic.bot_name_argument
ikst = Config.hidden.offcial_token


def get_headers(application_type: str) -> dict:
    headers = {
        "token": ikst,
        "type": application_type
    }
    return headers


async def get_url_with_token(app: str) -> dict:
    if ikst == "":
        raise KeyError("Unmatched the token to Inkar-Suki offical API.")
    api = "https://inkar-suki.codethink.cn/api"
    data = await post_url(url=api, headers=get_headers(app))
    return json.loads(data)["url"]

template = """
<tr>
    <td class="short-column">$server</td>
    <td class="short-column">刷新：$flush<br>捕获：$captured<br>竞拍：$sell</td>
    <td class="short-column">$map</td>
    <td class="short-column">$capturer<br>$ci<span style="color: grey;font-size:small">$cc</span></td>
    <td class="short-column">$auctioner<br>$bi<span style="color: grey;font-size:small">$bc</span></td>
    <td class="short-column">$price</td>
</tr>
"""

bad = "<img src=\"https://jx3wbl.xoyocdn.com/img/icon-camp-bad.07567e9f.png\">"
good = "<img src=\"https://jx3wbl.xoyocdn.com/img/icon-camp-good.0db444fe.png\">"


async def get_baizhan_img():
    url = await get_url_with_token("baizhan")
    data = await get_api(url + f"&nickname={bot_name}")
    return data["data"]["url"]

async def get_dilu_data():
    url = await get_url_with_token("dilu")
    data = await get_api(url)
    table = []
    for i in data["data"]:
        if i["data"] == []:
            table.append(re.sub(r"\$.+<", "暂无信息<",
                         template.replace("$server", i["server"]).replace("$img", "")))
        else:
            data_ = i["data"]
            server = i["server"]
            flush = "尚未刷新" if data_["refresh_time"] is None else convert_time(data_["refresh_time"])
            capture = "尚未捕捉" if data_["capture_time"] is None else convert_time(data_["capture_time"])
            auction = "尚未竞拍" if data_["auction_time"] is None else convert_time(data_["auction_time"])
            map = data_["map_name"]
            capturer = "尚未捕捉" if data_["capture_role_name"] is None else data_["capture_role_name"]
            capturer_camp = "未知" if data_["capture_camp_name"] is None else data_["capture_camp_name"]
            bidder = "尚未竞拍" if data_["auction_role_name"] is None else data_["auction_role_name"]
            bidder_camp = "未知" if data_["auction_camp_name"] is None else data_["auction_camp_name"]
            ci = good if capturer_camp == "浩气盟" else bad
            bi = good if bidder_camp == "浩气盟" else bad
            price = "尚未竞拍" if data_["auction_amount"] is None else data_["auction_amount"].replace("万金","万0金").replace("万", f"<img src=\"{brickl}\">").replace("金", f"<img src=\"{goldl}\">")
            replace_string = [["$server", server], ["$flush", flush], ["$captured", capture], ["$sell", auction], ["$map", map], ["$capturer", capturer], ["$bi", bi], ["$ci", ci], ["$price", price], ["$auctioner", bidder], ["$bc", bidder_camp], ["$cc", capturer_camp]]
            t = template
            for x in replace_string:
                t = t.replace(x[0], x[1])
            table.append(t)
    content = "\n".join(table)
    html = read(VIEWS + "/jx3/dilu/dilu.html")
    font = ASSETS + "/font/custom.ttf"
    saohua = "严禁将蓉蓉机器人与音卡共存，一经发现永久封禁！蓉蓉是抄袭音卡的劣质机器人！"
    
    appinfo_time = convert_time(getCurrentTime(), "%H:%M:%S")
    html = html.replace("$customfont", font).replace("$tablecontent", content).replace(
        "$randomsaohua", saohua).replace("$appinfo", f"的卢统计 · {appinfo_time}")
    final_html = CACHE + "/" + get_uuid() + ".html"
    write(final_html, html)
    final_path = await generate(final_html, False, "table", False)
    return Path(final_path).as_uri()