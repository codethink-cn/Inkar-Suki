import sys
from pathlib import Path

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import CommandArg

TOOLS = Path(__file__).resolve().parent.parent.parent / "tools"
sys.path.append(str(TOOLS))
from permission import checker, error
from http_ import http

sign = on_command("sign", aliases={"公告"}, priority=5)


@sign.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id), 10) == False:
        sign.finish(error(10))
    cmd = args.extract_plain_text()
    groups = await bot.call_api("get_group_list")
    for i in groups:
        await bot.call_api("send_group_msg",group_id=i["group_id"],message=f"[开发者全域公告]{cmd}")
        
call_api = on_command("call_api",aliases={"api"},priority=5)
@call_api.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await call_api.finish(error(10))
    cmd = args.extract_plain_text()
    await http.get_url(f"http://127.0.0.1:2334/{cmd}",300)