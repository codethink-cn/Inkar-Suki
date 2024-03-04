from src.tools.basic import *
from src.tools.generate import generate, get_uuid
from src.tools.config import Config
from src.tools.file import read, write
import json
import os

from pathlib import Path
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment as ms
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from tabulate import tabulate


"""
帮助文件生成函数。

包含文字 + 图片信息。

文字来源于内置，图片由每个`plugin`文件夹下的`info.json`中的内容整合，再以`selenium`进行渲染所得。
"""

help = on_command("help", aliases={"帮助", "功能", "查看", "文档", "使用说明"}, priority=5)
css = """
<style>
            ::-webkit-scrollbar 
            {
                display: none;   
            }
            table 
            { 
                border-collapse: collapse; 
            } 
            table, th, td
            { 
                border: 1px solid rgba(0,0,0,0.05); 
                font-size: 0.8125rem; 
                font-weight: 500; 
            } 
            th, td 
            { 
                padding: 15px; 
                text-align: left; 
            }
            @font-face
            {
                font-family: Custom;
                src: url("customfont");
            }
</style>"""
css = css.replace("customfont", Config.font_path)
path = PLUGINS


@help.handle()
async def help_():
    await help.finish(f"Inkar Suki · 音卡使用文档：\nhttps://inkar-suki.codethink.cn/Inkar-Suki-Docs/#/")