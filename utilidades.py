
import struct

def color(r, g, b):
    #print(str(r)+" "+str(g)+" "+str(b))
    return bytes([round(b * 255), round(g * 255), round(r * 255)])

#Reserva 1 Byte en memoria
def char(c):
    return struct.pack('=c', c.enconde('ascii'))

#Reserva 2 Byte en memoria
def word(w):
    return struct.pack('=h',w)

#Reserva 4 Byte en memoria
def dword(d):
    return struct.pack('=l',d)

#Funciones matematicas:

#Producto cruz
def crossProduct2x2(pointA, pointB):
    return (pointA[0]*pointB[1]) - (pointA[1]*pointB[0])

#Producto cruz
def crossProduct2x3(pointA, pointB):
    res = []
    res.append(pointA[1] * pointB[2] - pointA[2] * pointB[1])
    res.append(pointA[2] * pointB[0] - pointA[0] * pointB[2])
    res.append(pointA[0] * pointB[1] - pointA[1] * pointB[0])
    return res

#Producto punto
def dotProduct(pointA, pointB):
    product = 0
    for i in range(len(pointA)):
        product = product + pointA[i] * pointB[i]

    return product

#resta de puntos
def mySubtract(list1, list2):
    resta = []
    if (len(list2) >= len(list1)):
        for i in range(len(list1)):
            resta.append(list1[i]-list2[i])
    return resta

#Normalizar vector:
def normalizarVector(vector):

    #largo del vector
    largo =  (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5
    vector[0] = vector[0]/ largo
    vector[1] = vector[1] / largo
    vector[2] = vector[2] / largo
    return  vector

#Calcula coordenadas Barycentricas
def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B[1] - C[1])*(P[0] - C[0]) + (C[0] - B[0])*(P[1] - C[1]) ) /
              ((B[1] - C[1])*(A[0]- C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        v = ( ((C[1] - A[1])*(P[0] - C[0]) + (A[0] - C[0])*(P[1] - C[1]) ) /
              ((B[1] - C[1])*(A[0] - C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w




