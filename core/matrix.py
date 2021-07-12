import numpy as np
from math import cos,sin,pi,tan

def makeIdentity():
    return np.eye(4,dtype=np.float)

def makeTranslation(x,y,z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]],dtype=np.float)

def makeRotationX(angle):
    c,s = cos(angle),sin(angle)
    return np.array([[1,0,0,0],
                     [0,c,-s,0],
                     [0,s,c,0],
                     [0,0,0,1]],dtype=np.float)

def makeRotationY(angle):
    c,s = cos(angle),sin(angle)
    return np.array([[c,0,s,0],
                     [0,1,0,0],
                     [-s,0,c,0],
                     [0,0,0,1]],dtype=np.float)

def makeRotationZ(angle):
    c,s = cos(angle),sin(angle)
    return np.array([[c,-s,0,0],
                     [s,c,0,0],
                     [0,0,1,0],
                     [0,0,0,1]],dtype=np.float)

def makeScale(s):
    if type(s) in (list,tuple):
        sx,sy,sz = s[0],s[1],s[2]
    else:
        sx,sy,sz = s,s,s

    return np.array([[sx,0,0,0],
                     [0,sy,0,0],
                     [0,0,sz,0],
                     [0,0,0,1]],dtype=np.float)

def makePerspective(angleOfView=60,aspectRatio=1,near=0.1,far=1000):
    a = angleOfView*pi/180
    d = 1.0/tan(a/2)
    r = aspectRatio
    b = (far+near)/(near-far)
    c = 2*far*near/(near-far)
    return np.array([[d/r,0,0,0],
                     [0,d,0,0],
                     [0,0,b,c],
                     [0,0,-1,0]],dtype=np.float)

