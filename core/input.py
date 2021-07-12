# import KEY_XXX them all
# TODO remove the ugly use
from glfw import *

class KeyEvent:
    def __init__(self,key,action,mode):
        self.key = key
        self.action = action
        self.mode = mode

class Input(object):
    def __init__(self) -> None:
        self.keyDownList    = set()
        self.keyUpList      = set()
        self.keyPressedList = set()

        self.keyEvents      = []

    def update(self):
        self.keyDownList.clear()
        self.keyUpList.clear()

        for evt in self.keyEvents:
            if evt.action == PRESS:
                self.keyDownList.add(evt.key)
                self.keyPressedList.add(evt.key)
            elif evt.action == RELEASE:
                self.keyUpList.add(evt.key)
                self.keyPressedList.remove(evt.key)
        self.keyEvents.clear()

    def isKeyDown(self,key):
        return key in self.keyDownList
    
    def isKeyUp(self, key):
        return key in self.keyUpList
    
    def isKeyPressed(self, key):
        return key in self.keyPressedList

    def receiveKeyEvent(self, k,a,m):
        self.keyEvents.append(KeyEvent(k,a,m))
    