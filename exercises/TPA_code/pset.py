# -*- coding: utf-8 -*-


import numpy as np

class Particle:
    def __init__(self,mass = 1.0, pos = None, vel = None):
        
        if pos == None:
            pos = np.zeros((3,1))
        if vel == None:
            vel = np.zeros((3,1))
        self.m = mass
        self.p = pos
        self.last_p = pos # used in PBD
        self.v = vel

        self.press = 0.0
        self.dens = mass
        
        self.f_press = np.zeros((3,1))
        self.f_visco = np.zeros((3,1))
        self.f_surften = np.zeros((3,1))
        self.f = np.zeros((3,1))
        
        self.w = 1.0/mass # used in PBD
        
        self.fixed = False  # used for boundary conditions, e.g. in PBD
        
    #
    
    def set_pos(self,p):
        self.p[:] = np.array(p).reshape((3,1))
    #

    def set_vel(self,v):
        self.v[:] = np.array(v).reshape((3,1))
    #

    def set_force(self,f):
        self.f[:] = np.array(f).reshape((3,1))
    #

    def add_force(self,f):
        self.f[:] = self.f + np.array(f).reshape((3,1))
    #

#


class ParticleSet:
    def __init__(self,num=1,mass=1.0):
        self.setup(num,mass)
    #
    
    # A little bit of sugar to make a ParticleSet look like a list
    
    def __iter__(self):
        """ Returns an iterator for the particles list """
        return iter(self.pts)
    #
    
    def __getitem__(self,i):
        """ Returns the i-th particle object """
        return self.pts[i]
    #

    def setup(self,num=1,mass=1.0):
        """ An array of particles is set up"""
        self.n = num
        self.pts = [Particle(mass = mass) for i in range(self.n)]

    #

    def get_mass(self,k):
        return float(self.pts[k].m)
    #

    def get_w(self,k):
        return float(self.pts[k].w)
    #

    def get_pos(self,k):
        return self.pts[k].p
    #
    def get_vel(self,k):
        return self.pts[k].v
    #


    def set_mass(self,k,m):
        self.pts[k].m = m
        self.pts[k].w = 1.0/m

        self.pts[k].fixed = False
    #

    def set_fixed(self,k):
        self.pts[k].m = np.inf
        self.pts[k].w = 0.0

        self.pts[k].fixed = True
    #

    def set_pos(self,k,p):
        self.pts[k].set_pos( np.array(p).reshape((3,1)) )
    #

    def set_vel(self,k,v):
        self.pts[k].set_vel( np.array(v).reshape((3,1)) )
    #

    def translate(self,k,p):
        self.pts[k].set_pos( self.pts[k].p + np.array(p).reshape((3,1)))

    def translate_all(self,p):
        for i in range(self.n):
            self.translate(i,p)

    def add_force(self,k,f):
        self.pts[k].add_force(f)
    #

    def build_cube(self,n,dx,total_mass,centered=True,orig=np.zeros(3)):
        N = n**3
        self.setup(N,total_mass/N)

        if centered:
            orig -= dx*(n-1)*0.5

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    idx = k*n*n + i*n + j
                    self.set_pos(idx,(orig[0]+i*dx,orig[1]+j*dx,orig[2]+k*dx))
                #
            #
        #
    #


#


 
