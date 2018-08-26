import requests
from bypy import ByPy

bypy = ByPy()


def crawl(targetId):
    print("-- target " + str(targetId))
    # 下载网页
    rsp = requests.get(
        "https://boxueio.com/series/antlr-basics/episode/" + str(targetId))
    print(rsp.content)

    

    # 找出视频描述json

    # 解析出视频地址

    # 下载视频到指定目录

    # 转码压缩为mp4

    # 同步到百度网盘


def main():
    print(" --- hello ---")
    # bypy.list()
    # bypy.mkdir("iPython/test1")

    for index in range(1, 2):
        try:
            crawl(index)
        except Exception as e:
            print("handler error with " + str(index) + " " + str(e))
            pass

    pass


if __name__ == '__main__':
    main()
