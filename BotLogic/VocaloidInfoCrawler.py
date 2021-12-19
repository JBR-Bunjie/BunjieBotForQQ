import datetime
from typing import Dict, Any

import requests
from requests.adapters import HTTPAdapter

import json
import os

import time
import random
from BotLogic import bilibiliDynamicJsonDataParser as Parser

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

# 暂存动态内容，根据catchList顺序来存储
# 初次启动时读取文件中存好的动态
userInfoList = []


def catchNews(target: str, parentFolderPath: str) -> Dict[str, Any]:
    # global userInfoList
    # dynamicPageCode = dynamicUrlTemplate + "/" + target + "/dynamic"
    dynamicPageList = dynamicListUrlTemplate + target + r"&offset_dynamic_id=0&need_top=1&platform=web"

    # 获取目标对象最新的十条动态信息
    try:
        dynamicPageListData = requests.get(dynamicPageList, headers=headers)
        dynamicPageListData.close()
        # 将信息写入文件
        with open(parentFolderPath + "infoLog/user" + target + "LatestDynamicInfo.json", mode="wb") as f:
            f.write(dynamicPageListData.content)
        time.sleep(random.random() * 5)
        return json.loads(dynamicPageListData.content)
    except Exception as e:
        print(e)
        dynamicPageList = {}
        return dynamicPageList


def crawlerOutInterface(parentFolderPath: str):
    # global userInfoList
    # 若userInfoList为空，则必为重新启动了项目，需要从已有json文件中读取info

    # 设立返回值列表，若userInfoList和爬虫的最新数据不符，就立即更新userInfoList并返回新值
    returnInfo = []

    # 本地数据
    localFilesInfo = []

    # 错误对象
    errorList = []
    errorMessage = []

    print("开始加载本地信息")
    # 启动爬虫，将本地信息存储到localFilesInfo中
    for i in range(len(catchList)):
        # 先检查本地信息是否存在，若不存在则先进行一次爬取
        if not os.path.exists(parentFolderPath + "infoLog/user" + str(catchList[i]) + "LatestDynamicInfo.json"):
            print("缺少当前目标信息，先进行一次捕获，本次的对象为：" + str(catchList[i]))
            result = catchNews(target=str(catchList[i]), parentFolderPath=parentFolderPath)
            if result == {}:
                print("爬虫出错，本次循环跳过这个对象")
                errorList.append(catchList[i])
                continue

            print("当前信息添加完毕")

        jsonData = Parser.preParsing(parentFolderPath=parentFolderPath, catchTarget=catchList[i])
        print("第" + str(i) + "条信息预处理完毕，进行信息装载")
        localFilesInfo.append(Parser.dynamicParser(jsonData=jsonData))
        print("当前信息装载完毕")
    print("本地信息加载完毕！")

    print("开始准备爬取最新信息")
    # 爬取最新信息，存储到latestInfo中
    for i in range(len(catchList)):
        if catchList[i] in errorList:
            print("当前对象：" + str(catchList[i]) + "出过错，跳过该对象")
            continue

        print("-----*-----")
        print("正在爬取对象：UID-" + str(catchList[i]))
        catchNewsResults = catchNews(target=str(catchList[i]), parentFolderPath=parentFolderPath)
        if catchNewsResults == {}:
            print("对当前对象进行爬取时出错，转接下一个")
            errorMessage.append(str(datetime.time) + "时出错，对象为：" + str(catchList[i]))
            continue

        print("当前对象爬取完毕，进行进一步解析")
        jsonData = Parser.preParsing(parsingTarget=catchNewsResults)
        tempData = Parser.dynamicParser(jsonData=jsonData)

        if tempData == localFilesInfo[i]:
            print("same post，pass")
            pass
        else:
            print("having new post, please waiting for compare")
            cardNumber = 1
            while tempData != localFilesInfo[i]:
                # 此时，已经确定有至少有一条动态不一样，继续对接下来的实时爬取的信息进行解析
                returnInfo.append(tempData)
                tempData = Parser.dynamicParser(jsonData=jsonData, cardNumber=cardNumber)
                cardNumber = cardNumber + 1

        print("第" + str(i) + "条信息解析完毕")
    print("最新信息加载完毕")

    return returnInfo


if __name__ == "__main__":
    print(str(os.getcwd() + "\\"))
    print(crawlerOutInterface(str(os.getcwd() + "\\")))
    # for m in catchList:
    #     catchNews(str(m), "")
    # for m in range(len(catchList)):
    #     print(Parser(str(os.getcwd()) + "\\", m))

# /data/cards/0/card

# https://space.bilibili.com/36081646/dynamic

# https://weibo.com/u/3206936735
# https://weibo.com/u/6077799204
# https://weibo.com/u/6077799204?display=0&retcode=6102
