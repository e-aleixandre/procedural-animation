import numpy as np

class hash:
    
    
    def __init__(self,N,dx):
        self.N = N
        self.dx = dx
        self.keys = []
        self.table = [[] for i in range(self.N)]
        self.neighs = [[] for i in range(self.N)]
        self.cellID = self.hash_func

        
    def hash_func(self,p):
        (x,y,z) = p
        i = int(x/self.dx)
        j = int(y/self.dx)
        k = int(z/self.dx)
        #
        index = (73856093 * i + 19349663 * j + 83492791 * k) % self.N
        #
        return index
    #

    def insert(self,key,value):
        id = self.hash_func(key)
        if len(self.table[id]) == 0:
            self.keys.append(key)
        self.table[id].append(value)

    def computeNeighbors(self,d=1):
        self.neighs = [[] for i in range(self.N)]
        r = range(-d,d+1,1)

        for key in self.keys:
            cell0 = self.hash_func( key )
            for direc in [ ( x  ,  y  ,  z)  for x in r for y in r for z in r ]:
                cell = self.hash_func( ( key[0] + direc[0]*self.dx ,  key[1] + direc[1]*self.dx ,  key[2] + direc[2]*self.dx ) )
                self.neighs[cell0].extend( self.table[cell] )
    #

    def getNeighbors(self,p):
        pt = (p[0],p[1],p[2])
        cell = self.hash_func(pt)
        return self.neighs[cell]

    def clear(self):
        self.table = [[] for i in range(self.N)]








class grid:
    
    
    
    def __init__(self,dx):
        self.dx = dx
        self.table = {}
        self.neighs = {}
        self.cellID = self.gridFunc

    #

    def gridFunc(self, p ):
        (x,y,z) = p
        i = int(x/self.dx)
        j = int(y/self.dx)
        k = int(z/self.dx)

        return (i,j,k)
    #

        
    
    def insert(self,coords,value):
        p = (coords[0] , coords[1] , coords[2])
        cell = self.gridFunc(p)
        if cell not in self.table :
            self.table[cell] = [value]
        else:
            self.table[cell].append(value)

    def computeNeighbors(self):
        self.neighs = {}
        r = [-1,0,1]
        for cell in self.table:
            self.neighs[cell] = []
            #print "clave:",cell, "valor:",self.table[cell]
            for direc in [ (cell[0]+x,  cell[1]+y,  cell[2]+z)  for x in r for y in r for z in r ]:
                #print "   Vecino:", direc
                if direc in self.table:
                    #print "       '-->", self.table[direc]
                    self.neighs[cell].extend( self.table[direc] )
            #print "Lista final de vecions:",sorted(self.neighs[cell])


    def getNeighbors(self,p):
        pt = (p[0],p[1],p[2])
        cell = self.gridFunc(pt)
        if cell in self.neighs:
            return self.neighs[cell]
        else:
            return []
    
    def getCell(self,p):
        pt = (p[0],p[1],p[2])
        cell = self.gridFunc(pt)
        if cell in self.table:
            return self.table[cell]
        else:
            return []
        

    def clear(self):
        self.table = {}
    #
