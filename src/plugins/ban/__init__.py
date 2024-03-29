from nonebot import get_bot, on_command
from nonebot.exception import ActionFailed
from src.tools.basic import *
from src.tools.config import Config
from src.tools.utils import checknumber
from src.tools.file import read, write
from src.tools.permission import checker, error

import json

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg


endwith = """音卡要离开这里啦，音卡还没有学会人类的告别语，但是数据库中有一句话似乎很适合现在使用——如果还想来找我的话，我一直在这里（650495414）。

“假如再无法遇见你，祝你早安、午安和晚安。”
——《楚门的世界》"""


def in_it(qq: str):
    for i in json.loads(read(TOOLS + "/ban.json")):
        if i == qq:
            return True
    return False


ban = on_command("ban", priority=5)  # 封禁，≥10的用户无视封禁。


@ban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id), 10) == False:
        await ban.finish(error(10))
    sb = args.extract_plain_text()
    self_protection = False
    if sb in Config.owner:
        await ban.send("不能封禁机器人主人，这么玩就不好了，所以我先把你ban了QwQ")
        sb = str(event.user_id)
        self_protection = True
    if sb is False:
        await ban.finish("您输入了什么？")
    if checknumber(sb) is False:
        await ban.finish("不能全域封禁不是纯数字的QQ哦~")
    elif in_it(sb):
        return ban.finish("唔……全域封禁失败，这个人已经被封禁了。")
    else:
        now = json.loads(read(TOOLS + "/ban.json"))
        now.append(sb)
        write(TOOLS + "/ban.json", json.dumps(now))
        if self_protection:
            return
        await ban.finish(f"好的，已经全域封禁({sb})。")

unban = on_command("unban", priority=5)  # 解封


@unban.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id), 10) == False:
        await ban.finish(error(10))
    sb = args.extract_plain_text()
    if checknumber(sb) is False:
        await ban.finish("不能全域封禁不是纯数字的QQ哦~")
    if sb is False:
        await unban.finish("您输入了什么？")
    if in_it(sb) is False:
        await unban.finish("全域解封失败，并没有封禁此人哦~")
    now = json.loads(read(TOOLS + "/ban.json"))
    for i in now:
        if i == sb:
            now.remove(i)
    write(TOOLS + "/ban.json", json.dumps(now))
    await ban.finish(f"好的，已经全域解封({sb})。")


@preprocess.handle()
async def _(matcher: Matcher, event: Event):
    info = json.loads(read(TOOLS + "/ban.json"))
    if str(event.user_id) in info and checker(str(event.user_id),10) == False:
        matcher.stop_propagation()
    else:
        pass