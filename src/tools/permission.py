from typing import Union, Any

from src.tools.database import group_db, Permission

def get_all_admin() -> Permission:
    data: Union[Permission, Any] = group_db.where_one(Permission(), default=Permission())
    return data

def judge(user_id: str) -> bool:
    data = get_all_admin()
    permission = data.permissions_list
    return user_id in permission

def checker(user_id: str, level: int):
    data = get_all_admin()
    data = data.permissions_list
    return False if user_id not in data else int(data[user_id]) >= level

def error(level):
    return f"唔……你权限不够哦，这条命令要至少{level}的权限哦~"