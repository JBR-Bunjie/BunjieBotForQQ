from loguru import logger

logFileName = "logs/botReport.log"
logger.add(logFileName, rotation="daily", encoding="utf8", backtrace=True, diagnose=True)


# 发送组对象
# bunjie全体大会：113624942
# 天蓝色的回忆：708968066
# 714888277
groupIdList = [708968066]

messageNeedToSend = []

# 定时任务的执行时间间隔
timeInterval = 30

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41",
    'Connection': 'close',
}

# b站个人空间开头地址
dynamicUrlTemplate = "https://space.bilibili.com"
# b站前十条动态分页请求地址
dynamicListUrlTemplate = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid="

# 捕获对象
# 36081646：luo
# 406948651：ling
# 156489：刊娘
# 399918500：miku
# 406950978：mo
# 406949083：moke
# 406948276: yanhe
# 10878474：vsinger团队
# 406948857: longya
# 34727551：luo站
# 347392364：ling站
# 2720641：z新豪
catchList = [36081646, 406948651, 156489, 399918500, 406950978, 406949083, 406948276, 10878474, 406948857, 2720641]


# http://api.mtyqx.cn/api/random.php

# https://space.bilibili.com/36081646/dynamic

# https://weibo.com/u/3206936735
# https://weibo.com/u/6077799204
# https://weibo.com/u/6077799204?display=0&retcode=6102
