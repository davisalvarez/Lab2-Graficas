import struct
from utilidades import *
class ModeloOBJ(object):

    def __init__(self, filename):
        m = open(filename,'r')

        self.lineas = m.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.traducir()


    def traducir(self):

        for line in self.lineas:
            if line:
                tipo, valor = line.split(' ', 1)

                #Vertices
                if tipo == 'v':
                    self.vertices.append(list(map(float,valor.split(' '))))
                # Normales
                elif tipo == 'vn':
                    self.normals.append(list(map(float,valor.split(' '))))
                # Texturas
                elif tipo == 'vt':
                    self.texcoords.append(list(map(float,valor.split(' '))))
                # Caras
                elif tipo == 'f':
                    caras =  valor.split(' ')
                    lista=[]
                    for cara in caras:
                        if cara!='':
                            c = cara.split('/')
                            vector=[]
                            for x in c:
                                try:
                                    vector.append(int(x))
                                except:
                                    print("no int")
                            lista.append(vector)
                    self.faces.append(lista)


class Texture(object):
    def __init__(self, filename):
        self.filename = filename
        self.traducir()

    def traducir(self):
        image = open(self.filename, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r, g, b))

        image.close()

    def getColor(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.width)
            y = int(ty * self.height)

            return self.pixels[y][x]
        else:
            return color(0, 0, 0)

