from OpenGL.GL import *
from .material import Material
from core.uniform import Uniform

class BasicMaterial(Material):
    def __init__(self):
        vsCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;

        in vec3 vertexPosition;
        in vec3 vertexColor;
        out vec3 color;

        void main()
        {
            gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(vertexPosition, 1);
            color = vertexColor;
        }
        """
        fsCode = """
        uniform bool useVertexColor;
        uniform vec3 baseColor;
        in vec3 color;
        out vec4 fragColor;

        void main()
        {
            fragColor = useVertexColor?vec4(color*baseColor,1):vec4(baseColor,1);
        }
        """
        super().__init__(vsCode,fsCode)
        self.addUniform(Uniform.Vec3Type, "baseColor", [1.0,1.0,1.0])
        self.addUniform(Uniform.BoolType, "useVertexColor", True)
        self.locateUniforms()

class PointMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        self.settings['drawStyle'] = GL_POINTS
        self.settings['pointSize'] = 8
        self.settings['roundedPoints'] = False

        self.setProperties(properties)
    
    def updateRenderSettings(self):
        glPointSize(self.settings['pointSize'])

        if self.settings['roundedPoints']:
            glEnable(GL_POINT_SMOOTH)
        else:
            glDisable(GL_POINT_SMOOTH)
        
class LineMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        self.settings['drawStyle'] = GL_LINE_STRIP
        self.settings['lineWidth'] = 1
        self.settings['lineType'] = 'connected'

        self.setProperties(properties)
    
    def updateRenderSettings(self):
        glLineWidth(self.settings['lineWidth'])
        if self.settings['lineType'] == 'connected':
            self.settings['drawStyle'] = GL_LINE_STRIP
        elif self.settings['lineType'] == 'loop':
            self.settings['drawStyle'] = GL_LINE_LOOP
        elif self.settings['lineType'] == 'segments':
            self.settings['drawStyle'] = GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style.")
        
class SurfaceMaterial(BasicMaterial):
    def __init__(self, properties={}):
        super().__init__()

        self.settings['drawStyle'] = GL_TRIANGLES
        self.settings['doubleSide'] = False
        self.settings['wireframe'] = False
        self.settings['lineWidth'] = 1

        self.setProperties(properties)
    
    def updateRenderSettings(self):
        if self.settings['doubleSide']:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
        
        if self.settings['wireframe']:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLineWidth(self.settings['lineWidth'])

    
        
