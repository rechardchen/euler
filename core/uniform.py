from OpenGL.GL import *

#TODO: support UBO

class Uniform(object):

    IntType = 0
    BoolType = 1
    FloatType = 2
    Vec2Type = 3
    Vec3Type = 4
    Vec4Type = 5
    Mat4Type = 6

    def __init__(self, dataType, data):
        self.dataType = dataType
        self.data = data
        self.variableRef = -1
    
    def locateVariable(self, programRef, variableName):
        self.variableRef = glGetUniformLocation(programRef, variableName)

    def uploadData(self):
        if self.variableRef == -1:
            print("upload uniform with no ref!")
            return
        
        if self.dataType in (Uniform.IntType, Uniform.BoolType):
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == Uniform.FloatType:
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == Uniform.Vec2Type:
            glUniform2f(self.variableRef, self.data[0], self.data[1])
        elif self.dataType == Uniform.Vec3Type:
            glUniform3f(self.variableRef, self.data[0],self.data[1],self.data[2])
        elif self.dataType == Uniform.Vec4Type:
            glUniform4f(self.variableRef, self.data[0],self.data[1],self.data[2],self.data[3])
        elif self.dataType == Uniform.Mat4Type:
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)
        else:
            raise Exception("Uniform slot {} has unknown dataType {}".format(self.variableRef, self.dataType))