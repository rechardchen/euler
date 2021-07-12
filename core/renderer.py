from OpenGL.GL import *
from .object3d import Mesh

class Renderer(object):
    def __init__(self, clearColor=[0,0,0]):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(clearColor[0], clearColor[1], clearColor[2], 1)
    
    def render(self, scene, camera):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        camera.updateViewMatrix()
        
        meshFilter = lambda x:isinstance(x,Mesh)
        for mesh in filter(meshFilter, scene.descendantIter()):
            if not mesh.visible:
                continue
            
            glUseProgram(mesh.material.programRef)
            glBindVertexArray(mesh.geometry.vaoRef)

            #update uniform variables stored outside of Material
            mesh.material.uniforms['modelMatrix'].data = mesh.getWorldMatrix()
            mesh.material.uniforms['viewMatrix'].data = camera.viewMatrix
            mesh.material.uniforms['projectionMatrix'].data = camera.projectionMatrix

            for variableName, uniformObject in mesh.material.uniforms.items():
                uniformObject.uploadData()
            
            #update render states
            mesh.material.updateRenderSettings()

            drawStyle = mesh.geometry.primType
            if 'drawStyle' in mesh.material.settings:
                drawStyle = mesh.material.settings['drawStyle']
            if mesh.geometry.indexBuffer is not None: # drawElments
                glDrawElements(drawStyle, mesh.geometry.indexCount, GL_UNSIGNED_INT, None)
            else:
                glDrawArrays(drawStyle, 0, mesh.geometry.vertexCount)