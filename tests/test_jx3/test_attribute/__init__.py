from src.tools.dep.common_api import *


def test_fetch():
    task = Jx3PlayerDetailInfo.from_username('破阵子', '烤冷面不加蛋')
    data = asyncio.run(task)
    assert data.user
    assert data.attribute
    task = Jx3PlayerDetailInfo.from_username('斗转星移', '云澈')
    data = asyncio.run(task)
    assert data.user
    assert data.attribute

    filebase_database.Database.save_all()