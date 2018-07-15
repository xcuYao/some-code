import requests
import re
import json
import time
import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建基类
Base = declarative_base()


# 定义映射对象
class ZhixiaoTable(Base):
    # 表名
    __tablename__ = "zhixiao"
    # 表结构
    id = Column(Integer, primary_key=True)
    icon_url = Column('icon_url', String(20))
    app_name = Column('app_name', String(20))
    app_author = Column('app_author', String(20))
    app_pv_num = Column('app_pv_num', Integer)
    app_collect_num = Column('app_collect_num', Integer)
    app_tags = Column('app_tags', String(20))
    publish_time = Column('publish_time', DateTime)
    app_qr_code_addr = Column('app_qr_code_addr', String(20))
    screenshots = Column('screenshots', Text)
    app_intro = Column('app_intro', Text)
    star_value = Column('star_value', Float)
    star_num = Column('star_num', Integer)
    source_id = Column('source_id', Integer)
    create_time = Column('create_time', DateTime)


# 初始化数据库连接
engine = create_engine('mysql://username:password@localhost:3306/work?charset=utf8mb4', echo=False)

# 创建DBSession
DBSession = sessionmaker(bind=engine)

# 创建session ORM映射对象
session = DBSession()


# 关闭数据库连接
def closeDB():
    session.close()


# 抓取
def crawl(targetId):
    rsp = requests.get('https://minapp.com/api/v5/trochili/miniapp/' +
                       str(targetId) + '/')
    if rsp.status_code != 200:
        print("get " + str(targetId) + " error:" + str(rsp.status_code))
        return
    saveDB(rsp.content)


# 存储
def saveDB(jsonString):
    object = json.loads(jsonString)
    tags = []
    for tag in object['tag']:
        tags.append(tag['name'])
    screenshots = []
    for screenshot in object['screenshot']:
        screenshots.append(screenshot['image'])
    star_num = 0
    star_total = 0
    star_avg = 0
    for idx, value in enumerate(object['rating']):
        star_total += value * (idx + 1)
        star_num += value
    classify = ','.join(tags)
    screenshots = ','.join(screenshots)

    if star_num == 0:
        star_avg = 0
    else:
        star_avg = star_total / star_num

    zx_obj = ZhixiaoTable(
        icon_url=object['icon']['image'],
        app_name=object['name'],
        app_author=object['created_by'],
        app_pv_num=object['visit_amount'],
        app_tags=object['created_by'],
        publish_time=datetime.datetime.fromtimestamp(object['created_at']),
        app_qr_code_addr=object['qrcode']['image'],
        screenshots=screenshots,
        app_intro=object['description'],
        star_value=star_avg,
        star_num=star_num,
        source_id=object['id'],
        create_time=datetime.datetime.fromtimestamp(time.time()))
    session.add(zx_obj)
    session.commit()
    print("save " + str(object['id']) + " success name:" + object['name'])


def main():
    f = open('./error_index.txt', 'a+')
    for index in range(100, 7839):
        try:
            crawl(index)
        except:
            f.write(str(index) + '\n')
            print('handler error with ' + str(index))
        else:
            time.sleep(1)
    print("zhixiao data all over!")

    closeDB()


if __name__ == '__main__':
    main()
