from utilidades import *
from ModeloOBJ import *
import random
import numpy as np

BLACK = color(0,0,0)
WHITE = color(1,1,1)
YELLOW = color(1,1,0)

class render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.default_color = BLACK
        self.vetex_color = WHITE
        self.pixels = []
        self.zBuffer = []
        self.xVP=0
        self.yVP = 0
        self.widthVP = 0
        self.heightVP = 0

    def glInit(self):
        self.iniciarFramebuffer(BLACK)

    def glCreateWindow(self, w, h):
        self.width = w
        self.height = h
        self.iniciarFramebuffer(BLACK)


    def iniciarFramebuffer(self, _color):
        self.pixels = []
        for y in range(self.height):
            linea=[]
            for x in range(self.width):
                linea.append(_color)
            self.pixels.append(linea)


    # Z-Buffer A.K.A  buffer de profundidad
    def iniciarZbuffer(self):
        self.zBuffer = []
        for y in range(self.height):
            linea = []
            for x in range(self.width):
                linea.append(-float('inf'))
            self.zBuffer.append(linea)

        #print(str(self.pixels))


        #self.pixels = [ [ BLACK for x in range(self.width)] for y in range(self.height) ]

    def glViewPort(self, x, y, width, height):
        self.xVP= x
        self.yVP = y
        self.widthVP = width
        self.heightVP = height

    def glClear(self):
        self.iniciarFramebuffer(self.default_color)
        self.iniciarZbuffer()


    def glClearColor(self, r, g, b):
        self.default_color=color(r, g, b)

    def glVertex(self, x, y):
        #pos X
        xIMG = self.xVP + (x+1)* (self.widthVP/2)
        #pos Y
        yIMG = self.yVP + (y+1)*(self.heightVP / 2)

        self.pintarPixelIMG(round(xIMG),round(yIMG))

        #print("x: "+str(xIMG))
        #print("y: " + str(yIMG))


    def pintarPixelIMG(self, x, y, color = None):
        try:

            self.pixels[y][x] = color or self.vetex_color
        except:
            print("pintarPixelIMG() Pixel fuera")

    def glColor(self, r, g, b):
        self.vetex_color=color(r, g, b)

    def glFinish(self):
        self.generar("gotham.bmp")
        self.glZBuffer("Luz.bmp")

    def glZBuffer(self, filename):

        imagen = open(filename, 'wb')

        #BITMAPFILEHEADER
        #14 Bytes

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14+40+ self.width * self.height * 3))  #4
        imagen.write(word(0)) #2
        imagen.write(word(0)) #2
        imagen.write(dword(14+40)) #4

        #BITMAPINFOHEADER
        #40 Bytes

        imagen.write(dword(40)) #4
        imagen.write(dword(self.width)) #4
        imagen.write(dword(self.height)) #4
        imagen.write(word(1)) #2
        imagen.write(word(24)) # 2
        imagen.write(dword(0)) # 4
        imagen.write(dword(self.width * self.height * 3))  # 4

        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zBuffer[x][y] != -float('inf'):
                    if self.zBuffer[x][y] < minZ:
                        minZ = self.zBuffer[x][y]

                    if self.zBuffer[x][y] > maxZ:
                        maxZ = self.zBuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zBuffer[x][y]
                print(str(depth))
                if depth == -float('inf') or math.isnan(depth):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                imagen.write(color(depth,depth,depth))

        """
        for y in range(self.height):
            for x in range(self.width):
                imagen.write(self.pixels[y][x])
        """
        imagen.close()

    def generar(self, filename):

        imagen = open(filename, 'wb')

        #BITMAPFILEHEADER
        #14 Bytes

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14+40+ self.width * self.height * 3))  #4
        imagen.write(word(0)) #2
        imagen.write(word(0)) #2
        imagen.write(dword(14+40)) #4

        #BITMAPINFOHEADER
        #40 Bytes

        imagen.write(dword(40)) #4
        imagen.write(dword(self.width)) #4
        imagen.write(dword(self.height)) #4
        imagen.write(word(1)) #2
        imagen.write(word(24)) # 2
        imagen.write(dword(0)) # 4
        imagen.write(dword(self.width * self.height * 3))  # 4

        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4
        imagen.write(dword(0))  # 4

        #self.pixels[11][11]=color(162,0,255)

        for y in range(self.height):
            for x in range(self.width):
                imagen.write(self.pixels[y][x])

        imagen.close()




    def glLine(self, x0, y0, x1, y1):
        # x0: x inicial de la linea
        x0 = round(self.xVP + (x0 + 1) * (self.widthVP / 2))
        # x1: x final de la linea
        x1 = round(self.xVP + (x1 + 1) * (self.widthVP / 2))
        # y0: y inicial de la linea
        y0 = round(self.yVP + (y0 + 1) * (self.heightVP / 2))
        # y1: y final de la linea
        y1 = round(self.yVP + (y1 + 1) * (self.heightVP / 2))

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        cambioPixel = 0
        cambiar = 0.5

        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.pintarPixelIMG(y, x)
            else:
                self.pintarPixelIMG(x, y)

            cambioPixel += m
            if cambioPixel >= cambiar:
                if y1 > y0:
                    y += 1
                else:
                    y -= 1
                cambiar += 1

    def glLineIMG(self, x0, y0, x1, y1):

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        cambioPixel = 0
        cambiar = 0.5

        try:
            m = dy / dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.pintarPixelIMG(y, x)
                else:
                    self.pintarPixelIMG(x, y)

                cambioPixel += m
                if cambioPixel >= cambiar:
                    if y1 > y0:
                        y += 1
                    else:
                        y -= 1
                    cambiar += 1

    def transform(self, vertex, translate=(0,0,0), scale=(1,1,1)):
        """
        print(str(round(vertex[0]*scale[0] + translate[0])))
        print(str(round(vertex[1] * scale[1] + translate[1])))
        print(str(round(vertex[2] * scale[2] + translate[2])))

        var = input("ya")
        """
        return (round(vertex[0]*scale[0] + translate[0]),
                round(vertex[1]*scale[1] + translate[1]),
                round(vertex[2]*scale[2] + translate[2]))

    def paintModelOBJ(self, filename, translate = (0,0,0), scale = (1,1,1), isWireframe = False, texture = None):
        model = ModeloOBJ(filename)
        light = (0,0,1)

        for cara in model.faces:

            vertices = len(cara)

            if isWireframe:

                for vert in range(vertices):
                    v1 = model.vertices[cara[vert][0] - 1]
                    v2 = model.vertices[cara[(vert + 1) % vertices][0]-1]

                    v1 = self.transform(v1, translate, scale)
                    v2 = self.transform(v2, translate, scale)

                    #self.pintarPixelIMG(x1, y1)
                    self.glLineIMG(v1[0], v1[1], v2[0], v2[1])

            else:
                pologon= []
                listaText = []
                #print(str(cara))
                for vert in range(vertices):
                    v1 = model.vertices[cara[vert][0] - 1]

                    v1 = self.transform(v1, translate, scale)
                    pologon.append(v1)
                    #x0 = round(v1[0] * scale[0] + translate[0])
                    #y0 = round(v1[1] * scale[1] + translate[1])

                    if texture:
                        vt = model.texcoords[cara[vert][1]-1]
                        listaText.append(vt)
                    else:
                        listaText.append((0,0))


                normal = crossProduct2x3(mySubtract(pologon[1], pologon[0]), mySubtract(pologon[2], pologon[1]))

                #Normalizamos
                normal = normalizarVector(normal)

                intensity = dotProduct(normal, light)
                #print(str(intensity))
                if intensity >= 0:
                    print("Modelando")
                    self.earClipping(pologon, texture = texture, texcoords = listaText, intensity = intensity)


    def paintPoly(self, poly):
        largo = len(poly)

        for point in range(largo):
            v1 = poly[point]
            v2 = poly[(point + 1) % largo]
            self.glLineIMG(v1[0],v1[1],v2[0],v2[1])

    def fillTriangle(self, A, B, C, _color = None):

        def flatBottom(v1, v2, v3):

            for y in range(v1[1], v3[1]+1):

                xi = round( v1[0] + (v3[0] - v1[0])/(v3[1] - v1[1])*(y - v1[1]) )
                xf = round( v2[0] + (v3[0] - v2[0])/(v3[1] - v2[1])*(y - v2[1]) )

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.pintarPixelIMG(x,y, _color)

            #self.paintPoly([v1, v2, v3])

        def flatTop(v1, v2, v3):

            for y in range (v1[1], v3[1]+1):
                xi = round( v2[0] + (v2[0] - v1[0])/(v2[1] - v1[1])*(y - v2[1]) )
                xf = round( v3[0] + (v3[0] - v1[0])/(v3[1] - v1[1])*(y - v3[1]) )

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.pintarPixelIMG(x, y, color)

        #Aseguramos la forma del triangulo

        if A[1] > B[1]:
            A, B = B, A
        if A[1] > C[1]:
            A, C = C, A
        if B[1] > C[1]:
            B, C = C, B
        if A[1]==C[1]:
            return

        if A[1] == B[1]: #flatBottom
            flatBottom(A, B, C)
        elif B[1] == C[1]: #flatTop
            flatTop(A, B, C)
        else: #Otro caso

            xD = A[0] + (C[0] - A[0])/(C[1] - A[1]) * (B[1] - A[1])

            D=(round(xD), B[1])


            #Dividimos el triangulo en 2
            flatBottom(D, B, C)
            flatTop(A, B, D)

    def polyOrientation(self, polygon):
        sumPX = 0
        lar = len(polygon)

        for p in range(lar):
            sumPX += crossProduct2x2(polygon[p], polygon[(p + 1) % lar])
        return sumPX


    def earClipping(self, polygon, _color = None, texture = None, texcoords = (), intensity = 1):

        #Calculamos la orientación del poligon
        ori = self.polyOrientation(polygon)

        #verificamos si es CW
        if ori > 0:
            polygon.reverse()
       #print(str(polygon))
        r = 0
        g = 0
        b = 0
        while(len(polygon) >= 3):
            pz = len(polygon)
            pz2 = len(polygon)
            #print("len: "+str(len(polygon)))
            isTriRemove = True

            print("poly: " + str(pz) + " vt: " + str(len(texcoords)))
            for point in range(pz):
            #point = 0
            #while(point < pz):
                #if(point+2 >= pz2):
                #    print("STOPPPP!")
                #    break

                #print("pz: "+str(pz)+" point: "+str(point)+" len: "+str(len(polygon)))
                v1 = polygon[point]
                v2 = polygon[(point + 1) % pz]
                v3 = polygon[(point + 2) % pz]
                #point += 1
                oriT = self.polyOrientation([v1, v2, v3])

                if oriT > 0:
                    #print(str(oriT)+" > 0")
                    continue

                #verificar si tiene punto adentro
                for x in polygon:
                    d1 = self.polyOrientation([x, v1, v2] )
                    d2 = self.polyOrientation([x, v2, v3])
                    d3 = self.polyOrientation([x, v3, v1])
                    #print("1- "+str(d1)+" 2>"+str(d2)+" 3>"+str(d3))
                    if (d1 > 0 and d2 > 0 and d2 > 0):
                        #tiene punto
                        continue


                isTriRemove = False
                #self.fillTriangle(v1, v2, v3, _color)


                #intento:
                vt1 = texcoords[point]
                vt2 = texcoords[(point + 1) % pz]
                vt3 = texcoords[(point + 2) % pz]


                print(v1)
                self.triangle_bc(v1, v2, v3, texture = texture, texcoords = (v1,vt2, vt3) , intensity = intensity )
                polygon.remove(polygon[(point + 1) % pz])
                pz2 -= 1
                #pz = len(polygon)
                #self.paintPoly(polygon)
                #if(point > pz):
                break
            if isTriRemove:
                break









    def fillPoly(self, polygon, translate = (0,0,0), scale = (1,1,1)):

        v0 = polygon[0]
        v1 = polygon[1]
        v2 = polygon[2]

        v0 = self.transform(v0, translate, scale)
        v1 = self.transform(v1, translate, scale)
        v2 = self.transform(v2, translate, scale)

        self.earClipping(polygon, color(random.randint(0, 255) / 255, random.randint(0, 255)/ 255, random.randint(0, 255)/ 255) )
        #self.fillTriangle(v0, v1, v2)


    #Coordendas Barycentricas
    def triangle_bc(self, A, B, C, _color = WHITE, texture = None, texcoords = (), intensity = 1):

        minX = min(A[0], B[0], C[0])
        minY = min(A[1], B[1], C[1])
        maxX = max(A[0], B[0], C[0])
        maxY = max(A[1], B[1], C[1])

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C,(x, y))

                if u >= 0 and v >= 0 and w >= 0:
                    #self.pintarPixelIMG(x, y, _color)

                    z = A[2] * u + B[2] * v + C[2] * w

                    if z > self.zBuffer[y][x]:

                        b, g, r = _color
                        b /= 255
                        g /= 255
                        r /= 255

                        b *= intensity
                        g *= intensity
                        r *= intensity

                        if texture:
                            ta, tb, tc = texcoords
                            tx = ta[0] * u + tb[0] * v + tc[0] * w
                            ty = ta[1] * u + tb[1] * v + tc[1] * w

                            texColor = texture.getColor(tx, ty)
                            b *= texColor[0] / 255
                            g *= texColor[1] / 255
                            r *= texColor[2] / 255
                        print("sup")
                        self.pintarPixelIMG(x, y, color(r,g,b))
                        self.zBuffer[y][x] = z

#eliminar!!
    def loadModel(self, filename, translate = (0,0,0), scale = (1,1,1), texture = None,  isWireframe = False):
        model = ModeloOBJ(filename)
        light = (0,0,1)

        for face in model.faces:

            vertCount = len(face)

            if isWireframe:
                for vert in range(vertCount):
                    v0 = model.vertices[ face[vert][0] - 1 ]
                    v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]
                    v0 = V2(round(v0[0] * scale.x  + translate.x),round(v0[1] * scale.y  + translate.y))
                    v1 = V2(round(v1[0] * scale.x  + translate.x),round(v1[1] * scale.y  + translate.y))
                    self.glLine_coord(v0, v1)
            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]
                if vertCount > 3:
                    v3 = model.vertices[ face[3][0] - 1 ]

                v0 = self.transform(v0,translate, scale)
                v1 = self.transform(v1,translate, scale)
                v2 = self.transform(v2,translate, scale)
                if vertCount > 3:
                    v3 = self.transform(v3,translate, scale)

                if texture:
                    vt0 = model.texcoords[face[0][1] - 1]
                    vt1 = model.texcoords[face[1][1] - 1]
                    vt2 = model.texcoords[face[2][1] - 1]
                    vt0 = (vt0[0], vt0[1])
                    vt1 = (vt1[0], vt1[1])
                    vt2 = (vt2[0], vt2[1])
                    if vertCount > 3:
                        vt3 = model.texcoords[face[3][1] - 1]
                        vt3 = (vt3[0], vt3[1])
                else:
                    vt0 = (0,0)
                    vt1 = (0,0)
                    vt2 = (0,0)
                    vt3 = (0,0)

                normal = np.cross(np.subtract(v1,v0), np.subtract(v2,v0))
                normal = normal / np.linalg.norm(normal)
                intensity = np.dot(normal, light)

                if intensity >=0:
                    self.triangle_bc(v0,v1,v2, texture = texture, texcoords = (vt0,vt1,vt2), intensity = intensity )
                    if vertCount > 3: #asumamos que 4, un cuadrado
                        self.triangle_bc(v0,v2,v3, texture = texture, texcoords = (vt0,vt2,vt3), intensity = intensity)


















