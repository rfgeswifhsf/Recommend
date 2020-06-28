import pandas as pd
from sqlalchemy import create_engine
import logging
import configure
# 初始化数据库连接，使用pymysql模块

logging.basicConfig(level=logging.DEBUG)

'''tnt_prod 产品表'''
def tnt_prod():
    logging.info('tnt_prod数据库,连接中.......')
    logging.info('mysql+pymysql://{}:{}@{}/{}'.format(configure.TntUserName,configure.TntPassWord,configure.TntUrl,configure.TntDataBase))

    engine_tnt = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(configure.TntUserName,configure.TntPassWord,configure.TntUrl,configure.TntDataBase))

    sql_tnt_prod_weshop_user_prod = ''' select * from emc_weshop_user_prod t where t.category_id in( '1', '11', '15', '16', '17'); '''
    sql_tnt_prod_weshop_prod =  ''' select * from emc_weshop_prod t where t.category_id in( '1', '11', '15', '16', '17'  ); '''
    sql_tnt_prod_tnt_product =  ''' select * from tnt_product t ; '''


    df_tnt_prod_weshop_user_prod = pd.read_sql_query(sql_tnt_prod_weshop_user_prod, engine_tnt)
    df_tnt_prod_weshop_prod = pd.read_sql_query(sql_tnt_prod_weshop_prod, engine_tnt)
    df_tnt_prod_tnt_product = pd.read_sql_query(sql_tnt_prod_tnt_product, engine_tnt)
    logging.info('tnt_prod连接完成。')
    engine_tnt.dispose()
    return df_tnt_prod_weshop_user_prod,df_tnt_prod_weshop_prod,df_tnt_prod_tnt_product

def product_db():
    '''product_db产品表'''
    # logging.info('mysql+pymysql://{}:{}@{}/{}'.format(configure.ProdUserName,configure.ProdPassWord,configure.ProdUrl,configure.ProdDataBase))
    # engine_product_db = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(configure.ProdUserName,configure.ProdPassWord,configure.ProdUrl,configure.ProdDataBase))
    # sql_product_db_prod_product =  ''' select * from product t ; '''
    # df_product_db_product = pd.read_sql_query(sql_product_db_prod_product, engine_product_db)

def mind_order():
    '''订单表'''
    logging.info('mind_order数据库,连接中.......')
    logging.info('mysql+pymysql://{}:{}@{}/{}'.format(configure.MindUserName,configure.MindPassWord,configure.MindUrl,configure.MindDataBase))
    engine_order = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(configure.MindUserName,configure.MindPassWord,configure.MindUrl,configure.MindDataBase))

    sql_mind_order_main_order= ''' select * from main_order t ; '''
    sql_mind_order_sub_order= ''' select * from  sub_order t ; '''
    sql_mind_order_order_goods_detail = '''select * from order_goods_detail'''

    df_mind_order_main_order = pd.read_sql_query(sql_mind_order_main_order, engine_order)
    df_mind_order_sub_order = pd.read_sql_query(sql_mind_order_sub_order, engine_order)
    df_mind_prder_order_goods_detail = pd.read_sql_query(sql_mind_order_order_goods_detail, engine_order)


    merge_sub_order_id = pd.merge(df_mind_order_sub_order,df_mind_prder_order_goods_detail,on='sub_order_id')
    merge_order_id = pd.merge(merge_sub_order_id,df_mind_order_sub_order,on='order_id')

    'customer_id_x,order_id,goods_id,goods_num,refunded_num(已退数量)，payment_time_x'

    df_order_take_ = pd.DataFrame(merge_order_id,columns=['customer_id_x','order_id','goods_id','goods_num','refunded_num','payment_time_x'])
    df_order_take = df_order_take_.rename(columns={'customer_id_x':'user_id','order_id':'order_id','goods_id':'product_id','goods_num':'product_num','refunded_num':'refunded_num','payment_time_x':'payment_time'})


    '''
    评分规则 : 购买数量-退货量。当前时间-支付时间
    '''
    def grade(x):
        x['grade_num']=x['product_num']-x['refunded_num']
        x['grade_time']='尚无'

        return x

    new_order_df= df_order_take.groupby(['user_id','order_id','product_id']).apply(grade)

    new_order_df['user_id']=new_order_df['user_id'].map(lambda x:str(x)[:-2])
    new_order_df['order_id'] = new_order_df['order_id'].map(lambda x: str(x)[:-2])
    new_order_df['product_id'] = new_order_df['product_id'].map(lambda x: str(x)[:-2])

    # print(new_order_df)
    logging.info('mind_order数据库,连接完成')
    engine_order.dispose()
    return  new_order_df


'''希望能增加用户行为表'''

if __name__ == '__main__':
    mind_order()
