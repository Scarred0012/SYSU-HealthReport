import requests

def get_img(driver, token):
    ''' 调用 http://fast.95man.com 在线识别验证码
    '''

    headers = {'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'}
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    res =  s.get(url)
    
    files = {'imgfile': ('captcha.jpg', res.content)}
    r = requests.post(f'http://api.95man.com:8888/api/Http/Recog?Taken={token}&imgtype=1&len=4', 
        files=files, headers=headers)
    arrstr = r.text.split('|')
    # 返回格式：识别ID|识别结果|用户余额
    if(int(arrstr[0]) > 0):
        print(f'验证码识别成功')
        capt = arrstr[1]
        return capt
    else:
        print(f'识别失败：{arrstr[0]}，重试')
        raise Exception('验证码识别失败')


def tgbot_send(token, chatid, message):
    data = {'chat_id': chatid, 'text': f'健康申报结果：{message}'}
    try:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')


def wx_send(wxsend_key, message):
    data = {
        "title": f'健康申报结果：{message}',
        "desp": "如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。"
    }
    try:
        r = requests.post(f'https://sctapi.ftqq.com/{wxsend_key}.send', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')
