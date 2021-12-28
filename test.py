from loguru import logger
import json
import requests

# dynamicPageList = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=36081646&offset_dynamic_id=0&need_top=1&platform=web"
#
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41",
#     'Connection': 'close',
# }
#
# try:
#     dynamicPageListData = requests.get(dynamicPageList, headers=headers)
#     dynamicPageListData.close()
#     a = dynamicPageListData.content.decode('utf8')
#     # 将json信息写入文件
#     with open("Test.json", mode="wb") as f:
#         f.write(dynamicPageListData.content)
#     print("yes!")
#     with open("Test.json", mode="w", encoding="utf8") as f:
#         f.write(a)
# except Exception:
#     logger.exception("One Problem Occurred in Catch News Function")

logger.add("Test.log", encoding="utf8")
logger.add("Test.log", encoding="utf8")
logger.remove()
logger.add("Test.log", encoding="utf8")
logger.debug("two sentences")

# import traceback
#
# from loguru import logger
#
# logger.add("sys.stderr", backtrace=True, diagnose=True)  # Caution, may leak sensitive data in prod
#
# global b
#
#
# def func(a, b):
#     return a / b
#
#
# @logger.catch
# def nested(c):
#     try:
#         func(5, c)
#     except ZeroDivisionError as e:
#         b = e
#         message = traceback.format_exc()
#         print(message)
#         logger.exception("what?")
#
#
# nested(0)
