# 输入路径
USER_PROFILE_TRAIN='./data/train/userProfile_all.csv'
ORDER_HISTORY_TRAIN='./data/train/orderHistory_all.csv'
USER_COMMENT_TRAIN='./data/train/userComment_all.csv'
ACTION_TRAIN='./data/train/action_all.csv'
LABEL_TRAIN='./data/train/orderFuture_all.csv'

# 输出路径
OUT_ACTION_WITH_HISTORY='./data/train_use/action_train_with_history.csv'
OUT_USER_PROFILE_TRAIN='./data/train_use/userProfile_train.csv'
OUT_ORDER_HISTORY_TRAIN='./data/train_use/orderHistory_train.csv'
OUT_USER_COMMENT_TRAIN='./data/train_use/userComment_train.csv'
OUT_ACTION='./data/train_use/action_train.csv'
OUT_ACTION_1='./data/train_use/action_train_1.csv'
OUT_ACTION_2='./data/train_use/action_train_2.csv'
OUT_LABEL_TRAIN='./data/train_use/label_train.csv'

# # 处理用户个人信息
# python3 process_userProfile.py $USER_PROFILE_TRAIN $OUT_USER_PROFILE_TRAIN || exit 1
# 处理用户历史订单数据
# python3 process_orderHistory.py $ORDER_HISTORY_TRAIN $OUT_ORDER_HISTORY_TRAIN || exit 1
# # 处理评论信息
# python3 process_userComment.py $USER_COMMENT_TRAIN $OUT_USER_COMMENT_TRAIN || exit 1
# # 将历史订单信息里面的成单，加到action里面去
# python3 process_combine_his_action.py $ACTION_TRAIN $ORDER_HISTORY_TRAIN $OUT_ACTION_WITH_HISTORY || exit 1
# # 处理浏览信息
# python3 process_action.py $ACTION_TRAIN $OUT_ACTION || exit 1
# # 处理浏览信息增加
# python3 process_action_1.py $OUT_ACTION_WITH_HISTORY $OUT_ACTION_1 || exit 1
# # 增加新的action特征
# python3 process_action_3.py $OUT_ACTION_WITH_HISTORY $OUT_ACTION_2 || exit 1
# # 进行训练集维度的合并
# python3 process_combine.py $OUT_USER_PROFILE_TRAIN $OUT_ORDER_HISTORY_TRAIN $OUT_USER_COMMENT_TRAIN $LABEL_TRAIN $OUT_ACTION $OUT_ACTION_1 $OUT_ACTION_2 $OUT_LABEL_TRAIN || exit 1

# 输入路径
USER_PROFILE_TRAIN='./data/test/userProfile_test.csv'
ORDER_HISTORY_TRAIN='./data/test/orderHistory_test.csv'
USER_COMMENT_TRAIN='./data/test/userComment_test.csv'
ACTION_TRAIN='./data/test/action_test.csv'

# 输出路径
OUT_ACTION_WITH_HISTORY='./data/test_use/action_train_with_history.csv'
OUT_USER_PROFILE_TRAIN='./data/test_use/userProfile_test.csv'
OUT_ORDER_HISTORY_TRAIN='./data/test_use/orderHistory_test.csv'
OUT_USER_COMMENT_TRAIN='./data/test_use/userComment_test.csv'
OUT_ACTION='./data/test_use/action_test.csv'
OUT_ACTION_1='./data/test_use/action_test_1.csv'
OUT_ACTION_2='./data/test_use/action_test_2.csv'
OUT_LABEL_TRAIN='./data/test_use/label_test.csv'

# # 处理用户个人信息
# python3 process_userProfile.py $USER_PROFILE_TRAIN $OUT_USER_PROFILE_TRAIN || exit 1
# # 处理用户历史订单数据
# python3 process_orderHistory.py $ORDER_HISTORY_TRAIN $OUT_ORDER_HISTORY_TRAIN || exit 1
# # 处理评论信息
# python3 process_userComment.py $USER_COMMENT_TRAIN $OUT_USER_COMMENT_TRAIN || exit 1
# # 将历史订单信息里面的成单，加到action里面去
# python3 process_combine_his_action.py $ACTION_TRAIN $ORDER_HISTORY_TRAIN $OUT_ACTION_WITH_HISTORY || exit 1
# # 处理浏览信息
# python3 process_action.py $ACTION_TRAIN $OUT_ACTION || exit 1
# # 处理浏览信息增加
# python3 process_action_1.py $OUT_ACTION_WITH_HISTORY $OUT_ACTION_1 || exit 1
# # 增加新的action特征
# python3 process_action_3.py $OUT_ACTION_WITH_HISTORY $OUT_ACTION_2 || exit 1
# # 进行训练集维度的合并
# python3 process_combine.py $OUT_USER_PROFILE_TRAIN $OUT_ORDER_HISTORY_TRAIN $OUT_USER_COMMENT_TRAIN $OUT_ACTION $OUT_ACTION_1 $OUT_ACTION_2 $OUT_LABEL_TRAIN || exit 1
