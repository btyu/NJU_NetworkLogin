# ===== 必须设置 =====
username = 'username'  # 用户名
password = 'password'  # 密码

# ===== 保持登录设置 =====
check_frequency = 24  # 日常检查频率，可以为小数，单位：小时
error_check_frequency = 2  # 如果上次检查并尝试登录时出错了，再次重试的时间间隔，可以为小数，单位：小时

# ===== 可选设置 =====
login_retry_time = 5  # 如果登录失败，重新尝试次数
login_retry_frequency = 5  # 如果登录失败，重新尝试的时间间隔，可以为小数，单位：秒
logout_retry_time = 5  # 如果登出失败，重新尝试次数
logout_retry_frequency = 5  # 如果登出失败，重新尝试的时间间隔，可以为小数，单位：秒

