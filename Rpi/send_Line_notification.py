from os import path, remove

import requests
import shutil

from read_config import RC

def sendLineMessage(token,message = None,image = None):
    RC.initialize()

    url = "https://notify-api.line.me/api/notify"
    headers = { "Authorization": "Bearer " + token }

    filename = "tempfile.jpg"

    data = dict()
    if message :
        data['message'] = '\n' + message 

    files = {}
    if path.exists(image) :
        files['imageFile'] = open(image, 'rb')
    else:
        r = requests.get(image, stream = True)
        if r.status_code == 200 :
            r.raw.decode_content = True
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

            files['imageFile'] = open(filename,'rb')
            
    requests.post(
        url,
        headers = headers,
        data = data,
        files = files
    )

    files['imageFile'].close()
    remove('./' + filename)


if __name__ == "__main__":
    RC.initialize()
    sendLineMessage(RC.getLineKey(),"test","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRcxYjqWm-l89uuhZCDY4gFtNvaNe3vWxGcTQ&usqp=CAU")