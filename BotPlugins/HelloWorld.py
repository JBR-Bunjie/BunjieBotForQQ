from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from nonebot import permission as perm
from nonebot.message import unescape

__plugin_name__ = 'HelloWorld'
__plugin_usage__ = '用法： 对我说 "HelloWorld"，我会回复 "HelloWorld!ヾ(•ω•`)o"'


@on_command('HelloWorld')  # , permission=perm.SUPERUSER
async def HelloWorld(session: CommandSession):
    await session.send('HelloWorld!ヾ(•ω•`)o"')


@on_command('checkInfo')
async def crawler(session: CommandSession):
    await session.send("")


# # 将函数注册为群成员增加通知处理器
# @on_notice('group_increase')
# async def _(session: NoticeSession):
#     # 发送欢迎消息
#     await session.send('欢迎新朋友～')


# def sendLatestMessage(session: CommandSession):
#     await session.send()
