from core.object3d import Mesh
from core.geometry import Geometry
from core.attribute import Attribute
from material.basicMaterial import LineMaterial

class AxisHelper(Mesh):
    def __init__(self, axisLen=1,lineWidth=4,axisColors=[[1,0,0],[0,1,0],[0,0,1]]):
        geo = Geometry()

        positionData = [[0,0,0],[axisLen,0,0],
                        [0,0,0],[0,axisLen,0],
                        [0,0,0],[0,0,axisLen]]
        colorData = [axisColors[0],axisColors[0],
                     axisColors[1],axisColors[1],
                     axisColors[2],axisColors[2]]
        geo.addAttribute(Attribute.Vec3Type, "vertexPosition", positionData)
        geo.addAttribute(Attribute.Vec3Type, "vertexColor", colorData)
        geo.countVertices()

        mat = LineMaterial({'lineWidth': lineWidth,
                            'useVertexColor':True,
                            'lineType':'segments'})
        
        super().__init__(geo, mat)

class GridHelper(Mesh):
    def __init__(self, size = 10, division = 10, lineWidth=4, centerColor = [1,1,1], gridColor = [0,0,0]):
        geo = Geometry()
        
        sep = size / division
        positionData = []
        colorData = []

        #add horizontal lines
        for i in range(division + 1):
            y = -size/2 + i*sep
            positionData.extend([[-size/2, y, 0],[size/2, y, 0]])
            if i == division // 2:
                colorData.extend([centerColor, centerColor])
            else:
                colorData.extend([gridColor, gridColor])
        #add vertical lines
        for i in range(division + 1):
            x = -size /2 + i*sep
            positionData.extend([[x,-size/2,0],[x, size/2, 0]])
            if i == division // 2:
                colorData.extend([centerColor, centerColor])
            else:
                colorData.extend([gridColor, gridColor])
        
        geo.addAttribute(Attribute.Vec3Type, "vertexPosition", positionData)
        geo.addAttribute(Attribute.Vec3Type, "vertexColor", colorData)
        geo.countVertices()

        mat = LineMaterial({
            "lineWidth": lineWidth,
            "useVertexColor": True,
            "lineType": "segments"
        })

        super().__init__(geo, mat)