from OpenGL.GL import *

GL_SHADER_PREFIX = "#version 430 core\n"
GL_MAJOR_VERSION = 4
GL_MINOR_VERSION = 3

class OpenGLUtils(object):
    
    @staticmethod
    def initializeShader(code, shaderType):
        shaderSrc = GL_SHADER_PREFIX + code
        shaderRef = glCreateShader(shaderType)
        glShaderSource(shaderRef,shaderSrc)
        glCompileShader(shaderRef)

        compileSuccess = glGetShaderiv(shaderRef, GL_COMPILE_STATUS)
        if not compileSuccess:
            errorMessage = glGetShaderInfoLog(shaderRef)
            errorMessage = "\n" + errorMessage.decode('utf8')
            glDeleteShader(shaderRef)
            raise Exception(errorMessage)
        return shaderRef
    
    @staticmethod
    def initializeProgram(vsCode, fsCode):
        vertexShaderRef = OpenGLUtils.initializeShader(vsCode, GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initializeShader(fsCode, GL_FRAGMENT_SHADER)
        programRef = glCreateProgram()
        glAttachShader(programRef,vertexShaderRef)
        glAttachShader(programRef,fragmentShaderRef)
        glLinkProgram(programRef)

        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)
        if not linkSuccess:
            errorMessage = glGetProgramInfoLog(programRef)
            errorMessage = '\n' + errorMessage.decode('utf8')
            glDeleteProgram(programRef)
            raise Exception(errorMessage)
        
        return programRef
    
    @staticmethod
    def printSystemInfo():
        print("Vendor:" + glGetString(GL_VERSION).decode('utf8'))
        print("Renderer: " + glGetString(GL_RENDERER).decode('utf8'))
        print("OpenGL version supported: "+glGetString(GL_VERSION).decode('utf8'))
        print("GLSL version supported: "+glGeetStr(GL_SHADING_LANGUAGE_VERSION).decode('utf8'))


