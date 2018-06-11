import pandas as pd
import time
import seaborn as sns 
import matplotlib.pyplot as plt
import datetime
import numpy as np
import re
from operator import itemgetter
from matplotlib.font_manager import *#导入这个包，可以添加中文字体
import xlwt

chat_file = '自己的csv文件'
myGirl = '目标联系人的微信号'

''' 读取原数据 '''
chat = pd.read_csv(chat_file, sep=',', usecols=[6,7,8])
chat_time = []
chat_content = []
chat_all = []
for i in range(len(chat)-1):
    content = chat[i:i+1]
    if content['talker'].values[0] == myGirl:
        t = content['createTime'].values[0]//1000
        c = content['content'].values[0]
        chat_time.append(t)
        chat_content.append(c)
        chat_all.append([t,c])
chat_all = sorted(chat_all, key=itemgetter(0))#以第一维为索引排序

''' 转换时间格式 '''        
def to_hour(t):
    struct_time = time.localtime(t)
    hour = round((struct_time[3] + struct_time[4] / 60), 2)
    return hour
hour_set = [to_hour(i) for i in chat_time]

print('\n.......................\n开始画图\n.......................')
from matplotlib.font_manager import *#如果想在图上显示中文，需导入这个包
myfont = FontProperties(fname=r'C:\Windows\Fonts\MSYH.TTC',size=22)#标题字体样式
myfont2 = FontProperties(fname=r'C:\Windows\Fonts\MSYH.TTC',size=18)#横纵坐标字体样式
sns.set_style('darkgrid')#设置图片为深色背景且有网格线
sns.distplot(hour_set, 24, color='lightcoral')
plt.xticks(np.arange(0, 25, 1.0), fontsize=15)
plt.yticks(fontsize=15)
plt.title('聊天时间分布', fontproperties=myfont)
plt.xlabel('时间段', fontproperties=myfont2)
plt.ylabel('聊天时间分布', fontproperties=myfont2)
fig = plt.gcf()
fig.set_size_inches(15,8)
fig.savefig('chat_time.png',dpi=100)
plt.show() 
print('\n.......................\n画图结束\n.......................')

''' 聊天时段分布 '''
print('\n.......................\n开始聊天时段统计\n.......................')
time_slice = [0,0,0,0,0,0]
deep_night = []
for i in range(len(hour_set)):
    if hour_set[i]>=2 and hour_set[i]<6:
        time_slice[0] += 1
        deep_night.append([chat_time[i], chat_content[i]])
    elif hour_set[i]>=6 and hour_set[i]<10:
        time_slice[1] += 1
    elif hour_set[i]>=10 and hour_set[i]<14:
        time_slice[2] += 1
    elif hour_set[i]>=14 and hour_set[i]<18:
        time_slice[3] += 1
    elif hour_set[i]>=18 and hour_set[i]<22:
        time_slice[4] += 1
    else:
        time_slice[5] += 1
labels = ['凌晨2点至6点','6点至10点','10点至14点',
          '14点至18点','18点至22点','22点至次日凌晨2点']
time_distribution = {
        labels[0]: time_slice[0],
        labels[1]: time_slice[1],
        labels[2]: time_slice[2],
        labels[3]: time_slice[3],
        labels[4]: time_slice[4],
        labels[5]: time_slice[5]
        }
print(time_distribution)

''' 深夜聊天记录 '''
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('late')
for i in range(len(deep_night)):
    sheet.write(i,0,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(deep_night[i][0])))
    sheet.write(i,1,deep_night[i][1])
wbk.save('聊得很晚.xls')
print('\n.......................\n聊天时段统计结束\n.......................')

''' 字符统计 '''
print('\n..........\n开始字符统计\n............\n')
start = datetime.datetime.now()
pattern_love = '.*?(爱).*?'
pattern_morning= '.*?(早安).*?'
pattern_night = '.*?(晚安).*?'
pattern_miss = '.*?(想你).*?'
pattern_set = [pattern_love, pattern_morning, pattern_night, pattern_miss]
statistic = [0,0,0,0]
for i in range(len(chat_content)):
    for j in range(len(pattern_set)):
        length = len(re.findall(pattern_set[j], str(chat_content[i])))
        statistic[j] += length
result = {
        '爱': statistic[0],
        '早安': statistic[1],
        '晚安': statistic[2],
        '想你': statistic[3]
        }
print(result)
end = datetime.datetime.now()
print('\n..........\n字符统计结束,用时: {}\n............\n'.format(end-start))
