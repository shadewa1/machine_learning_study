#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   HBOS异常点检测.py    
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2022/4/12 10:10   SeafyLiang   1.0        HBOS异常点检测
"""
'''
HBOS全名为：Histogram-based Outlier Score。它是一种单变量方法的组合，不能对特征之间的依赖关系进行建模，但是计算速度较快，对大数据集友好，
其基本假设是数据集的每个维度相互独立，然后对每个维度进行区间(bin)划分，区间的密度越高，异常评分越低。理解了这句话，基本就理解了这个算法。
模型参数：
n_bins：分箱的数量
alpha：用于防止边缘溢出的正则项
tol：用于设置当数据点落在箱子外时的宽容度
contamination：用于设置异常点的比例
'''
# 导入包
from pyod.utils.data import generate_data, evaluate_print

# 样本的生成
X_train, y_train, X_test, y_test = generate_data(n_train=200, n_test=100, contamination=0.1)

print(X_train.shape)
# (200, 2)

print(X_test.shape)
# (100, 2)

from pyod.models import hbos
from pyod.utils.example import visualize

# 模型训练
clf = hbos.HBOS()
clf.fit(X_train)
y_train_pred = clf.labels_
y_train_socres = clf.decision_scores_

# 返回未知数据上的分类标签 (0: 正常值, 1: 异常值)
y_test_pred = clf.predict(X_test)
# 返回未知数据上的异常值 (分值越大越异常)
y_test_scores = clf.decision_function(X_test)

print(y_test_pred)
# [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1]


print(y_test_scores)
# [-0.90209111 -0.90209111 -0.09322378 -0.44865128 -0.09322378 -0.44865128
#  -0.90209111 -0.09322378  0.36021604 -0.44865128 -0.90209111 -0.09322378
#  -0.90209111  2.00232582 -0.44865128 -0.09322378 -0.44865128 -0.90209111
#  -0.90209111 -0.90209111 -0.90209111 -0.90209111 -0.09322378 -0.09322378
#  -0.09322378 -0.90209111 -0.90209111 -0.09322378 -0.90209111 -0.90209111
#  -0.09322378 -0.90209111 -0.09322378 -0.90209111 -0.44865128 -0.09322378
#  -0.44865128 -0.90209111 -0.90209111 -0.90209111 -0.44865128 -0.09322378
#   0.36021604 -0.09322378 -0.90209111 -0.90209111 -0.44865128 -0.90209111
#  -0.90209111 -0.09322378  2.00232582 -0.09322378 -0.44865128  0.36021604
#  -0.44865128 -0.44865128 -0.90209111 -0.44865128 -0.90209111 -0.90209111
#  -0.44865128 -0.44865128 -0.90209111 -0.90209111  0.36021604 -0.44865128
#  -0.09322378 -0.44865128 -0.90209111 -0.44865128 -0.90209111 -0.09322378
#   0.36021604 -0.90209111  0.36021604 -0.44865128 -0.90209111 -0.90209111
#  -0.44865128 -0.09322378 -0.90209111  0.36021604 -0.90209111 -0.09322378
#   0.36021604 -0.44865128 -0.90209111 -0.90209111 -0.09322378 -0.44865128
#   5.5335093   5.94991172  6.33881212  2.79916998  6.33881212  6.18587879
#   5.94991172  6.33035346  5.69806266  6.18587879]

# 模型评估
clf_name = 'HBOS'
evaluate_print(clf_name, y_test, y_test_scores)
# HBOS ROC:1.0, precision @ rank n:1.0

# 模型可视化
visualize(clf_name,
          X_train, y_train,
          X_test, y_test,
          y_train_pred, y_test_pred,
          show_figure=True,
          save_figure=False
          )
