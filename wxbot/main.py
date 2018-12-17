from wxpy import *

bot = Bot()
my_friend = bot.friends().search('秦鹏飞', sex=MALE)[0]
groups = bot.groups()

# 获取用户群聊列表
print("----- 用户群聊列表start")
for g in groups:
    print(g)

# 获取所有的好友信息
print("----- 用户好友列表")
all_friends = bot.friends()
for f in all_friends:
    print (f)
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
