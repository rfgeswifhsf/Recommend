'''tnt_prod 产品库'''
TntUserName = 'root'
TntPassWord = '123456'
TntUrl = '10.200.3.180:3306'
TntDataBase = 'tnt_prod'

'''product_db 产品表'''
ProdUserName = 'vacations_lvmama'
ProdPassWord = 'HMou+H4yuHO38PcG6+0mP47+MWq0po6fCr7v4DNQf8clW32HCXXgbBoyUN+9d/lJ1eB7vN8VE7w6C0wnqAEeUA=='
ProdUrl = '10.201.2.14:3306'
ProdDataBase = 'product_db'

'''mind_order 订单库'''
MindUserName = 'root'
MindPassWord = '111111'
MindUrl= '192.168.0.64:3306'
MindDataBase= 'mind_order'



'''历史行为库'''
uacName = 'root'
uacPassWord = '111111'
uacUrl = '192.168.0.63:3306'
uacDataBase = 'afanti'
uactable='rec_useraction'





action_score={
'purchase' : {'score':1.5,'decay':0}        #购买得分1.5，0表示得分随时间衰减
,'click' : {'score':0.3,'decay':1}          #点击得分0.3,1表示得分不随时间衰减
,'reserve' : {'score':0.5,'decay':0}        #预定
,'follow' : {'score':0.5,'decay':1}         #收藏
,'unfollow' : {'score':-0.5,'decay':0}      #取消收藏
,'comment' : {'score':0.5,'decay':0}        #评论
,'share' : {'score':0.5,'decay':1}          #分享
,'paied' : {'score':1.5,'decay':0}          #已支付
,'chargeBack' : {'score':-1.5,'decay':1}    #退单
# 搜索另算吧 ,按名称相似度算吧。
,'reschedule' : {'score':2,'decay':0}      #再次预定
}
