#-*- coding: utf-8 -*-
import sys
import random
import math
import os
from operator import itemgetter
from collections import defaultdict


random.seed(0)
import time
begin =time.time()
'''新用户&时效性优与usercf'''
class ItemBasedCF(object):
    '''

    群体/个体：更侧重用户自身的个体行为
    计算代价：适用于物品数较少的场合
    适用场景：长尾物品丰富，用户个性化需求强烈的场合
    冷启动：新加入的用户能很快得到推荐
    可解释性：强
    实时性：用户新的行为一定导致推荐结果的变化


    '''

    def __init__(self):
        self.trainset = {}
        self.product_sim_mat = {}
        self.product_popular = {}
        self.product_count = 0

    def generate_dataset(self, dataframe):
        max_score = max(dataframe['score'])
        min_score = min(dataframe['score'])

        for index,row in dataframe.iterrows():
            user, product, rating = str(int(row['user_id'])),str(int(row['proid'])),row['score']
            self.trainset.setdefault(user, {})
            self.trainset[user][product] = (float(rating)-min_score)/(max_score-min_score)

    def calc_product_sim(self):
        ''' 计算产品相似矩阵 '''
        for user, products in self.trainset.items():
            for product in products:
                if product not in self.product_popular:
                    self.product_popular[product] = 0
                '''得分'''
                self.product_popular[product]+=products[product]

        # 得分为0，说明没有用户对该产品产生过行为，即无法和其他产品计算相似度，应该给予过滤



        '''产品总数'''
        self.product_count = len(self.product_popular)
        print('total product number = %d' % self.product_count, file=sys.stderr)
        '''计算产品相似度,产品倒排矩阵,产品prod1,产品prod1 在一个以上用户那里有过行为开始计数'''
        itemsim_mat = self.product_sim_mat


        for user, products in self.trainset.items():
            for prod1 in products:
                itemsim_mat.setdefault(prod1, defaultdict(int))
                for prod2 in products:
                    if prod1 == prod2:
                        continue
                    itemsim_mat[prod1][prod2]+=products[prod1]
                    itemsim_mat[prod1][prod2]+=products[prod2]
        '''计算两个产品的相识度'''
        for prod1, related_products in itemsim_mat.items():
            for prod2, count in related_products.items():
               if self.product_popular[prod1] * self.product_popular[prod2]==0:
                    continue
               else:
                itemsim_mat[prod1][prod2] =count/math.sqrt(self.product_popular[prod1] * self.product_popular[prod2])

        #     相识度矩阵做归一化
        normallist = [list(i.values()) for i in itemsim_mat.values()] #[[],[],[]]
        normallist = sum(normallist, []) #[]
        max_values = max(normallist)
        min_values = min(normallist)

        reg =max_values-min_values+0.000000001 #防止reg为0

        for prod1 ,related_products in itemsim_mat.items():
            for prod2,count in related_products.items():
                itemsim_mat[prod1][prod2]=(count-min_values)/reg



    def recommend(self, user,trainset,product_sim_mat,K,N):
        ''' 计算用户u对产品的兴趣程度。在k个相似产品中推荐N个 '''

        rank = {}
        watched_products = trainset[user]
        for product, rating in watched_products.items():
            for related_product, similarity_factor in sorted(product_sim_mat[product].items(),
                                                           key=itemgetter(1), reverse=True)[:K]:

                if related_product not in watched_products:
                    rank.setdefault(related_product, 0)
                    '''
                    p(u,i)=∑w(i,j)*r(u,j)
                    为用户U对未接触过的产品i的感兴趣程度，w(i,j)为产品相识度。r(u,j)表示用户对产品j的行为得分。
                    求和的基数是 S(i,k)与N(u)的交集，S(i,k)表示和物品i最相似的k个物品，N(u)表示用户u产生过行为的物品集合
                    '''
                    # rank[related_product] += ((similarity_factor-self.min_point)/(self.max_point-self.min_point))* rating
                    rank[related_product] += similarity_factor*rating


        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]




