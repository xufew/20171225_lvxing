# =======================
# -*- coding: utf-8 -*-
# author: LONGFEI XU
# Try your best
# ============


# #############################
# 提取样本
# #############################
USER_PROFILE_TRAIN = './data/train/userProfile_train.csv'
ORDER_HISTORY_TRAIN = './data/train/orderHistory_train.csv'
USER_COMMENT_TRAIN = './data/train/userComment_train.csv'
ACTION_TRAIN = './data/train/action_train.csv'
LABEL_TRAIN = './data/train/orderFuture_train.csv'
USER_PROFILE_TEST = './data/test/userProfile_test.csv'
ORDER_HISTORY_TEST = './data/test/orderHistory_test.csv'
USER_COMMENT_TEST = './data/test/userComment_test.csv'
ACTION_TEST = './data/test/action_test.csv'

SAMPLE_USER_PROFILE = './data/train/userProfile_add.csv'
SAMPLE_ORDER_HISTORY = './data/train/orderHistory_add.csv'
SAMPLE_USER_COMMENT = './data/train/userComment_add.csv'
SAMPLE_ACTION = './data/train/action_add.csv'
SAMPLE_LABEL = './data/train/orderFuture_add.csv'

ALL_USER_PROFILE = './data/train/userProfile_all.csv'
ALL_ORDER_HISTORY = './data/train/orderHistory_all.csv'
ALL_USER_COMMENT = './data/train/userComment_all.csv'
ALL_ACTION = './data/train/action_all.csv'
ALL_LABEL = './data/train/orderFuture_all.csv'

# #############################
# 训练相关
# #############################
TRAIN_DATA_PATH = './data/train_use/label_train_drop.csv'
# TRAIN_DATA_PATH = './tmp/tmp_5/tmp_train_his'
TEST_DATA_PATH = './data/test_use/label_test_drop.csv'
# TEST_DATA_PATH = './tmp/tmp_4/tmp_test'

MODEL_LIGHTGBM_CL = './model/lightgbm_cl.pkl'
MODEL_LIGHTGBM_R = './model/lightgbm_r.pkl'
MODEL_XGBOOST_C = './model/gbdt_c.pkl'
MODEL_XGBOOST_R = './model/gbdt_r.pkl'
MODEL_RF = './model/rf.pkl'
MODEL_EXTRATREE = './model/extratree.pkl'
MODEL_ADABOOST = './model/adaboost.pkl'
MODEL_GBDT = './model/gbdt.pkl'
MODEL_LR = './model/lr.pkl'
MODEL_COMBINE = './model/combine.pkl'

RESULT_FINAL_TRANS = './data/result_compare.csv'
RESULT_LIGHTGBM_CL = './data/result_lightgbm_cl.csv'
RESULT_LIGHTGBM_R = './data/result_lightgbm_r.csv'
RESULT_XGBOOST_C = './data/result_xgboost_c.csv'
RESULT_XGBOOST_R = './data/result_xgboost_r.csv'
RESULT_EXTRATREE = './data/result_extratree.csv'
RESULT_ADABOOST = './data/result_adaboost.csv'
RESULT_GBDT = './data/result_gbdt.csv'
RESULT_RF = './data/result_rf.csv'
RESULT_COMBINE = './data/result_combine.csv'
