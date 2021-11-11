#!/usr/bin/python3
import sys
import argparse
from time import localtime, strftime,time

import sph
import file_io as fio

class ParticleSimulation:
    def __init__(self,system = None,slabel=""):
        self.t_ini = 0.0
        self.t_fin = 1.0
        self.t_step = 0.1
        self.final_step_tol = 1e-5
        
        self.nparts = 100
        
        self.scene_file = None
        
        self.parallel = True
        self.nprocs = 0
        
        self.kernel_parts = 27
        self.fluid_volume = 0.1
        
        self.gravity = [0.0,0.0,-9.81]

        if system is not None:
            self.system = system
            self.nparts = system.particles.n
        else:
            self.system = sph.SPHSystem()
            self.system.setup_fluid(self.nparts)
        
        self.label = slabel
    ###

        
    def load(self,scene_file):
        self.scene_file = scene_file
        fio.load_scene(scene_file,self)

        param_file = scene_file[:-4]+'.prm'
        init_conds_file = scene_file[:-4]+'.dat'
        domain_file = scene_file[:-4]+'.dom'
            
        # If there is a system, we create a new one.
        self.system = sph.SPHSystem()        
        fio.load_sph_params(param_file,self.system)
        self.system.kernel_parts = self.kernel_parts
        self.system.fluid_volume = self.fluid_volume
        self.system.setup_fluid(self.nparts)

        fio.read_state(init_conds_file,self.system)
        
        self.system.domain = sph.Domain(dom = fio.load_domain(domain_file))
        
        if self.nparts != self.system.particles.n:
            sys.stderr.write("LOAD ERROR: size of particle system ")
            sys.stderr.write("{} difers from initial condition file {}.\n".format(self.nparts,self.system.particles.n))
            sys.exit("Exit with error.")
        
    ###
    
    def save(self):
        if self.scene_file == None or self.scene_file == "":
            self.scene_file = strftime("%Y-%m-%d_%H.%M.%S",localtime())+'.scn'
        
        fio.save_scene(self)

        sph_params_file = self.scene_file[:-4]+'.prm'
        fio.save_sph_params(sph_params_file,self.system)

        sph_init_file = self.scene_file[:-4]+'.dat'
        fio.save_state(sph_init_file,self.system)
        
        sph_domain_file = self.scene_file[:-4]+'.dom'
        fio.save_domain(sph_domain_file,self.system.domain)
        


    def run(self):
        if self.scene_file == None:
            self.save()
        
        t = self.t_ini
        n=1
        while t < self.t_fin:
            print("n={};  t={}\n".format(n,t+self.t_step))

            t_pre_step = time()
            self.system.solve(self.t_step)
            print("Step computation took "+str(time() - t_pre_step)+'s\n')

            t += self.t_step
            fio.save_step(self.scene_file[:-4],self.system,t,n)
            n+=1

        if t > self.t_fin + self.final_step_tol:
            print("n={};  t={}\n".format(n,self.t_fin))

            t_remain = self.t_step - (t - self.t_fin)

            t_pre_step = time()
            self.system.solve(t_remain)
            print("Step computation took "+str(time() - t_pre_step)+'s\n')

            t = self.t_fin
            fio.save_step(self.scene_file[:-4],self.system,t,n)
        
        print("Simulation end.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SPH fluid simulation")
    
    parser.add_argument('-f',type=str,default="",dest='spath')
    args = parser.parse_args()


    sim = ParticleSimulation()
    if args.spath != "":
        sim.load(args.spath)
    sim.run()
#
