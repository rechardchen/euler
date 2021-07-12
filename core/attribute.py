from OpenGL.GL import *
import numpy as np

#TODO: Vertex Buffer

class Attribute(object):
    
    IntType = 0
    FloatType = 1
    Vec2Type = 2
    Vec3Type = 3
    Vec4Type = 4

    def __init__(self, dataType, data):
        self.dataType = dataType
        self.data = data

        self.bufferRef = glGenBuffers(1)
        self.uploadData()

    def uploadData(self):
        data = np.array(self.data).astype(np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def associateVariable(self, programRef, variableName):
        variableRef = glGetAttribLocation(programRef, variableName)
        if variableRef == -1:
            print("Variable '{}' not found in program!".format(variableName))
            return
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferRef)
        if self.dataType == Attribute.IntType:
            glVertexAttribPointer(variableRef, 1, GL_INT, False, 0, None)
        elif self.dataType == Attribute.FloatType:
            glVertexAttribPointer(variableRef, 1, GL_FLOAT, False, 0, None)
        elif self.dataType == Attribute.Vec2Type:
            glVertexAttribPointer(variableRef, 2, GL_FLOAT, False, 0, None)
        elif self.dataType == Attribute.Vec3Type:
            glVertexAttribPointer(variableRef, 3, GL_FLOAT, False, 0, None)
        elif self.dataType == Attribute.Vec4Type:
            glVertexAttribPointer(variableRef, 4, GL_FLOAT, False, 0, None)
        else:
            raise Exception("Attribute "+variableName + " has unknown type "+str(self.dataType))
        glEnableVertexAttribArray(variableRef)
    
    # def __del__(self):
    #     glDeleteBuffers(1,(self.bufferRef,))
        