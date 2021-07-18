from math import pi
from core.object3d import Object3D
from core.input import MouseEvent,MOUSE_BUTTON_RIGHT,PRESS,RELEASE,KEY_W,KEY_S,KEY_A,KEY_D
from core.matrix import *

TWO_PI=pi*2

class MovementRig(Object3D):
    def __init__(self, moveSpeed, mouseSpeed):
        super().__init__()

        # self.yaw = 0
        # self.pitch = 0

        self.moving = False
        self.moveSpeed = moveSpeed
        self.mouseSpeed = mouseSpeed
        self.mousePos = None
    
    # must be registered manually
    def mouseEvent(self, me, input):
        if me.button == MOUSE_BUTTON_RIGHT:
            if me.action == PRESS:
                self.moving = True
                self.mousePos = me.pos
                input.showCursor(False)
            elif me.action == RELEASE:
                self.moving = False
                self.mousePos = None
                input.showCursor(True)

    def update(self, dt, input):
        if not self.moving:
            return
        
        mouseCur = input.mousePos
        deltaX = mouseCur[0] - self.mousePos[0]
        deltaY = mouseCur[1] - self.mousePos[1]
        #reset mouse position
        input.setMousePos(self.mousePos[0], self.mousePos[1])

        # process rotation
        yaw = (-self.mouseSpeed*dt*deltaX) % TWO_PI
        pitch = (-self.mouseSpeed*dt*deltaY) % TWO_PI

        self.applyMatrix(makeRotationX(pitch))
        self.applyMatrix(makeRotationY(yaw))

        # process movement
        move = [0,0,0]
        moveDelta = self.moveSpeed * dt
        if input.isKeyPressed(KEY_W):
            # move foward
            move[2] -= moveDelta
        if input.isKeyPressed(KEY_S):
            move[2] += moveDelta
        if input.isKeyPressed(KEY_A):
            move[0] -= moveDelta
        if input.isKeyPressed(KEY_D):
            move[0] += moveDelta

        self.translate(*move)