from core.openGLUtils import OpenGLUtils
from core.uniform import Uniform

class Material(object):
    def __init__(self, vsCode, fsCode):
        self.programRef = OpenGLUtils.initializeProgram(vsCode, fsCode)

        self.uniforms = {}

        # add predefined uniforms
        self.uniforms['modelMatrix'] = Uniform(Uniform.Mat4Type, None)
        self.uniforms['viewMatrix'] = Uniform(Uniform.Mat4Type, None)
        self.uniforms['projectionMatrix'] = Uniform(Uniform.Mat4Type, None)

        self.settings = {}
    
    def addUniform(self, dataType, variableName, data):
        self.uniforms[variableName] = Uniform(dataType, data)
    
    def locateUniforms(self):
        for variableName, uniformObject in self.uniforms.items():
            uniformObject.locateVariable(self.programRef, variableName)
    
    def updateRenderSettings(self):
        pass

    def setProperties(self, properties):
        for name, data in properties.items():
            if name in self.uniforms:
                self.uniforms[name].data = data
            elif name in self.settings:
                self.settings[name] = data
            else:
                raise Exception("Material has no property named: "+name)
    
