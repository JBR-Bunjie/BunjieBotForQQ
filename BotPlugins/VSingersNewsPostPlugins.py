import os

from aiocqhttp import MessageSegment
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from BotLogic import VocaloidInfoCrawler as vic

__plugin_name__ = 'VsingerNews'
__plugin_usage__ = '用法： 对我说 "HelloWorld"，我会回复 "HelloWorld!ヾ(•ω•`)o"'

# 发送组对象
# bunjie全体大会：113624942
# 天蓝色的回忆：708968066
groupIdList = [708968066]


@on_command('VsingerNews')  # , permission=perm.SUPERUSER
async def HelloWorld(session: CommandSession):
    await session.send('我会自动播报最新的Vsinger成员的动态的啦!ヾ(•ω•`)o"')


@nonebot.scheduler.scheduled_job('interval', minutes=30)
async def _():
    global groupIdList
    bot = nonebot.get_bot()
    print("新循环")
    # await bot.send_group_msg(group_id=113624942, message="新循环")

    print("进入错误捕捉")
    try:
        VsingerNews = vic.crawlerOutInterface("BotLogic/")
        # VsingerNews = ""
        # VsingerNews示例；
        # [
        #   {
        #   'dynamicContent': '#非洲のGUMI酱#\n#旧曲重听# 荷包蛋六周年！#洛天依# #COP#\n“这种绝望 每个漆黑深夜 腐蚀着未愈的伤口”\n原曲地址：\nhttps://www.bilibili.com/video/av3402945',
        #   'picNumberCount': 1,
        #   'dynamicType': 2,
        #   'picAddress': 'images/videoCover/av3402945Cover'
        #   }
        # ]

        if not VsingerNews:
            print("已是最新消息")
            # await bot.send_private_msg(user_id=1059384125, message="已是最新消息")
            # await bot.send_group_msg(group_id=113624942, message="非洲のGUMI酱#\n#旧曲重听# 荷包蛋六周年！#洛天依# #COP#\n“这种绝望 每个漆黑深夜 腐蚀着未愈的伤口”\n原曲地址：\nhttps://www.bilibili.com/video/av3402945" + MessageSegment.image("https://i1.hdslb.com/bfs/archive/d6096ad8b828efc204c12afc7d086625f3b27f89.jpg"))
            pass
        else:
            print("准备发送最新消息")
            # seq = MessageSegment.image("http://api.mtyqx.cn/api/random.php")
            # # https://i0.hdslb.com/bfs/album/704c7c644ac2292adf587134a9142bd7d10599ce.jpg@320w_320h_1e_1c.webp
            #
            # await bot.send_group_msg(group_id=113624942, message="已是最新消息")
            #
            # print("单图测试")
            # await bot.send_group_msg(group_id=113624942, message=seq)
            #
            # print("单图带字测试")
            # seq = seq + MessageSegment.image("http://api.mtyqx.cn/api/random.php")
            # await bot.send_group_msg(group_id=113624942, message="你好 " + seq)
            for t in VsingerNews:
                # t是一个字典：
                for i in groupIdList:
                    # 对所有发送组对象发送消息
                    seq = ""
                    for j in t["picAddress"]:
                        seq = seq + MessageSegment.image(j)
                    await bot.send_group_msg(group_id=i, message=t["dynamicContent"] + "\n" + seq)

    except CQHttpError as e:
        print("CQHttpError")
        print(e)
        await bot.send_group_msg(group_id=113624942, message="bot出错了, CQHttpError: " + str(e))
        pass
    except Exception as e:
        print("Other Exception Error")
        print(e)
        await bot.send_group_msg(group_id=113624942, message="bot出错了, Other Exception: " + str(e))
        pass

# 这里最主要的就是第 8 行，nonebot.scheduler.scheduled_job() 是一个装饰器，
# 第一个参数是触发器类型（这里是 cron，表示使用 Cron 类型的触发参数）。
# 这里 hour='*' 表示每小时都执行，minute 和 second 不填时默认为 0，也就是说装饰器所装饰的这个函数会在每小时的第一秒被执行。
#
# 除了 cron，还有两种触发器类型 interval 和 date。
# 例如，你可以使用 nonebot.scheduler.scheduled_job('interval', minutes=10) 来每十分钟执行一次任务。
#
# 限于篇幅，这里无法给出太详细的接口介绍，
# nonebot.scheduler 是一个 APScheduler 的 AsyncIOScheduler 对象，因此关于它的更多使用方法，可以参考 APScheduler 的官方文档。

# http://api.mtyqx.cn/api/random.php
