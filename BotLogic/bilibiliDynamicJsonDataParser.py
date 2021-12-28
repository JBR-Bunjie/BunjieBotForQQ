# 解析的内容直接来源于；
# https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=0&host_uid=

import json
import os
import time
import random
import requests

global jsonData


def preParsing(root=None, catchTarget=None, parsingTarget=None):
    if parsingTarget is None:
        # 即root and catchTarget == Not None
        # 此时解析本地保存好的文件
        with open(root + "infoLog\\user" + str(catchTarget) + "LatestDynamicInfo.json", mode="r",
                  encoding="utf8") as f:
            jsonDataInPreParse = f.read()

        jsonDataInPreParse = json.loads(jsonDataInPreParse)
    else:
        jsonDataInPreParse = json.loads(parsingTarget.decode("utf8"))
    return jsonDataInPreParse


def differenceJudge(localData, latestData):
    pass


#
# def topDynamicParser(jsonData: dict) -> dict:
#     if jsonData["data"]["cards"][0]["extra"]["is_space_top"] == 1:
#         # 该用户存在置顶动态，这条动态我们单独匹配
#         topDynamicParser(jsonData["data"]["cards"][0]["card"])


def dynamicParser(jsonData: dict, cardNumber=0) -> dict:
    # 一些需要用到的返回值变量，做一次事先声明
    picAddress = []
    path = os.getcwd()

    # ------------------------*------------------------
    # 读取已有信息完毕，准备进行解析：
    # ------------------------*------------------------
    if jsonData["data"]["cards"][0]["extra"]["is_space_top"] == 1:
        # 该用户存在置顶动态，这条动态我们单独匹配
        # 仍未实现：12/18/2021
        jsonDataCard = json.loads(jsonData["data"]["cards"][cardNumber+1]["card"])
    else:
        # 该用户不存在置顶动态，这条动态我们直接捕获
        jsonDataCard = json.loads(jsonData["data"]["cards"][cardNumber]["card"])

    # 还没有处理音频投稿与转发、专栏投稿与转发的情况
    if list(jsonDataCard.keys())[0] == "aid":
        # 投稿了视频动态：
        # 组织机器人消息格式
        dynamicContent = "#" + jsonDataCard["owner"]["name"] + "#\n" + jsonDataCard[
            "dynamic"] + "\n" + "https://www.bilibili.com/video/av" + str(jsonDataCard["aid"])
        # 爬取视频的封面图片
        picUrl = jsonDataCard["pic"]
        picAddress.append(picUrl)

    elif list(jsonDataCard.keys())[0] == "item":
        # 投稿了日常动态：
        # 组织机器人消息格式
        dynamicContent = "#" + jsonDataCard["user"]["name"] + "#\n" + jsonDataCard["item"]["description"]
        # 爬取日常动态下的图片
        picUrl = jsonDataCard["item"]["pictures"]
        picNumberCount = len(picUrl)
        for i in range(picNumberCount):
            picAddress.append(picUrl[i]["img_src"])

    else:
        # 纯文字动态
        if "origin" not in jsonDataCard:
            dynamicContent = "#" + jsonDataCard["user"]["uname"] + "#\n" + jsonDataCard["item"]["content"]
            picAddress = []
        # 转发动态
        # 可能会套娃，暂时跳过，目前只处理了当前用户内容和原生内容
        else:
            originDynamic = json.loads(jsonDataCard["origin"])
            if list(originDynamic.keys())[0] == "aid":
                # 转发的是视频
                # 组织机器人消息格式
                dynamicContent = "#" + jsonDataCard["user"]["uname"] + "#\n" + jsonDataCard["item"][
                    "content"] + "\n" + "原曲地址：\n" + "https://www.bilibili.com/video/av" + str(originDynamic["aid"])
                # 爬取原曲封面
                picUrl = originDynamic["pic"]
                picAddress.append(picUrl)

            else:
                # 转发的是别人的日常动态
                # 组织机器人消息格式
                dynamicContent = "#" + jsonDataCard["user"]["uname"] + "#\n" + jsonDataCard["item"][
                    "content"] + "\n" + "-------*-------\n" + "#" + originDynamic["user"]["name"] + "#\n" + \
                                 originDynamic["item"]["description"]
                # 爬取视频的封面图片
                picUrl = originDynamic["item"]["pictures"]
                picNumberCount = len(picUrl)
                for i in range(picNumberCount):
                    picAddress.append(picUrl[i]["img_src"])

    return {
        "dynamicContent": dynamicContent,
        "picAddress": picAddress,
    }


def dynamicParserWithPicturesDownload(jsonData: dict, root: str, catchTarget: int, headers: dict) -> dict:
    # 一些需要用到的返回值变量，做一次事先声明
    dynamicContent = ""
    picAddress = []
    path = os.getcwd()

    # ------------------------*------------------------
    # 读取已有信息完毕，准备进行解析：
    # ------------------------*------------------------
    if jsonData["data"]["cards"][0]["extra"]["is_space_top"] == 1:
        # 该用户存在置顶动态，这条动态我们单独匹配
        # 当前先跳过：2021/12/17
        jsonDataCard = json.loads(jsonData["data"]["cards"][1]["card"])
    else:
        # 该用户不存在置顶动态，这条动态我们直接捕获
        jsonDataCard = json.loads(jsonData["data"]["cards"][0]["card"])

    if list(jsonDataCard.keys())[0] == "aid":
        # 投稿了视频动态：
        dynamicType = 0
        # 组织机器人消息格式
        dynamicContent = "#" + jsonDataCard["owner"]["name"] + "#\n" + jsonDataCard[
            "dynamic"] + "\n" + "https://www.bilibili.com/video/av" + str(jsonDataCard["aid"])
        # 爬取视频的封面图片
        picUrl = jsonDataCard["pic"]
        if not os.path.exists("images/videoCover/av" + str(jsonDataCard["aid"]) + "Cover" + ".png"):
            res = requests.get(url=picUrl, headers=headers)
            with open(root + "images/videoCover/av" + str(jsonDataCard["aid"]) + "Cover" + ".png",
                      mode="wb") as f:
                f.write(res.content)
        picAddress.append(picUrl)

    elif list(jsonDataCard.keys())[0] == "item":
        # 投稿了日常动态：
        dynamicType = 1
        # 组织机器人消息格式
        dynamicContent = "#" + jsonDataCard["user"]["name"] + "#\n" + jsonDataCard["item"]["description"]
        # 爬取日常动态下的图片
        picUrl = jsonDataCard["item"]["pictures"]
        picNumberCount = len(picUrl)
        for i in range(picNumberCount):
            # if not os.path.exists("images/dailyDynamicPic/pic" + str(i) + ".png"):
            res = requests.get(url=picUrl[i]["img_src"], headers=headers)
            with open(root + "images/dailyDynamicPic/pic" + str(catchTarget) + str(i) + ".png",
                      mode="wb") as f:
                f.write(res.content)
            time.sleep(random.random() * 5)
            picAddress.append(picUrl[i]["img_src"])

    else:
        # 转发可能会套娃，需要递归解决
        # 暂时跳过，目前只处理了当前用户内容和原生内容
        originDynamic = json.loads(jsonDataCard["origin"])
        if list(originDynamic.keys())[0] == "aid":
            # 如果转发的是视频
            dynamicType = 2
            # 组织机器人消息格式
            dynamicContent = "#" + jsonDataCard["user"]["uname"] + "#\n" + jsonDataCard["item"][
                "content"] + "\n" + "原曲地址：\n" + "https://www.bilibili.com/video/av" + str(originDynamic["aid"])
            # 爬取原曲封面
            picUrl = originDynamic["pic"]
            if not os.path.exists("images/videoCover/av" + str(originDynamic["aid"]) + "Cover" + ".png"):
                res = requests.get(url=picUrl, headers=headers)
                with open(root + "images/videoCover/av" + str(originDynamic["aid"]) + "Cover" + ".png",
                          mode="wb") as f:
                    f.write(res.content)
            picAddress.append(picUrl)

        else:
            # 如果转发的是别人的日常动态
            dynamicType = 3
            # 组织机器人消息格式
            dynamicContent = "#" + jsonDataCard["user"]["uname"] + "#\n" + jsonDataCard["item"][
                "content"] + "\n" + "-------*-------\n" + "#" + originDynamic["user"]["name"] + "#\n" + \
                             originDynamic["item"]["description"]
            # 爬取视频的封面图片
            picUrl = originDynamic["item"]["pictures"]
            picNumberCount = len(picUrl)
            for i in range(picNumberCount):
                # if not os.path.exists("images/dailyDynamicPic/pic" + str(i) + ".png"):
                res = requests.get(url=picUrl[i]["img_src"], headers=headers)
                with open(root + "images/dailyDynamicPic/pic" + str(catchTarget) + str(i) + ".png",
                          mode="wb") as f:
                    f.write(res.content)
                time.sleep(random.random() * 5)
                picAddress.append(picUrl[i]["img_src"])

    print(picAddress)
    return {
        "dynamicContent": dynamicContent,
        "dynamicType": dynamicType,
        "picAddress": picAddress,
    }
