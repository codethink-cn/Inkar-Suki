from datetime import datetime
from random import randint

async def what2eat():
    hour = datetime.now().strftime("%H")
    hour = int(hour)
    if 3 <= hour <= 10:
        flag = 0
    elif 11 <= hour <= 15:
        flag = 1
    elif 16 <= hour <= 24:
        flag = 2
    elif 0 <= hour <= 2:
        flag = 2
    breakfast = ["面包", "蛋糕", "荷包蛋", "烧饼", "饽饽", "油条", "馄饨", "火腿", "面条", "小笼包", "牢头姐姐做的点心", "玉米粥", "肉包", "山东煎饼", "饺子", "煎蛋", "烧卖", "生煎", "锅贴", "包子", "酸奶", "苹果", "梨", "香蕉", "皮蛋瘦肉粥", "蛋挞", "南瓜粥", "煎饼", "玉米糊", "泡面",
                 "粥", "馒头", "燕麦片", "水煮蛋", "米粉", "豆浆", "牛奶", "花卷", "豆腐脑", "煎饼果子", "小米粥", "黑米糕", "鸡蛋饼", "牛奶布丁", "水果沙拉", "鸡蛋羹", "南瓜馅饼", "鸡蛋灌饼", "奶香小馒头", "汉堡包", "披萨", "八宝粥", "三明治", "蛋包饭", "豆沙红薯饼", "驴肉火烧", "粥", "粢饭糕", "蒸饺", "白粥"]
    lunch = ["盖浇饭", "砂锅", "大排档", "米线", "满汉全席", "西餐", "麻辣烫", "自助餐", "炒面", "快餐", "水果", "西北风", "馄饨", "火锅", "烧烤", "泡面", "速冻水饺", "日本料理", "涮羊肉", "味千拉面", "肯德基", "面包", "扬州炒饭",
             "自助餐", "茶餐厅", "海底捞", "咖啡", "比萨", "麦当劳", "兰州拉面", "沙县小吃", "烤鱼", "海鲜", "铁板烧", "韩国料理", "粥", "快餐", "萨莉亚", "桂林米粉", "东南亚菜", "甜点", "农家菜", "川菜", "粤菜", "湘菜", "本帮菜", "竹笋烤肉"]
    supper = ["盖浇饭", "砂锅", "大排档", "米线", "满汉全席", "西餐", "麻辣烫", "自助餐", "炒面", "快餐", "水果", "西北风", "馄饨", "火锅", "烧烤", "泡面", "速冻水饺", "日本料理", "涮羊肉", "味千拉面", "肯德基", "面包", "扬州炒饭", "自助餐",
              "茶餐厅", "海底捞", "咖啡", "比萨", "麦当劳", "兰州拉面", "沙县小吃", "烤鱼", "海鲜", "铁板烧", "韩国料理", "粥", "快餐", "萨莉亚", "桂林米粉", "东南亚菜", "甜点", "农家菜", "川菜", "粤菜", "湘菜", "本帮菜", "竹笋烤肉"]  # 有什么用？你问我我怎么知道（狗头
    if flag == 0:
        num = randint(0, 59)
        return breakfast[num]
    elif flag == 1:
        num = randint(0, 46)
        return lunch[num]
    else:
        num = randint(0, len(supper)-1)
        return supper[num]
