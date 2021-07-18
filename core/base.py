import glfw
from .input import Input,MouseEvent
from .openGLUtils import GL_MAJOR_VERSION, GL_MINOR_VERSION
from time import time
from OpenGL.GL import glViewport

class Base(object):
    def __init__(self, windowSize = [1024,768], windowTitle="Euler Framework") -> None:
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, GL_MAJOR_VERSION)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, GL_MINOR_VERSION)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(windowSize[0], windowSize[1], windowTitle, None, None)

        #make the window context current
        glfw.make_context_current(self.window)

        self.input = Input(self.window)
        glfw.set_key_callback(self.window, self.keyCallback)
        glfw.set_framebuffer_size_callback(self.window, self.frameBufferSizeCallback)
        glfw.set_cursor_pos_callback(self.window, self.cursorPosCallback)
        glfw.set_mouse_button_callback(self.window, self.mouseButtonCallback)
        
        self.timeStamp = time()

    # implement by extending class
    def initialize(self):
        pass
    
    # implement by extending class
    def update(self,dt=0):
        pass
    
    def updateDeltaTime(self):
        curTime = time()
        deltaTime= curTime - self.timeStamp
        self.timeStamp = curTime
        return deltaTime

    def run(self):
        # start up
        self.initialize()
        self.timeStamp = time()

        while not glfw.window_should_close(self.window):
            dt = self.updateDeltaTime()

            ## process input ##
            glfw.poll_events()
            self.input.update()

            ## update & render ##
            self.update(dt)

            glfw.swap_buffers(self.window)

        glfw.terminate()
    
    def keyCallback(self, window, key, scanCode, action, mode):
        self.input.receiveKeyEvent(key,action,mode)
    
    def frameBufferSizeCallback(self, window, width, height):
        glViewport(0,0,width,height)
    
    def cursorPosCallback(self, window, x, y):
        self.input.receiveCursorEvent(x, y)
    
    def mouseButtonCallback(self, window, button, action, mode):
        pos = glfw.get_cursor_pos(window)
        mouseEvt = MouseEvent(button,action,mode,pos)
        self.input.receiveMouseButtonEvent(mouseEvt)

if __name__ == "__main__":
    # Base().run()

    class Test(Base):
        def update(self):
            if self.input.keyDownList or self.input.keyPressedList or self.input.keyUpList:
                print("==========================================================")
                if len(self.input.keyDownList) > 0:
                    print("keys down: ", self.input.keyDownList)
                if len(self.input.keyPressedList) > 0:
                    print("keys pressed: ", self.input.keyPressedList)
                if len(self.input.keyUpList) > 0:
                    print("keys up: ", self.input.keyUpList)
    
    Test().run()