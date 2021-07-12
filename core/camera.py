from .object3d import Object3D
from .matrix import makeIdentity,makePerspective
from numpy.linalg import inv

class Camera(Object3D):
    def __init__(self):
        super().__init__()
        self.projectionMatrix = makeIdentity()
        self.viewMatrix = makeIdentity()
    
    def setPerspective(self,angleOfView=60,aspectRatio=1,near=0.1,far=1000):
        self.projectionMatrix = makePerspective(angleOfView,aspectRatio,near,far)

    def updateViewMatrix(self):
        self.viewMatrix = inv(self.getWorldMatrix())
