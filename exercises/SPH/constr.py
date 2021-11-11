# -*- coding: utf-8 -*-


import numpy as np



def compute_k_coef(c,n):
    c.k_coef = 1-(1-c.stiffness)**(1.0/n)
#




class DistanceConstraint(object):

    def __init__(self,l0,stiff,i,j,posns):
        self.n=2
        self.indices = [i,j]
        self.positions = posns
        self.l0 = l0

        self.stiffness = stiff
        self.k_coef = 1.0 
    #

    def project_positions(self):
        i = self.indices[0]
        j = self.indices[1]
        pi = self.positions.get_pos(i)
        pj = self.positions.get_pos(j)
        d = pi-pj
        n = np.linalg.norm(d)
        C = n - self.l0

        W = self.positions.get_w(i) + self.positions.get_w(j)
        if n*W < 1e-8:
            return

        dp = self.k_coef*C*d/(n*W)
        dpi = - self.positions.get_w(i)*dp
        dpj =   self.positions.get_w(j)*dp

        pi = pi + dpi
        pj = pj + dpj

        self.positions.set_pos(i,pi)
        self.positions.set_pos(j,pj)
    #

    # For debug and info purposes
    def get_value(self):
        i = self.indices[0]
        j = self.indices[1]
        return np.linalg.norm(self.positions.get_pos(i)-self.positions.get_pos(j)) - self.l0
    #

#




class DistanceToPointConstraint(object):


    def __init__(self,p0,l0,stiff,i,posns):
        self.n=1
        self.indices = [i]
        self.positions = posns
        self.l0 = l0
        self.p0 = p0

        self.stiffness = stiff
        self.k_coef = 1.0 
    #

    def project_positions(self):
        # TODO: TPA implement
        pass
    #
#

class PointConstraint(DistanceToPointConstraint):

    def __init__(self,p0,stiff,i,posns):
        super(PointConstraint,self).__init__(p0,0.0,stiff,i,posns)
    #

#


class InDiscConstraint(object):
    def __init__(self,p0,l0,stiff,i,posns):
        self.n=1
        self.indices = [i]
        self.positions = posns
        self.l0 = l0
        self.p0 = p0

        self.stiffness = stiff
        self.k_coef = 1.0 
    #

    def project_positions(self):
        # TODO: TPA implement
        pass
    #
#



class BendingConstraint(object):
    """
    Bending constraint by kelager et al. 2010
    http://image.diku.dk/kenny/download/kelager.niebe.ea10.pdf
    """
    def __init__(self,ks,kc,i,j,m,posns):
        self.n=3
        self.indices = [i,j,m] # b0, b1, v
        self.stifness = ks
        self.k_coef = 1.0 

        self.glob_curv = kc
        self.positions = posns

        b0 = self.positions.get_pos(i)
        b1 = self.positions.get_pos(j)
        v = self.positions.get_pos(m)
        c = 1.0/3.0*(b0+b1+v)
        self.h0 = np.linalg.norm(v-c)
    #

    def project_positions(self):
        # TODO: TPA implement
        pass
    #
#

class CollisionConstraint(object):
    def __init__(self,p,n,i,posns):
        self.n = 1
        self.point = np.array(p).reshape( (3,1) )
        self.normal = np.array(n).reshape( (3,1) )
        self.indices = [i]
        self.positions = posns
        self.stiffness = 1.0

    #

    def project_positions(self):
        # el jacobiano es la normal
        dp = np.zeros((3,1))
        i = self.indices[0]
        pi = self.positions.get_pos(i)
        C = float((pi - self.point).transpose().dot(self.normal))

        if C < 0:
            dp = -self.k_coef*C*self.normal

        if C < 0:
            self.positions.set_pos(i,pi + dp)
        #
    #


#


class ClothBaloonConstraint(object):

    def __init__(self,posns,tris,overpressure = 1.0):
        self.positions=posns
        self.triangles=tris
        self.V0 = self.compute_vol()
        self.overpressure = overpressure
        self.stiffness = 1.0
        self.indices = range(posns.n)

    def compute_vol(self):
        V = 0
        for tri in self.triangles:
            p1 = self.positions.get_pos(tri[0])
            p2 = self.positions.get_pos(tri[1])
            p3 = self.positions.get_pos(tri[2])
            n = np.cross(p1.transpose(),p2.transpose())
            V += float(n.dot(p3))
        return V

    def project_positions(self):
        # TODO: TPA implement
        pass
   #

#
