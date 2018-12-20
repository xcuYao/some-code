from wxpy import *
import base64

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Float, LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

bot = Bot()
my_friend = bot.friends().search('秦鹏飞', sex=MALE)[0]
groups = bot.groups()
file_handler = bot.file_helper

# 创建基类
Base = declarative_base()

# 定义映射对象
class WxFriendTable(Base):
    # 表名
    __tablename__ = "wx_friend"
    # 表结构
    id = Column(Integer, primary_key=True)
    remark_name = Column('remark_name', String(20))
    nick_name = Column('nick_name', String(20))
    sex = Column('sex', Integer)
    province = Column('province', String(20))
    city = Column('city', String(20))
    signature = Column('signature', String(120))
    avatar = Column('avatar', LargeBinary(length=(2*32)-1))

# 初始化数据库连接
engine = create_engine('mysql://work:Iwork996.@localhost:3306/work?charset=utf8mb4', echo=False)
# 创建DBSession
DBSession = sessionmaker(bind=engine)
# 创建session ORM映射对象
session = DBSession()

# 关闭数据库连接
def closeDB():
    session.close()

# 保存到数据库
def saveObj(f, avatar):
    friend_obj=WxFriendTable(
            remark_name=f.remark_name,
            nick_name=f.nick_name,
            sex=f.sex,
            province=f .province,
            city=f.city,
            signature=f.signature,
            avatar=avatar
        )
    session.add(friend_obj)
    session.commit()
    print("save " + str(friend_obj.id) + " success.")

# 获取用户群聊列表
print("----- 用户群聊列表start")
for g in groups:
    print(g)

# 获取所有的好友信息
print("----- 用户好友列表")
all_friends = bot.friends()
for idx, f in enumerate(all_friends):
    avatar_path = "/Users/yaoning/Downloads/wx/"+str(idx)+".jpg"
    f.get_avatar(save_path = avatar_path)
    with open(avatar_path, "rb") as fa:
        code64 = base64.b64encode(fa.read())
    print("第[%d]位好友 昵称:%s 备注名:%s 性别:%s 省份:%s 城市:%s 个性签名:%s 微信号:%s 微信ID:%s"%(idx, f.nick_name, f.remark_name, f.sex, f.province, f.city, f.signature, f.alias, f.wxid))
    saveObj(f,code64)
print("----- 共有 %s 位好友"%len(all_friends))

# 捕获指定用户的消息
@bot.register(my_friend)
def reply_my_friend(msg):
    print("捕获到人 [呼吸] 的消息:%s"%msg)
    # return 'received: {} ({})'.format(msg.text, msg.type)

# 捕获指定群的聊天记录
target_group = groups.search('生辰纲')[0]
@bot.register(target_group)
def handler_group_msg(msg):
    print("捕获到群 [生辰纲] 的消息:%s"%msg)

# 
@bot.register()
def print_others(msg):
    print("捕获到余下消息:%s"%msg)

if __name__ == '__main__':
	bot.join()
