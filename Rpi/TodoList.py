import json
import os

class TodoList:
    
    todoList = None

    @staticmethod
    def initialize(todoList_path = "./todoList.json"):
        TodoList.reRead(todoList_path)

    @staticmethod
    def reRead(todoList_path = "./todoList.json"):
        with open(todoList_path,"rb") as f:
            TodoList.todoList = json.load(f)

    @staticmethod
    def addTodo(task):
        TodoList.reRead()
        usedID = []
        for tl in TodoList.todoList:
            usedID.append(int(tl['id']))
        usedID = sorted(usedID)
        newID = -1
        for i in range(len(usedID)):
            if usedID[i] != i:
                newID = i
                break
        if usedID == []:
            newID = 0
        elif newID == -1:
            newID = usedID[-1]+1
        TodoList.todoList.append({"id":str(newID),"status":"0","task":task})
        with open("./todoList.json",'w') as f:
            json.dump(TodoList.todoList,f)
        return

    @staticmethod
    def deleteTodo(index):
        TodoList.reRead()
        TodoList.todoList.pop(index)
        with open("./todoList.json",'w') as f:
            json.dump(TodoList.todoList,f)
        return

    def editTodo(id, task):
        TodoList.reRead()
        for todo in TodoList.todoList:
            if todo['id'] == id:
                todo['task'] = task
                break
        with open("./todoList.json",'w') as f:
            json.dump(TodoList.todoList,f)
        return
    
    def changeStatus(id):
        TodoList.reRead()
        for todo in TodoList.todoList:
            if todo["id"] == id:
                if todo["status"] == "0":
                    todo["status"] = "1"
                elif todo["status"] == "1":
                    todo["status"] = "0"
                break
        with open("./todoList.json",'w') as f:
            json.dump(TodoList.todoList,f)
        return


if __name__ == '__main__':
    os.system("jq . ./todoList.json")
    # TodoList.reRead()
    # TodoList.addTodo("addTodoTesting")