from os import path
import nonebot
import Gloway.bot_config as bot_config

# 发送组对象
groupIdList = [113624942]
# 捕获对象
# 36081646：洛天依
# 406948651：乐正绫
# 156489：刊娘
catchList = [36081646, 406948651, 156489]

# 第一个参数为插件路径，第二个参数为插件前缀（模块的前缀）
nonebot.load_plugins(path.join(path.dirname(__file__), 'BotPlugins'), 'BotPlugins')

# # 如果使用 wsgi
# bot = nonebot.get_bot()
# app = bot.asgi

if __name__ == '__main__':
    nonebot.init(bot_config)
    nonebot.load_builtin_plugins()
    nonebot.run()
