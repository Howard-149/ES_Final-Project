from os import path, remove

import requests
import shutil

from read_config import RC
from TodoList import TodoList

def sendLineMessage(token,message = None,image = None):
    RC.initialize()

    url = "https://notify-api.line.me/api/notify"
    headers = { "Authorization": "Bearer " + token }

    filename = "tempfile.jpg"

    data = dict()
    if message :
        data['message'] = '\n' + message 

    files = {}
    if image != None:
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

    if image != None:
        files['imageFile'].close()
        remove('./' + filename)


if __name__ == "__main__":
    RC.initialize()
    TodoList.reRead()
                    
    line_message="Todo-List : \n"
    for todo in TodoList.todoList:
        if todo["status"] == "0":
            line_message += "    ☐  "
        elif todo["status"] == "1":
            line_message += "    ☑  "
        
        line_message += todo["task"]
        line_message += "\n"
    
        
    sendLineMessage("dOkC46UJeLY1PC3OlFCIFxRh5Y997BNXe3JA2ydHLxU",line_message)
    # sendLineMessage(RC.getLineKey(),line_message)