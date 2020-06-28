#-*-coding:utf-8-*-
import pandas as pd
from gensim.models import Word2Vec,Doc2Vec
import multiprocessing
import os


class CBOW:
    def __init__(self):
       pass

    def get_train_data(self,dataframe,L=10):
        dataframe['proid'] = dataframe['proid'].apply(str)
        pro_list = dataframe.groupby('user_id')['proid'].apply(list).values
        model = Word2Vec(pro_list, size=L, window=5, sg=0, hs=0, min_count=1, workers=multiprocessing.cpu_count(),iter=10)
        model.save('../modelRelation/item2vec')
        return model

    def recommend(self,model,proID,K):
        proID = str(proID)
        rank = model.most_similar(proID,topn=K)
        return rank
