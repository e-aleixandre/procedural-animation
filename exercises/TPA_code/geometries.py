# -*- coding: utf-8 -*-

from pset import ParticleSet



def build_cube(system,n,dx,total_mass):
    N = n*n*n
    system.particles = ParticleSet(N,total_mass/N)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                idx = i*n*n + j*n + k
                system.particles.set_pos(idx,(i*dx,j*dx,k*dx))
            #
        #
    #
#


