import json
import pickle

from kafka import KafkaConsumer
from modelpakage import usercf,itemcf,item2vec
import logging

from gensim.models import Word2Vec,Doc2Vec

logging.DEBUG

# group_id,是为了不影响其他应用对同一kafka topic的消费，自己随便取名字，但是不能重名
# auto_offset_reset='latest' 表示从最新位置开始消费，earliest表示最早位置
if __name__ == '__main__':

    consumer = KafkaConsumer("zhangwei1", bootstrap_servers=["10.200.5.117:9092"],group_id='rec3',auto_offset_reset='earliest')

    model_usercf = usercf.UserBasedCF()
    model_itemcf = itemcf.ItemBasedCF()

    # 加载 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset.file", "rb") as f:
        trainset = pickle.load(f)
        f.close()

    # 加载
    with open("../modelRelation/user_sim_mat.file", "rb") as f:
        user_sim_mat = pickle.load(f)
        f.close()

    # 加载 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset_item.file", "rb") as f:
        trainset_item = pickle.load(f)
        f.close()
    # 加载
    with open("../modelRelation/product_sim_mat.file", "rb") as f:
        product_sim_mat = pickle.load(f)
        f.close()


    model_item2vec = item2vec.CBOW()
    model_item2vec_ = Word2Vec.load('../modelRelation/item2vec')




    print('begin,consumer....')

    for msg in consumer:
        user_action=json.loads(s=msg.value) #dict()
        # {'db': 'afanti', 'table': 'rec_useraction', 'event_type': 1, 'data': {'user_id': '1448', 'user_action': 'purchase', 'proid': '25782', 'click_time': '2020-05-12 21:05:15'}}

#         首先判断，数据的  【 增1 删3 改2 】 类型
        '''
            1.监听--产品表，如果有新产品上架，或者有产品下架，重新训练模型，重新加载数据，usercf,item2vec
            2.监听--用户表，如果有新用户加入，重新训练 itemcf 
        '''
#         删除逻辑（没有逻辑，因为，用户行为不涉及删除）


#         更新逻辑（没有逻辑，同上）

#         插入逻辑（主要部分）
        if user_action['db']=='afanti' and user_action['table']=='rec_useraction' and user_action['event_type']==1:
           data =user_action['data']
           user_id = data['user_id']
           proid = data['proid']

           # usercf 推荐的10个可能感兴趣产品
           reclist_ucf = model_usercf.recommend(user_id,trainset,user_sim_mat,K=20,N=10)
           # print('********'*3,'usercf推荐的10个产品','**********'*3)
           # print(reclist_ucf)


           #itemcf 推荐的10个可能感兴趣的产品
           reclist_icf = model_itemcf.recommend(user_id,trainset_item,product_sim_mat,20,10)
           # print('********' * 3, 'itemcf推荐的10个产品', '**********' * 3)
           # print(reclist_icf)

           #item2vec  推荐的10个可能感兴趣的产品

           reclist_i2v = model_item2vec.recommend(model_item2vec_,proid,K=10)
           # print('********' * 3, 'item2vec推荐的10个产品', '**********' * 3)
           # print(reclist_i2v)

           # 过滤去重
           reclist=[]
           reclist_ucf_list = [ i[0] for i in reclist_ucf]
           reclist_icf_list = [ i[0] for i in reclist_icf]
           reclist_i2v_list = [i[0] for i in reclist_i2v]
           reclist.extend(reclist_ucf_list)
           reclist.extend(reclist_icf_list)
           reclist.extend(reclist_i2v_list)
           print(set(reclist))
           print(len(set(reclist)))

           # 把高曝光低点击的产品往后移 exposure （需要去数据库查表计算，为了节约时间，建议离线计算，保存结果，这里直接取结果）
           '''等埋点'''

           # 混入少量低曝光的产品，用来挖掘长尾分布 （同上）
           '''等卖点'''
