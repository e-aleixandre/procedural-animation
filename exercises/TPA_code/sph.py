# -*- coding: utf-8 -*-
"""
Created on Mon Nov 9 09:34:00 2015

@author: ignacio
"""
import argparse
from time import time
import numpy as np

from pset import ParticleSet
from geometries import build_cube
import kernels
import gridhash


    

class Domain:
    """ Data structure to describe the problem domain"""

    def __init__(self,dom=[-1.0,1.0,-1.0,1.0,-1.0,1.0]):
        self.x_min = dom[0]
        self.x_max = dom[1]
        self.y_min = dom[2]
        self.y_max = dom[3]
        self.z_min = dom[4]
        self.z_max = dom[5]
        
    def __str__(self):
        """ Transforms to string - useful for print """
        s = str(self.x_min) + " "
        s += str(self.x_max) + " "
        s += str(self.y_min) + " "
        s += str(self.y_max) + " "
        s += str(self.z_min) + " "
        s += str(self.z_max)
        return s


class SPHSystem:
    """ Class to simulate a fluid using SPH
    
    """

    def __init__(self):
        """ Constructor """
        
        self.particles = ParticleSet()


        """ Basic fluid parameters """
        self.density0 = 998.0
        self.viscosity = 0.1
        self.stiffness = 3.0
        self.surften = 1.0
        self.surften_threshold = 1.0
        
        self.col_restitution = 0.6

        self.kernel_parts = 27
        
        self.fluid_volume = 0.001 # 1l of fluid

        self.gravity = [0.0,0.0,-9.81]
        self.set_grav()

        """ Smoothing kernels """
        self.h = 0.01
        self.grid = gridhash.grid(self.h)
        self.kernel = kernels.StandardKernel(self.h)
        self.pkernel = kernels.SpikyKernel(self.h)
        self.vkernel = kernels.ViscosityKernel(self.h)
        
        """ Simulation domain """
        self.domain = Domain()
        
    #


    def set_grav(self):
        """ Sets up gravity vector """
        self.grav_acc = np.array(self.gravity).reshape((3,1))
    #

    def set_smoothing_length(self):
        """ Computation of the smoothing length
        
        To guarantee that we have kernel_part particles (in average)
        inside the kernel's support (Kelager)
        We compute the redius of an sphere that has the same
        volume as kernel_part particles.
        """

        # TODO: compute the smooting length
        self.h = 1.0 #TPA
        self.h2 = self.h**2

        self.grid = gridhash.grid(self.h)

        self.kernel = kernels.StandardKernel(self.h)
        self.pkernel = kernels.SpikyKernel(self.h)
        self.vkernel = kernels.ViscosityKernel(self.h)
    #
        

    def setup_fluid(self,n):
        """ Prepare data for a fluid with n particles
        
        This function is used when data is loaded, and build_fluid is not called 
        Before calling this function, fluid_volume, density and kernel_parts have to be defined.
        """

        particle_mass = 1.0 # TPA

        self.particles.setup(n,particle_mass)

        self.set_grav()

        self.set_smoothing_length()
        
        # Print fluid
        print("\nCONFIGURATION [setup_fluid]:")
        print("A fluid with total volume: "+str(self.fluid_volume))
        print("Density is "+str(self.density0))
        print("We have "+str(n)+" particles with mass "+str(self.particles[0].m))
        print("and volume "+str(self.fluid_volume/n))
        print("With an smoothing length of "+str(self.h)+", which should yield "+str(self.kernel_parts)+" neighbours (aprox)")

        
        

    def build_fluid(self, dens  = None, visco  = None, stiffness = None, surftens = None,
                         kernel_part = None, centered = True, orig = [0.0,0.0,0.0],
                         cube = False, edge = 0.1, ppedge = 5, fluid_volume = None,
                         positions = None, velocities = None):

        """ Build a fluid system 

            dens: fluid density
            visco: fluid viscosity
            stiffness: pressure stiffness
            surftens: surface tension coefficient
            kernel_part: number of particles inside a kernel (average)
            centered: create the cube centered in the origin
            orig: origin
            cube: build a cube
            edge: cube edge
            ppedge: particles per edge
            fluid_volume: volume of the fluid
            positions: vector of particle positions
            velocities: vector of particle velocities
            Note: some of the parameters are conflicting. E.g. if cube=True, then
            positions and velocities are ignored.
        """

        if dens is not None:
            self.density0 = dens

        if visco is not None:
            self.viscosity = visco

        if stiffness is not None:
            self.stiffness = stiffness

        if surftens is not None:
            self.surften = surftens

        if kernel_part is not None:
            self.kernel_parts = kernel_part
            
        if fluid_volume is not None:
            self.fluid_volume = fluid_volume


        # Check input parameters
        use_velocities = True
        if not cube:
            if positions is None:
                cube = True
            elif len(positions)%3:
                cube = True
            elif velocities is None or len(positions) != len(velocities):
                use_velocities = False

        print("Building fluid...")

        if cube:
            # we build a cubic shape, using an external function
            # TODO: initialize anything that is labelled with TPA
            # total fluid volume, total mass and distance between particles
            self.fluid_volume = 1.0 # TPA
            total_mass = 1.0 # TPA
            dist_parts = 1.0 # TPA
            
            # Params are: system,n,dx,total_mass
            build_cube(self,ppedge,dist_parts,total_mass)
            print("Cube built")
            n = self.particles.n
        else:
            # the number of particles is got from the vector of locations
            n = int(len(positions)/3)

            # TODO: compute particle mass and total mass
            particle_mass = 1.0 # TPA
            total_mass = 1.0 # TPA

            self.particles.setup(n,particle_mass)

            for i in range(n):
                # The positions and velocities are stored
                # They come as a large column vector of 3*n files
                pos = np.array(orig) + np.array(positions[3*i:3*i+3])

                vel = np.zeros(3)
                if use_velocities:
                    vel = np.array(velocities[3*i:3*i+3])

                self.particles.set_pos(i,pos)
                self.particles.set_vel(i,vel)
            #
            print("Building from position set")
        #

        self.set_grav()

        self.set_smoothing_length()

        # Uncomment to see all parameters
        print("\nCONFIGURATION [build_fluid]:")
        print("A volume of fluid with total volume: "+str(self.fluid_volume))
        print("Viscosity: mu="+str(self.viscosity)+". Stiffness: k="+str(self.stiffness))
        print("Surface tension: nu="+str(self.surften)+". Threshold: "+str(self.surften_threshold))
        if cube:
            print("A cube of edge "+str(edge)+" has been built")
            print("particles per edge: "+str(ppedge)+" at a distance "+str(dist_parts))            
        print("Density is "+str(dens)+" with total mass "+str(total_mass))
        print("We have "+str(n)+" particles with mass "+str(self.particles[0].m))
        print("With an smoothing length of "+str(self.h)+", which should yield "+str(self.kernel_parts)+" neighbours (aprox)")
    #


    def fill_grid(self):
        """ Compute grid stuff for neighbor detection """
        self.grid.clear()
        for i in range(self.particles.n):
            self.grid.insert(self.particles.get_pos(i),i)
        #
    #


    def compute_dens(self):
        """ Compute particles density and pressure """

        for cell in self.grid.table:

            neighs = self.grid.neighs[cell]

            for i in self.grid.table[cell]:
                # TODO: compute density and pressure
                # i is the index of each particle in the cell
                # e.g. you can access position as
                # p = self.particles.get_pos(i)
                self.particles[i].dens = 1.0 # TPA
                self.particles[i].press = 1.0 # TPA
    #

    def pressure_force(self):
        """ Compute pressure force """
        for cell in self.grid.table:

            neighs = self.grid.neighs[cell]

            for i in self.grid.table[cell]:
                # TODO: compute pressure force
                # i is the index of each particle in the cell
                # e.g. you can access position as
                # p = self.particles.get_pos(i)

                self.particles[i].f_press = np.zeros((3,1)) # TPA


    def viscosity_force(self):
        """ Compute viscosity force """
        for cell in self.grid.table:

            neighs = self.grid.neighs[cell]

            for i in self.grid.table[cell]:
                # TODO: compute viscosity force
                # i is the index of each particle in the cell
                # e.g. you can access position as
                # p = self.particles.get_pos(i)

                self.particles[i].f_visco = np.zeros((3,1)) # TPA
    ####


    def surface_tension_force(self):
        """ Compute surface tension force """
        for cell in self.grid.table:

            neighs = self.grid.neighs[cell]

            for i in self.grid.table[cell]:
                # TODO: compute surf. ten. force
                # i is the index of each particle in the cell
                # e.g. you can access position as
                # p = self.particles.get_pos(i)
                
                self.particles[i].f_surften = np.zeros((3,1)) # TPA
    #
    
    def check_domain(self):
        """ Confine particles inside the domain """
        parts = self.particles
        dom = self.domain
        e = self.col_restitution
        # tangential energy conservation.
        # TODO: Set as attribute
        b = 1.0 
        
        for i in range(parts.n):

            p = parts.get_pos(i)
            v = parts.get_vel(i)

            if p[0] < dom.x_min:
                p[0] = dom.x_min
                if v[0] < 0.0:
                    v[0] *= -e
                v[1] *= b
                v[2] *= b
            elif p[0] > dom.x_max:
                p[0] = dom.x_max
                if v[0] > 0.0:
                    v[0] *= -e
                v[1] *= b
                v[2] *= b

            if p[1] < dom.y_min:
                p[1] = dom.y_min
                if v[1] < 0.0:
                    v[1] *= -e
                v[0] *= b
                v[2] *= b
            elif p[1] > dom.y_max:
                p[1] = dom.y_max
                if v[1] > 0.0:
                    v[1] *= -e
                v[0] *= b
                v[2] *= b

            if p[2] < dom.z_min:
                p[2] = dom.z_min
                if v[2] < 0.0:
                    v[2] *= -e
                v[0] *= b
                v[1] *= b
            elif p[2] > dom.z_max:
                p[2] = dom.z_max
                if v[2] > 0.0:
                    v[2] *= -e
                v[0] *= b
                v[1] *= b

            parts.set_pos(i,p)
            parts.set_vel(i,v)

    
    
    
    def solve(self,dt):
        """ Simulation step """

        for par in self.particles:
            par.set_force(np.zeros((3,1)))

        self.fill_grid()
        t_pre_grid = time()
        self.grid.computeNeighbors()
        print("Grid building took "+str(time() - t_pre_grid)+'s')
        
        t_pre_dens = time()
        self.compute_dens()
        print("Density computation took "+str(time() - t_pre_dens)+'s')

        t_pre_forces = time()
        
        t_pre_press = time()
        self.pressure_force()
        print("Pressure force computation took "+str(time() - t_pre_press)+'s')
    
        if self.viscosity > 0.0:
            t_pre_visco = time()
            self.viscosity_force()
            print("Viscosity force computation took "+str(time() - t_pre_visco)+'s')
    
        if self.surften > 0.0:
            t_pre_sten = time()
            self.surface_tension_force()
            print("Surface tension computation took "+str(time() - t_pre_sten)+'s')

        print("Forces computation took "+str(time() - t_pre_forces)+'s')

            
        """ We add forces to particles """        
        for i in range(self.particles.n):
            self.particles[i].add_force(self.particles[i].f_press)
            if self.viscosity > 0.0:
                self.particles[i].add_force(self.particles[i].f_visco)
            if self.surften > 0.0:
                self.particles[i].add_force(self.particles[i].f_surften)


        """ We integrate the state of the particles """                        
        for part in self.particles:
            # Integrate velocities
            part.v += dt*(part.f/part.dens + self.grav_acc)
            part.v *= 0.999 # Artificial damping
            # Integrate positions
            part.p += dt*part.v
        
        # Check domain
        self.check_domain()

    #
#




if __name__=="__main__":
    parser = argparse.ArgumentParser(description="SPH fluid simulation")
    
    parser.add_argument('n',type=int,default=10)
    parser.add_argument('-te',type=float,default=1.0,dest='t_e')
    args = parser.parse_args()
    
    p_edge = args.n
    print("Silly SPH test with n={}.".format(p_edge))
    
    fluid = SPHSystem()
    # n,dx,dens,mass,sm_len
    fluid.build_fluid(ppedge=p_edge,edge = 1.8,dens = 980, kernel_part=35)
    for i in range(2):
        fluid.solve(0.01)
        print('step')
#
