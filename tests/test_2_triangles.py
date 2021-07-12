import sys
sys.path.append('.')

from core.base import Base
from core.openGLUtils import OpenGLUtils
from core.attribute import Attribute
from core.uniform import Uniform
from OpenGL.GL import *

class Test(Base):
    def initialize(self):
        vsCode = """
        in vec3 position;
        uniform vec3 translate;
        void main()
        {
            vec3 pos = position + translate;
            gl_Position = vec4(pos, 1.0);
        }
        """
        fsCode = """
        uniform vec3 baseColor;
        out vec4 fragColor;
        void main()
        {
            fragColor = vec4(baseColor, 1.0);
        }
        """
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        vaoRef = glGenVertexArrays(1)
        glBindVertexArray(vaoRef)
        positionData = [[0.0,0.2,0.0],[0.2, -0.2, 0.0],[-0.2,-0.2,0.0]]
        self.vertexCount = len(positionData)
        positionAttrib = Attribute(Attribute.Vec3Type, positionData)
        positionAttrib.associateVariable(self.programRef, "position")

        self.translate1 = Uniform(Uniform.Vec3Type, [-0.1,0.0,0.0])
        self.translate1.locateVariable(self.programRef, "translate")
        self.translate2 = Uniform(Uniform.Vec3Type, [0.1, 0.0, 0.0])
        self.translate2.locateVariable(self.programRef, "translate")
        self.baseColor1 = Uniform(Uniform.Vec3Type, [1.0, 0.0,0.0])
        self.baseColor1.locateVariable(self.programRef, "baseColor")
        self.baseColor2 = Uniform(Uniform.Vec3Type, [0.0,0.0,1.0])
        self.baseColor2.locateVariable(self.programRef, "baseColor")

        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_FRONT)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.programRef)

        self.translate1.uploadData()
        self.baseColor1.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

        self.translate2.uploadData()
        self.baseColor2.uploadData()
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

if __name__ == '__main__':
    Test().run()
