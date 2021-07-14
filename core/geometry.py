from .attribute import Attribute
from OpenGL.GL import *
import numpy as np
from math import cos,sin,pi

#TODO: refactor other_attib mechanism
class Geometry(object):
    def __init__(self):
        self.primType = GL_TRIANGLES

        # vertex Data
        self.attributes     = {}
        self.vertexCount    = None

        # index data
        self.indexCount     = None
        self.indexBuffer    = None

        # vao
        self.vaoRef         = glGenVertexArrays(1)

    def addAttribute(self, dataType, variableName, data):
        self.attributes[variableName] = Attribute(dataType,data)
    
    def countVertices(self):
        attrib = list(self.attributes.values())[0]
        self.vertexCount = len(attrib.data)

    def setIndexBuffer(self, indices):
        # self.indexCount = len(indices)
        self.indexBuffer = glGenBuffers(1)
        indices = np.array(indices).astype(np.uint32)
        self.indexCount = indices.size

        glBindVertexArray(self.vaoRef)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexBuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.ravel(), GL_STATIC_DRAW)
        glBindVertexArray(0)
    
    def associateVariables(self, programRef):
        glBindVertexArray(self.vaoRef)

        for variableName, attributeObject in self.attributes.items():
            attributeObject.associateVariable(programRef, variableName)
        glBindVertexArray(0)

class Rectangle(Geometry):
    def __init__(self, width=1, height=1, other_attribs={}):
        """
        width and height provides the 'vertexPosition' attribute, and other_attribs includes others.
        other_attribs can be {'vertexColor':(Attrib.Vec3Type, [c0,c1,c2])}
        """
        super().__init__()

        p0 = [-width/2,-height/2,0]
        p1 = [width/2,-height/2,0]
        p2 = [width/2,height/2,0]
        p3 = [-width/2,height/2,0]
        positionData = [p0,p1,p2,p3]
        self.addAttribute(Attribute.Vec3Type, "vertexPosition", positionData)

        for k,v in other_attribs.items():
            assert len(v[1]) == len(positionData)
            self.addAttribute(v[0], k, v[1])
        
        self.setIndexBuffer([[0,1,2],[0,2,3]])
        self.countVertices()

class Box(Geometry):
    def __init__(self, width=1, height = 1, depth = 1, other_attribs={}):
        super().__init__()

        p0 = [-width/2,-height/2,-depth/2]
        p1 = [width/2,-height/2,-depth/2]
        p2 = [width/2,height/2,-depth/2]
        p3 = [-width/2,height/2,-depth/2]

        p4 = [-width/2,-height/2,depth/2]
        p5 = [width/2,-height/2,depth/2]
        p6 = [width/2,height/2,depth/2]
        p7 = [-width/2,height/2,depth/2]
        positionData = [p0,p1,p2,p3,p4,p5,p6,p7]
        self.addAttribute(Attribute.Vec3Type, "vertexPosition", positionData)

        for k,v in other_attribs.items():
            assert len(v[1]) == len(positionData)
            self.addAttribute(v[0], k, v[1])
        
        self.setIndexBuffer([[0,2,1],[0,3,2],
                             [0,4,7],[0,7,3],
                             [4,5,6],[4,6,7],
                             [5,1,2],[5,2,6],
                             [7,6,2],[7,2,3],
                             [4,0,1],[4,1,5]])
        self.countVertices()

class ParametricGeometry(Geometry):
    def __init__(self, uStart, uEnd, uResolution, 
                vStart, vEnd, vResolution, surfaceFunction, other_attribs={}):
        super().__init__()

        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / uResolution
        positions = []
        
        for uIndex in range(uResolution+1):
            u = uStart + uIndex*deltaU
            for vIndex in range(vResolution+1):
                v = vStart + vIndex*deltaV
                positions.append(surfaceFunction(u,v))
        self.addAttribute(Attribute.Vec3Type, "vertexPosition", positions)

        for k,v in other_attribs.items():
            # v[0] is dataType, v[1] is value function
            values = []
            valueFunc = v[1]
            for uIndex in range(uResolution+1):
                u = uStart + uIndex*deltaU
                for vIndex in range(vResolution+1):
                    v = vStart + vIndex*deltaV
                    values.append(valueFunc(u,v))
            self.addAttribute(v[0], k, values)
        
        # index buffer
        indices = []
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):
                i0 = yIndex + xIndex*(vResolution+1)
                i1 = i0 + 1
                i2 = i1 + vResolution + 1
                i3 = i2 - 1
                indices += [[i0,i1,i2],[i0,i2,i3]]
        self.setIndexBuffer(indices)

        self.countVertices()

class PlaneGeometry(ParametricGeometry):
    def __init__(self, width=1,height=1,widthSegment=8,heightSegment=8, other_attribs={}):
        def S(u,v):
            return [u,v,0]
        super().__init__(-width/2, width/2, widthSegment, -height/2, height/2, heightSegment, S, other_attribs)

class EllipsoidGeometry(ParametricGeometry):
    def __init__(self,width=1,height=1,depth=1,radiusSegments=32, heightSegments=16,other_attribs={}):
        def S(u,v):
            return [width/2*sin(u)*cos(v),
                    height/2*sin(v),
                    depth/2*cos(u)*cos(v)]
        super().__init__(0,2*pi,radiusSegments,-pi/2,pi/2,heightSegments,S,other_attribs)
    
class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1,radiusSegments=32,heightSegments=16,other_attribs={}):
        super().__init__(2*radius,2*radius,2*radius,radiusSegments,heightSegments,other_attribs)
