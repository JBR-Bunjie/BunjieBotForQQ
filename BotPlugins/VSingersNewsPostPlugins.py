from aiocqhttp import MessageSegment
from aiocqhttp.exceptions import NetworkError
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command

import nonebot
from BotLogic import VocaloidInfoCrawler as vic

import datetime
import time

from BotLogic.config import *

__plugin_name__ = 'VsingerNews'
__plugin_usage__ = '用法： 对我说 "HelloWorld"，我会回复 "HelloWorld!ヾ(•ω•`)o"'


@on_command('VsingerNews')  # , permission=perm.SUPERUSER
async def HelloWorld(session: CommandSession):
    await session.send('我会自动播报最新的Vsinger成员的动态的啦!ヾ(•ω•`)o"')


@nonebot.scheduler.scheduled_job('interval', minutes=timeInterval)
async def _():
    bot = nonebot.get_bot()

    # 初始化日志框架
    timeStart = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 任务开始
    logger.info("新循环@" + str(timeStart))
    logger.info("-------------------mission start-------------------")

    # 进入功能核心
    try:
        VsingerNews = vic.crawlerOutInterface("BotLogic/")
        logger.info(VsingerNews)

        # VsingerNews["returnInfo"] 示例；
        # [
        #   {
        #   'dynamicContent': '#非洲のGUMI酱#\n#旧曲重听# 荷包蛋六周年！#洛天依# #COP#\n“这种绝望 每个漆黑深夜 腐蚀着未愈的伤口”\n原曲地址：\nhttps://www.bilibili.com/video/av3402945',
        #   'picAddress': 'images/videoCover/av3402945Cover'
        #   }
        # ]

        if VsingerNews["errorMessage"]:
            logger.debug("在本次循环出现过错误：")
            for i in VsingerNews["errorMessage"]:
                await reportErrorMessage(bot, i, timeStart)

        if not VsingerNews["returnInfo"]:
            logger.debug("已是最新消息")
        else:
            logger.debug("准备装载最新消息")
            for t in VsingerNews["returnInfo"]:
                # t是一个字典：
                    seq = ""
                    for j in t["picAddress"]:
                        seq = seq + MessageSegment.image(j)
                    messageNeedToSend.append(t["dynamicContent"] + "\n" + seq)

        logger.debug("准备发送最新消息")
        for i in groupIdList:
            # 对所有发送组对象发送消息
            for t in messageNeedToSend:
                try:
                    await bot.send_group_msg(group_id=i, message=t)
                    messageNeedToSend.remove(t)
                except Exception as e:
                    logger.exception("Error Occurred in Message Sending")
                    await reportErrorMessage(bot, e, timeStart)
                finally:
                    time.sleep(5)

    except Exception as e:
        logger.exception("Error Occurred")
        await reportErrorMessage(bot, e, timeStart)

    finally:
        logger.success("-------------------mission over-------------------\n")


async def reportErrorMessage(bot, e, timeStart, msg:str=""):
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if msg == "":
        message = "当前轮次执行开始时间：" + timeStart \
                  + "\n当前错误出现时间" + timeNow \
                  + "bot出错了\n类型：" + str(e) \
                  + "\n详细内容见对应日期的log文件"
    else:
        message = "当前轮次执行开始时间：" + timeStart \
                  + "\n当前错误出现时间" + timeNow \
                  + "bot出错了\n类型：" + str(e) \
                  + "\n详细内容见对应日期的log文件" \
                  + "msg：" + msg

    logger.debug("message: " + message)
    await bot.send_private_msg(user_id=1059384125, message=message)
