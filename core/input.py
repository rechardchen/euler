# import KEY_XXX them all
# TODO remove the ugly use
from glfw import *

class KeyEvent:
    def __init__(self,key,action,mode):
        self.key = key
        self.action = action
        self.mode = mode

class MouseEvent:
    def __init__(self,button,action,mode,pos):
        self.button = button
        self.action = action
        self.mode = mode
        self.pos = pos

class Input(object):
    def __init__(self, window) -> None:
        self.window = window

        # keyboard state
        self.keyDownList    = set()
        self.keyUpList      = set()
        self.keyPressedList = set()

        # mouse state
        self.mousePos = [0,0]

        # self.mouseButtons = [False]*3
        self.mouseEvtListeners = []

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

    def setMousePos(self, x,y):
        set_cursor_pos(self.window, x, y)
    
    def showCursor(self, show):
        set_input_mode(self.window, CURSOR, CURSOR_NORMAL if show else CURSOR_HIDDEN)

    def receiveKeyEvent(self, k,a,m):
        self.keyEvents.append(KeyEvent(k,a,m))
    
    def receiveCursorEvent(self, x, y):
        self.mousePos[0] = x
        self.mousePos[1] = y

    def receiveMouseButtonEvent(self,mouseEvt):
        for listener in self.mouseEvtListeners:
            listener.mouseEvent(mouseEvt, self)
    
    def regMouseEventListener(self, listener):
        self.mouseEvtListeners.append(listener)
    