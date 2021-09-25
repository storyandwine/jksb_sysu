import requests

def get_img(driver, rec_url):
    ''' 调用某位不知名好心人的在线识别验证码后端
    '''
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    res =  s.get(url)
    files = {'img': ('captcha.jpg', res.content, 'image/jpeg')}
    r =  requests.post(rec_url, files = files)
    if r.text.split('|')[0] is not '-1':
        capt = r.text.split('|')[1]
        print(f'验证码识别成功：{capt}')
        return capt
    else:
        print(f'识别失败：{r.text}，重试')
        return False


def wx_send(wxsend_key, message):
    data = {
        "text": "健康申报结果"+message,
        "desp": "如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。"
    }
    try:
        r = requests.post(f'https://sc.ftqq.com/{wxsend_key}.send', data = data)
        if r.status_code == 200:
            print('发送通知成功')
        else:
            print('发送通知失败')
    except:
        print('发送通知失败')
