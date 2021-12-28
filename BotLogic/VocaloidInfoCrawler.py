import requests

import json

import os
import time
import random

from BotLogic import bilibiliDynamicJsonDataParser as Parser
from BotLogic.config import *


def randomNumberGenerator(multiple=10) -> float:
    a = 0.0
    while a < 0.5:
        a = random.random()
    return a * multiple


def crawlerOutInterface(root: str = str(os.getcwd() + "\\")) -> dict:
    localInfo, preErrorList, preErrorMessage = checkLocalInfo(root=root)
    # -------------------*-------------------
    returnInfo, errorMessage = checkLatestInfoAndCompare(root=root, localInfo=localInfo,
                                                         preErrorList=preErrorList, preErrorMessage=preErrorMessage)

    return {"returnInfo": returnInfo, "errorMessage": errorMessage}


def checkLocalInfo(root: str) -> list:
    localInfo = []
    errorMessage = []
    errorList = []

    logger.debug("开始加载本地信息")

    # 启动爬虫，将本地信息存储到localInfo中
    for i in range(len(catchList)):
        # 先检查本地信息是否存在，若不存在则先进行一次爬取
        logger.debug("------检测第" + str(i) + "个对象" + str(catchList[i]) + "------")
        if not os.path.exists(root + "infoLog/user" + str(catchList[i]) + "LatestDynamicInfo.json"):
            logger.debug("缺少当前目标信息，先进行一次捕获")
            catchNews(target=str(catchList[i]), root=root, writeIntoFile=True)
            logger.debug("尝试捕获完成")

        # 将本地数据进行预处理
        try:
            jsonData = Parser.preParsing(root=root, catchTarget=catchList[i])
        except Exception as e:
            logger.exception("数据预处理失败，可能是本地数据存在问题，将重新进行一次目标数据捕获并覆盖原文件，本次循环跳过该对象")
            errorList.append(catchList[i])
            errorMessage.append(e)
            catchNews(target=str(catchList[i]), root=root, writeIntoFile=True)
            logger.debug("覆写尝试完成，覆写了" + str(catchList[i]))
            continue

        # 将预处理后的数据进行一次提取，深入处理
        # 这时候本地的数据可能会报错
        try:
            tempLocalInfo = Parser.dynamicParser(jsonData=jsonData)
        except Exception as e:
            logger.exception("数据解析失败，可能是本地数据存在问题，将重新进行一次目标数据捕获并覆盖原文件，本次循环跳过该对象")
            errorList.append(catchList[i])
            errorMessage.append(e)
            # 本次进行一次覆写，如果在爬虫这里出现了问题，就直接抛出异常，等下次循环再解决
            catchNews(target=str(catchList[i]), root=root, writeIntoFile=True)
            logger.debug("覆写尝试完成")
            continue

        # 最后，能装入localInfo的，一定都是正确的数据，而出过错的对象都在errorList里，在接下来直接跳过
        localInfo.append(tempLocalInfo)
        logger.debug("当前信息装载完毕")
    logger.debug("本地信息加载完毕！")

    return [localInfo, errorList, errorMessage]


def checkLatestInfoAndCompare(root: str, localInfo: list, preErrorList: list,
                              preErrorMessage: list) -> list:
    logger.debug("开始准备爬取最新信息并与本地记录对比")

    returnInfo = []

    # 爬取最新信息，存储到latestInfo中
    for i in range(len(catchList)):
        logger.debug("-----*-----")

        if catchList[i] in preErrorList:
            logger.debug("当前对象：" + str(catchList[i]) + "出过错，没能完成本地信息预载，本次循环跳过")
            continue

        logger.debug("正在爬取第" + str(i) + "个对象：UID-" + str(catchList[i]))
        catchNewsResults = catchNews(target=str(catchList[i]))
        if catchNewsResults is None:
            logger.debug("对当前对象进行爬取时出错，转接下一个")
            continue

        logger.debug("当前对象爬取完毕，进行进一步解析")
        try:
            jsonData = Parser.preParsing(parsingTarget=catchNewsResults)
            tempData = Parser.dynamicParser(jsonData=jsonData)
        except Exception as e:
            logger.exception("出错了，可能是爬取内容出错，或是b站动态页面的json格式发生了改变，请检查当前json文件的解析逻辑")
            preErrorMessage.append(e)
            continue

        if tempData == localInfo[i]:
            logger.debug("same post，pass")
        else:
            logger.debug("having new posts, please waiting for compare")
            cardNumber = 1
            # 此时，已经确定有至少有一条动态不一样，继续对接下来的实时爬取的信息进行解析
            while tempData != localInfo[i] and cardNumber < 8:
                returnInfo.append(tempData)
                tempData = Parser.dynamicParser(jsonData=jsonData, cardNumber=cardNumber)
                cardNumber = cardNumber + 1
            logger.debug("Comparison done, final cardNumber is" + str(cardNumber - 1))
            # 将新内容写入文件
            with open(root + "infoLog/user" + str(catchList[i]) + "LatestDynamicInfo.json", mode="wb") as f:
                f.write(catchNewsResults)
    logger.debug("最新信息加载完毕")

    return [returnInfo, preErrorMessage]


def catchNews(target: str, root: str = "", writeIntoFile=False):
    # global userInfoList
    # dynamicPageCode = dynamicUrlTemplate + "/" + target + "/dynamic"
    dynamicPageList = dynamicListUrlTemplate + target + r"&offset_dynamic_id=0&need_top=1&platform=web"

    # 获取目标对象最新的十条动态信息
    try:
        dynamicPageListData = requests.get(dynamicPageList, headers=headers)
        dynamicPageListData.close()
        # 在获取到后就直接json化，防止出现html代码装入json文件中
        data = dynamicPageListData.content
        # 如果没有任何问题的话，当前获取到的信息已经转换为了字典格式

        # 将json信息写入文件
        if writeIntoFile:
            with open(root + "infoLog/user" + target + "LatestDynamicInfo.json", mode="wb") as f:
                f.write(dynamicPageListData.content)
    except Exception:
        logger.exception("One Problem Occurred in Catch News Function")
        data = None

    time.sleep(randomNumberGenerator())
    # data：binary content
    return data


if __name__ == "__main__":
    print(str(os.getcwd() + "\\"))
    print(crawlerOutInterface())
    # for m in catchList:
    #     catchNews(str(m), "")
    # for m in range(len(catchList)):
    #     print(Parser(str(os.getcwd()) + "\\", m))

# /data/cards/0/card
