import requests

def send_ifttt(key, event, *v1):
    url = ('https://maker.ifttt.com/trigger/' + event + '/with/' + 'key/' + key + '?value1='+str(v1[0])+'&value2='+str(v1[1])+'&value3='+str(v1[2]))
    r = requests.get(url)
    return r.text

def send_ifttt(*v1):
    from main import rc
    url = ('https://maker.ifttt.com/trigger/' + rc.getIftttEvent() + '/with/' + 'key/' + rc.getIftttKey() + '?value1='+str(v1[0])+'&value2='+str(v1[1])+'&value3='+str(v1[2]))
    r = requests.get(url)
    return r.text

#傳送 HTTP 請求到 IFTTT
# ret = send_ifttt1( '0','1','2') 
# print('IFTTT 的回應訊息：',ret) # 輸出 IFTTT 回應的文字