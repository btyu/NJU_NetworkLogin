import requests
import config
import time
import sys


class TaoNJUNetworkLogin:
    login_url = 'http://219.219.114.172/portal_io/login'  # 登录url

    LOGIN_SUCCESS_CODE = 1
    LOGIN_ALREADY_CODE = 6

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_data = {
            'username': self.username,
            'password': self.password,
        }

    def __login(self):  # 登录
        try:
            r = requests.post(TaoNJUNetworkLogin.login_url, self.login_data)
        except Exception as e:
            return {
                'reply_code': -1,
                'exception': e,
            }
        else:
            return eval(r.text)

    def login(self):  # 登录（用户接口）
        print('----- 登录 -----')
        reply = self.__login()
        reply_code = reply['reply_code']
        if reply_code == TaoNJUNetworkLogin.LOGIN_SUCCESS_CODE:
            print('登录成功')
            login_success = True
        elif reply_code == TaoNJUNetworkLogin.LOGIN_ALREADY_CODE:
            print('已登录')
            login_success = True
        else:  # 登录失败
            t = 0
            login_success = False
            while t < config.login_retry_time:
                print('已尝试%d/%d次，登录失败，即将在%s秒后重试，.....' % (
                    t, config.login_retry_time,
                    str(config.login_retry_frequency),
                ))
                time.sleep(config.login_retry_frequency)
                reply = self.__login()
                reply_code = reply['reply_code']
                if reply_code in (TaoNJUNetworkLogin.LOGIN_SUCCESS_CODE, TaoNJUNetworkLogin.LOGIN_ALREADY_CODE):
                    print('在第%d尝试时登录成功' % t)
                    login_success = True
                    break
                t += 1

            if not login_success:
                print('已尝试%d/%d次，登录失败！' % (t, config.login_retry_time))
        print('-------------')
        return login_success

    def keep_login(self):
        print('===== 确保在线 =====')
        print('确保在线模式将每%s小时检查联网情况，若没在线则自动登录。如果尝试登录失败，将在失败后的%s小时后重试。' % (
            str(config.check_frequency),
            str(config.error_check_frequency),
        ))
        print('为确保功能正常，请不要退出这个程序')
        print('确实要退出，请按"Ctrl + C"结束程序')

        check_frequency_second = config.check_frequency * 60 * 60
        error_check_frequency_second = config.error_check_frequency * 60 * 60

        while True:
            success = self.login()
            if success:
                time.sleep(check_frequency_second)
            else:
                print('登录失败，将在%s小时后重试。' % str(config.error_check_frequency))
                time.sleep(error_check_frequency_second)


if __name__ == '__main__':
    args = sys.argv[1:]
    mode = None

    login = TaoNJUNetworkLogin(config.username, config.password)

    if len(args) != 0 and args[0] == 'login':
        mode = 1
    elif len(args) != 0 and args[0] == 'keep_login':
        mode = 2
    else:
        mode = input('请指定运行模式：登录一次(1) / 保持在线(2) / 取消(3)：')
        if mode.isdigit():
            mode = int(mode)

    if mode == 1:
        login.login()
    elif mode == 2:
        login.keep_login()
    else:
        print("已取消")
