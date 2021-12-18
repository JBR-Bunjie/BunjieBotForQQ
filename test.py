from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import requests
import time
import urllib
from lxml import etree
from aiocqhttp import MessageSegment
import requests
from config import IMAGE_LOCAL

class GetPic:
    def __init__(self):
        self.session = requests.session()

    def get_Pic(self):
        res = self.session.get("http://api.mtyqx.cn/api/random.php", verify=False)

        # 保存图片
        with open(IMAGE_LOCAL.format('8531'), "wb") as f:
            f.write(res.content)
        return True

@on_command('setu', aliases=('富婆','色图', '老婆', '老婆图', '萝莉'))
async def setu(session: CommandSession):
    Pic = GetPic()
    if Pic.get_Pic():
        seq = MessageSegment.image("{}.png".format('8531'))
        await session.send(seq)

@on_natural_language(keywords={'富婆','色图', '老婆', '老婆图', '萝莉'},only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    # 对消息进行分词和词性标注
    words = posseg.lcut(stripped_msg)

    pic = None
    # 遍历 posseg.lcut 返回的列表
    for word in words:
        # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
        if word.flag == 'st':
            pic = word.word
            break

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'setu', current_arg=pic)