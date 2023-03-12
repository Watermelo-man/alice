class Meeting():
    text = 'Привет! Это навык для игры "Миры Ктулху!"'
    idOutput = 1
    def __init__(self) -> None:
        pass
    def responseToMeetState(self,state:bool):
        if state == True:
            return [self.text,'false']
        else:
            return None