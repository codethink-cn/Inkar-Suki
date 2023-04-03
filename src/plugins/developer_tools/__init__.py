import os
import sys
import psutil
import nonebot
import json
import time
from nonebot import on_command, on_message
from nonebot.adapters import Message
from nonebot.params import CommandArg, Arg
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageSegment, unescape, Event, Bot, GroupMessageEvent
from nonebot.typing import T_State
from typing import List
from pathlib import Path
from functools import reduce
TOOLS = nonebot.get_driver().config.tools_path
sys.path.append(str(TOOLS))
CACHE = TOOLS[:-5] + "cache"
from permission import checker, error
from file import read, write
from config import Config
from utils import get_url, get_status, checknumber, data_post
from generate import generate
from .example import *
from config import Config

helpimg = on_command("helpimg", aliases={"hi"}, priority=5)


@helpimg.handle()
async def _(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id), 9) == False:
        await helpimg.finish(error(10))
    size = args.extract_plain_text()
    if size:
        if size.find("x"):
            write(Config.size,size)
            await helpimg.finish("好的~图片尺寸已修改为"+size+"。")
        else:
            await helpimg.finish("唔，这尺寸不对哦~")
    else:
        await helpimg.finish("唔，你忘记输入尺寸了啦！")
    
imgsize = on_command("imgsize",aliases={"is"},priority=5)

@imgsize.handle()
async def __(bot: Bot, event: Event):
    if checker(str(event.user_id),9) == False:
        await imgsize.finish(error(9))
    size = read(Config.size)
    await imgsize.finish("查到啦！当前图片尺寸为"+size+"。")
purge = on_command("purge",priority=5)

@purge.handle()
async def ___(event: Event):
    if checker(str(event.user_id),1) == False:
        await purge.finish(error(1))
    try:
        for i in os.listdir(CACHE):
            os.remove(CACHE+"/"+i)
    except:
        await purge.finish("部分文件并没有找到哦~")
    else:
        await purge.finish("好的，已帮你清除图片缓存~")

shutdown = on_command("shutdown",aliases={"poweroff"},priority=5)

@shutdown.handle()
async def ____(event: Event):
    if checker(str(event.user_id),10) == False:
        await shutdown.finish(error(10))
    await shutdown.send("请稍候，正在关闭中……")
    await shutdown.send("关闭成功！请联系Owner到后台手动开启哦~")
    sys.exit(0)

restart = on_command("restart",priority=5)
@restart.handle()
async def _(event: Event):
    with open("./src/plugins/developer_tools/example.py",mode="w") as cache:
        if checker(str(event.user_id),5) == False:
            await restart.finish(error(5))
        await  restart.send("好啦，开始重启，整个过程需要些许时间，还请等我一下哦~")
        cache.write("status=\"OK\"")

echo = on_command("echo",priority=5)
@echo.handle()
async def echo_(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),9) == False:
        await echo.finish(error(9))
    await echo.finish(args)

say = on_command("say",priority=5)
@say.handle()
async def say_(event: Event, args: Message = CommandArg()): 
    def _unescape(message: Message, segment: MessageSegment):
        if segment.is_text():
            return message.append(unescape(str(segment)))
        return message.append(segment)
    if checker(str(event.user_id),9) == False:
        await say.finish(error(9))
    message = reduce(_unescape, args, Message())
    await say.finish(message)

ping = on_command("ping", aliases={"-测试"}, priority=5)
@ping.handle()
async def _(event: Event):
    ikv = await Config.version()
    if checker(str(event.user_id),1) == False:
        times = str("现在是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f"\n当前版本{ikv}\n(Nonebot {Config.nonebot})")
        await ping.finish(times)
    def per_cpu_status() -> List[float]:
        return psutil.cpu_percent(interval=1, percpu=True)
    def memory_status() -> float:
        return psutil.virtual_memory().percent
    times = str("现在是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f"\n当前版本{ikv}\n(Nonebot {Config.nonebot})")
    msg = f"来啦！\n系统信息如下：\nCPU占用：{str(per_cpu_status()[0])}%\n内存占用：{str(memory_status())}%\n"
    await ping.finish(msg + times)

back = on_command("back", priority=5)
@back.handle()
async def back_(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id), 10) == False:
        await back.finish(error(10))
    os.system(args.extract_plain_text())
    await back.finish("好啦，执行完毕！")

front = on_command("front",priority=5)
@front.handle()
async def front_(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await front.finish(error(10))
    msg = os.popen(args.extract_plain_text()).read()
    if msg == "":
        msg = "执行完成，但没有输出哦~"
    await front.finish(f"{msg}")

post = on_command("post", aliases={"-公告"}, priority=5)
@post.handle()
async def _(bot: Bot, event: Event, args: Message = CommandArg()):
    if str(event.user_id) not in Config.owner:
        await post.finish("唔……只有机器人主人可以使用该命令哦~")
    cmd = args.extract_plain_text()
    groups = await bot.call_api("get_group_list")
    for i in groups:
        await bot.call_api("send_group_msg",group_id=i["group_id"],message=cmd)

call_api = on_command("call_api",aliases={"api"},priority=5)
@call_api.handle()
async def _(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await call_api.finish(error(10))
    cmd = args.extract_plain_text()
    await get_url(f"{Config.cqhttp}{cmd}")

git = on_command("git",priority=5)
@git.handle()
async def _(event: Event, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await call_api.finish(error(10))
    output = ""
    commit = args.extract_plain_text()
    if commit == "pull":
        output = os.popen("git pull").read()
        await git.finish(output)
    os.system("git add .")
    msg = ""
    msg = msg + os.popen("git commit -m \""+commit+"\"").read()
    msg = msg + os.popen("git push").read()
    if msg == "":
        msg = "执行完成，但没有输出哦~"
    await git.finish(msg)

voice = on_command("voice", priority=5)
@voice.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await call_api.finish(error(10))
    sth = args.extract_plain_text()
    final_msg = f"[CQ:tts,text={sth}]"
    await bot.call_api("send_group_msg",group_id=event.group_id,message=final_msg)
    
web = on_command("web",priority=5)
@web.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if checker(str(event.user_id),10) == False:
        await call_api.finish(error(10))
    data = args.extract_plain_text().split(" ")
    if len(data) != 2:
        await web.finish("至少需要两个参数哦，请检查后重试~")
    url = data[0]
    size = data[1]
    if await get_status(url) not in [200,301,302]:
        await web.finish("唔……网站图片获取失败。\n原因：响应码非200，请检查是否能正常访问。")
    else:
        image = generate(url,2,size,True)
        await web.finish("获取图片成功！\n"+MessageSegment.image(Path(image).as_uri()))

apply = on_command("apply", aliases={"-申请"}, priority=5)
@apply.handle()
async def _(state: T_State, event: Event):
    applier = str(event.user_id)
    state["user"] = applier
    return

@apply.got("group", prompt="感谢您申请使用Inkar Suki，接下来请发送您所为之申请的群聊的群号。")
async def _(bot: Bot, state: T_State, group: Message = Arg()):
    group_id = group.extract_plain_text()
    if checknumber(group_id) == False:
        await apply.finish("输入的内容有误，申请失败。")
    else:
        try:
            data = json.dumps(await bot.call_api("get_group_info", group_id=int(group_id)), ensure_ascii=False)
        except:
            data = "获取失败！"
        url = "https://api.github.com/repos/codethink-cn/Inkar-Suki/issues"
        token = Config.ght
        user = state["user"]
        bearer = "Bearer " + token
        final_header = {"Accept": "application/vnd.github+json","Authorization":bearer,"X-GitHub-Api-Version":"2022-11-28"}
        body = {"title":f"Inkar-Suki·使用申请","body":f"申请人QQ：{user}\n申请群聊：{group_id}\n群聊请求数据如下：```{data}```","labels":["申请"]}
        resp = await data_post(url, headers = final_header, json=body)
        logger.info(resp)
        await apply.finish("申请成功，请求已发送至GitHub，请等待通知！")