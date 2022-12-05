class State:
    atHome = True
    doorStates = []
    userAllStates = ["At Home", "Not At Home"]
    doorAllStates = ["door opening", "door closing", "door stopped"]
    
    @staticmethod
    def addDoorState(message):
        State.doorStates.append(message)
        return
        
    @staticmethod
    def getUserState():
        return State.userAllStates[0] if State.atHome else State.userAllStates[1]

    @staticmethod
    def changeUserState():
        State.atHome = not State.atHome

    @staticmethod
    def getDoorLastState():
        return State.doorStates[-1] if len(State.doorStates)>0 else None