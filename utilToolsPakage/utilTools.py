import math
import time, datetime
import pandas as pd
from sqlalchemy import create_engine
import configure

def time2time(action_time):
    '''
    将字符串转换成时间，并计算用户行为时间与参照时间之间的距离
    :param pivote_time:  参照时间
    :param action_time:  用户发生行为的时间
    :return: (action_time-pivote_time).days
    '''

    # 字符串转时间
    action_time = time.strptime(action_time, "%Y-%m-%d %H:%M:%S")
    a_y, a_m, a_d, a_h, a_min, a_s = action_time[0:6]

    pivote_time = datetime.datetime.now()
    action_time = datetime.datetime( a_y, a_m, a_d, a_h, a_min, a_s)

    return  abs((action_time-pivote_time).days)

def getData():
    '''
    获取用户行为数据库连接
    :return:
    '''
    engine = create_engine('mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(configure.uacName
                                                                              ,configure.uacPassWord
                                                                              ,configure.uacUrl
                                                                              ,configure.uacDataBase
                                                                              )
                                                                              ,encoding='utf-8')
    sql_action = '''select * from {}'''.format(configure.uactable)

    df_action = pd.read_sql_query(sql_action, engine)
    return df_action

def score(uaf):

    action = uaf['user_action']
    offset = uaf['getScoreoffset']
    score_  = configure.action_score[action]['score'] * offset
    return score_

def timeOffset(uaf):
    # print(uaf)
    '''
    计算时间距离
    :param uaf: str  eg --- 2020-05-27 11:55:19
    :return: day int
    # '''
    action = uaf['user_action']

    action_time = str(uaf['click_time'])
    if  configure.action_score[action]['decay']==0:
        substract = time2time(action_time)
        substract=1/(math.log(substract+1)+1)
    else:
        substract=1

    return substract
