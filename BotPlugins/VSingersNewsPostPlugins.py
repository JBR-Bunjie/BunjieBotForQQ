from aiocqhttp import MessageSegment
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
from BotLogic import VocaloidInfoCrawler as vic

import datetime

__plugin_name__ = 'VsingerNews'
__plugin_usage__ = '用法： 对我说 "HelloWorld"，我会回复 "HelloWorld!ヾ(•ω•`)o"'

# 发送组对象
# bunjie全体大会：113624942
# 天蓝色的回忆：708968066
groupIdList = [708968066]

# 定时任务的执行时间间隔
timeInterval = 30


# http://api.mtyqx.cn/api/random.php


async def reportErrorMessage(bot, e, timeStart):
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = "当前轮次执行开始时间：" + timeStart + "当前错误出现时间" + timeNow \
              + "bot出错了\n类型：Other Exception\n详细内容：\n" \
              + "Exception Cause：" + str(e.__cause__) \
              + "\nException Context：" + str(e.__context__) \
              + "\nException TraceBack：" + str(e.__traceback__)

    print(message)
    await bot.send_private_msg(user_id=1059384125, message=message)
    pass


@on_command('VsingerNews')  # , permission=perm.SUPERUSER
async def HelloWorld(session: CommandSession):
    await session.send('我会自动播报最新的Vsinger成员的动态的啦!ヾ(•ω•`)o"')


@nonebot.scheduler.scheduled_job('interval', minutes=timeInterval)
async def _():
    global groupIdList
    bot = nonebot.get_bot()
    print("-------------------mission start-------------------")
    # await bot.send_group_msg(group_id=113624942, message="新循环")

    # # 打印当前时间
    # time1 = datetime.datetime.now()
    # print(time1)
    # 打印按指定格式排版的时间
    timeStart = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("进入错误捕捉")
    try:
        VsingerNews = vic.crawlerOutInterface("BotLogic/")
        print(VsingerNews)
        # VsingerNews = ""
        # VsingerNews["returnInfo"]示例；
        # [
        #   {
        #   'dynamicContent': '#非洲のGUMI酱#\n#旧曲重听# 荷包蛋六周年！#洛天依# #COP#\n“这种绝望 每个漆黑深夜 腐蚀着未愈的伤口”\n原曲地址：\nhttps://www.bilibili.com/video/av3402945',
        #   'picNumberCount': 1,
        #   'dynamicType': 2,
        #   'picAddress': 'images/videoCover/av3402945Cover'
        #   }
        # ]

        if not VsingerNews["errorMessage"]:
            print("本次循环出现错误：")
            for i in VsingerNews["errorMessage"]:
                print(i)
                await reportErrorMessage(bot, i, timeStart)

        if not VsingerNews["returnInfo"]:
            print("已是最新消息")
            pass
        else:
            print("准备发送最新消息")
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
        await reportErrorMessage(bot, e, timeStart)

    except Exception as e:
        print("Other Exception Error")
        await reportErrorMessage(bot, e, timeStart)

    finally:
        print("-------------------mission over-------------------")
