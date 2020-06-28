#-*- coding: utf-8 -*-
import sys
import random
import math
import os
from operator import itemgetter
from collections import defaultdict
import  numpy as np
random.seed(0)

'''有新物品加入时，调用该算法'''
class UserBasedCF(object):
    '''
    群体/个体：更依赖于当前用户相近的用户群体的社会化行为
    计算代价：适用于用户数较少的场合
    适用场景：时效性强，用户个性化兴趣不太显著的场合
    冷启动：新加入的物品能很快进入推荐列表
    实时性：用户新的行为不一定导致推荐结果的变化


    '''
    def __init__(self):
        self.trainset = {}

        self.user_sim_mat = {}
        self.product_popular = {}
        self.product_count = 0
        self.max_point = 0.0
        self.min_point = 10.0

    def generate_dataset(self, dataframe):
        max_score = max(dataframe['score'])
        min_score = min(dataframe['score'])

        for index,row in dataframe.iterrows():
            user, product, rating = str(int(row['user_id'])),str(int(row['proid'])),row['score']
            self.trainset.setdefault(user, {})
            self.trainset[user][product] = (float(rating)-min_score)/(max_score-min_score)

    def calc_user_sim(self):
        '''计算相似用户'''
        '''定义一个倒排字典 p-u'''
        product2users = dict()
        for user, products in self.trainset.items():
            for product in products:
                '''以产品为key,用户为value，其结构为{key:[value1,value2,value3...]}'''
                if product not in product2users:
                    product2users[product] = set()
                product2users[product].add(user)


        '''产品数量'''
        self.product_count = len(product2users)
        print ('total product number = %d' % self.product_count, file=sys.stderr)

        '''用户倒排矩阵'''
        usersim_mat = self.user_sim_mat
        for product, users in product2users.items():
            for u in users:
                usersim_mat.setdefault(u, defaultdict(int))
                for v in users:
                    if u == v:
                        continue
                    usersim_mat[u][v] += self.trainset[u][product]
                    usersim_mat[u][v] += self.trainset[v][product]

        for u, related_users in usersim_mat.items():
            for v, count in related_users.items():
                usersim_mat[u][v] = count / np.linalg.norm(np.array(list(self.trainset[u].values()))) * np.linalg.norm(np.array(list(self.trainset[v].values())))


        #     相识度矩阵做归一化
        normallist = [list(i.values()) for i in usersim_mat.values()]  # [[],[],[]]
        normallist = sum(normallist, [])  # []
        max_values = max(normallist)
        min_values = min(normallist)
        reg = max_values - min_values + 0.000000001  # 防止reg为0

        for u, related_products in usersim_mat.items():
            for v, count in related_products.items():
                self.user_sim_mat[u][v] = (count - min_values) / reg


    def recommend(self, user,trainset,user_sim_mat,K,N):
        ''' 寻找k个相似用户，推荐n个产品 '''
        rank = dict()

        watched_products = trainset[user]
        for similar_user, similarity_factor in sorted(user_sim_mat[user].items(), key=itemgetter(1),
                                                      reverse=True)[0:K]:

            for product in trainset[similar_user]:

                '''如果产品已被用户购买过，则不参加推荐，得分为0'''
                if product in watched_products:
                    continue
                '''否则计算相似用户中，该产品的累积得分，相似用户中大多购买过该产品，则有理由相信当前用户对该物品兴趣大'''
                rank.setdefault(product, 0)
                rank[product] += similarity_factor * trainset[similar_user][product]
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]




# if __name__ == '__main__':
#     ratingfile = os.path.join('ml-1m', 'ratings.dat')
#     usercf = UserBasedCF()
#     usercf.generate_dataset(ratingfile)
#     usercf.calc_user_sim()
#
#     '''预测或推荐'''
#
#     for i, user in enumerate(usercf.trainset):
#         if i% 1000==0:
#             rec = usercf.recommend(user)
#             print(user,'--> ',rec)

