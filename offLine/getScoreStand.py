'''
读取截至前一天的所有用户行为信息，对用户历史行为打分
'''

import pickle
from modelpakage import item2vec,usercf,itemcf
from utilToolsPakage import utilTools

if __name__ == '__main__':
    # 加载用户历史行为数据库数据
    df_action = utilTools.getData()

    # 时间权重
    df_action['getScoreoffset'] = df_action[['user_action','click_time']].apply(utilTools.timeOffset, axis=1)
    df_action['score'] = df_action[['user_action','getScoreoffset']].apply(utilTools.score, axis=1)
    del df_action['user_action']
    del df_action['getScoreoffset']
    del df_action['click_time']


    # usercf
    model_usercf = usercf.UserBasedCF()  # 创建模型实例

    model_usercf.generate_dataset(df_action) # 加载模型数据
    model_usercf.calc_user_sim() #相识度计算
    # 保存 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset_ucf.file", "wb") as f:
        pickle.dump(model_usercf.trainset, f)
        f.close()
    # 保存user_sim_mat[u][V]=sim,  字典结构，用户：{相似用户：相似度}
    with open("../modelRelation/user_sim_mat_ucf.file", "wb") as f:
        pickle.dump(model_usercf.user_sim_mat, f)
        f.close()
    # 加载 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset_ucf.file", "rb") as f:
        trainset = pickle.load(f)
        f.close()
    # 加载
    with open("../modelRelation/user_sim_mat_ucf.file", "rb") as f:
        user_sim_mat = pickle.load(f)
        f.close()



    # itemcf
    model_itemcf = itemcf.ItemBasedCF()
    model_itemcf.generate_dataset(df_action)
    model_itemcf.calc_product_sim()

    # 保存 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset_item.file", "wb") as f:
        pickle.dump(model_itemcf.trainset, f)
        f.close()
    # product_sim_mat[u][V]=sim,  字典结构，产品：{相似产品：相似度}
    with open("../modelRelation/product_sim_mat.file", "wb") as f:
        pickle.dump(model_itemcf.product_sim_mat, f)
        f.close()

    # 加载 trainset[user][product] = float(rating)
    with open("../modelRelation/trainset_item.file", "rb") as f:
        trainset_item = pickle.load(f)
        f.close()
    # 加载
    with open("../modelRelation/product_sim_mat.file", "rb") as f:
        product_sim_mat = pickle.load(f)
        f.close()



    # item2vec
    model_item2vec = item2vec.CBOW()
    model = model_item2vec.get_train_data(df_action) # 方法已经写了模型保存






    #
    l=model_usercf.recommend('1680',trainset,user_sim_mat,K=20,N=10)   #K个用户，前N个感兴趣产品
    print(l)

    #
    ll = model_itemcf.recommend('1680',trainset_item,product_sim_mat,K=20,N=10)
    print(ll)

    #
    lll = model_item2vec.recommend(model,'28482',K=10)
    print(lll)
