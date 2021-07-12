import sys

sys.path.append('.')

from core.base import Base
from core.openGLUtils import OpenGLUtils
from OpenGL.GL import *
from core.attribute import Attribute
from core.matrix import *
from core.uniform import Uniform
import core.input as input
from math import pi

class Test(Base):
    def initialize(self):
        vsCode = """
        in vec3 position;
        uniform mat4 projection;
        uniform mat4 model;

        void main()
        {
            gl_Position = projection*model*vec4(position,1);
        }
        """

        fsCode = """
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(1,1,0,1);
        }
        """

        self.programRef = OpenGLUtils.initializeProgram(vsCode,fsCode)

        glClearColor(0,0,0,1)
        glEnable(GL_DEPTH_TEST)

        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)

        positionData = [[0,0.2,0],[0.1,-0.2,0],[-0.1,-0.2,0]]
        positionAttribute = Attribute(Attribute.Vec3Type, positionData)
        positionAttribute.associateVariable(self.programRef, "position")
        self.vertexCount = len(positionData)

        mMatrix = makeTranslation(0,0,-1)
        self.modelMatrix = Uniform(Uniform.Mat4Type, mMatrix)
        self.modelMatrix.locateVariable(self.programRef, "model")

        mMatrix = makePerspective()
        self.projectionMatrix = Uniform(Uniform.Mat4Type, mMatrix)
        self.projectionMatrix.locateVariable(self.programRef, "projection")

        self.moveSpeed = 0.5
        self.turnSpeed = 90*pi/180
    
    def update(self,dt):
        moveAmount = self.moveSpeed*dt
        turnAmount = self.turnSpeed*dt

        #global translations
        if self.input.isKeyPressed(input.KEY_W):
            m = makeTranslation(0,moveAmount,0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_S):
            m = makeTranslation(0,-moveAmount,0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_A):
            m = makeTranslation(-moveAmount,0,0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_D):
            m = makeTranslation(moveAmount,0,0)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_Z):
            m = makeTranslation(0,0,moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_X):
            m = makeTranslation(0,0,-moveAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        #global rotation
        if self.input.isKeyPressed(input.KEY_Q):
            m = makeRotationZ(turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        if self.input.isKeyPressed(input.KEY_E):
            m = makeRotationZ(-turnAmount)
            self.modelMatrix.data = m @ self.modelMatrix.data
        
        #local translation
        if self.input.isKeyPressed(input.KEY_I):
            m = makeTranslation(0,moveAmount,0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(input.KEY_K):
            m = makeTranslation(0,-moveAmount,0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(input.KEY_J):
            m = makeTranslation(-moveAmount,0,0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(input.KEY_L):
            m = makeTranslation(moveAmount,0,0)
            self.modelMatrix.data = self.modelMatrix.data @ m
        #local rotation
        if self.input.isKeyPressed(input.KEY_U):
            m = makeRotationZ(turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        if self.input.isKeyPressed(input.KEY_O):
            m = makeRotationZ(-turnAmount)
            self.modelMatrix.data = self.modelMatrix.data @ m
        
        # render scene
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.programRef)
        self.projectionMatrix.uploadData()
        self.modelMatrix.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

if __name__ == "__main__":
    Test().run()