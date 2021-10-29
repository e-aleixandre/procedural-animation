#!/usr/bin/python3
import kernels
import sph


from importlib import reload

reload(kernels)

import numpy as np

from test_data import h, test_vectors
from test_data import std_values, std_grads, std_lapl
from test_data import spiky_values, spiky_grads, spiky_lapl
from test_data import visco_values, visco_grads, visco_lapl

np.set_printoptions(precision=6,suppress=True)

TOL = 1e-8

def test_kernel(name,data,my_data):
    fail = False
    for v,d,md in zip(test_vectors,data,my_data):
        if np.linalg.norm(d-md) > TOL :
            fail = True
            print("   ERROR!")
            print("    ",name,"  v=",v.T)
            print("     ",md,"debería ser")
            print("      ",d)
            print("        ->  err=",d-md,"|",np.linalg.norm(d-md))
    #
    
    if fail:
        print (name,"con error!!\n")
    else:
        print("   ->  Ok!")
    #
#        


std_k = kernels.StandardKernel(h)
spiky_k = kernels.SpikyKernel(h)
visco_k = kernels.ViscosityKernel(h)


my_std_values  = map(std_k.value,test_vectors)
my_std_grads   = map(std_k.gradient,test_vectors)
my_std_lapl    = map(std_k.laplacian,test_vectors)

my_spiky_values = map(spiky_k.value,test_vectors)
my_spiky_grads  = map(spiky_k.gradient,test_vectors)
my_spiky_lapl   = map(spiky_k.laplacian,test_vectors)

my_visco_values = map(visco_k.value,test_vectors)
my_visco_grads  = map(visco_k.gradient,test_vectors)
my_visco_lapl   = map(visco_k.laplacian,test_vectors)


print("Testing standard kernel")
print("------   Value      -------")
test_kernel("std_values",std_values,my_std_values)
print("------   Gradient   -------")
test_kernel("std_grads",std_grads,my_std_grads)
print("------   Laplacian  -------")
test_kernel("std_laplacian",std_lapl,my_std_lapl)


print("\nTesting spiky kernel")
print("------   Value      -------")
test_kernel("spiky_values",spiky_values,my_spiky_values)
print("-------  Gradient   -------")
test_kernel("spiky_grads",spiky_grads,my_spiky_grads)
print("-------  Laplacian  -------")
test_kernel("spiky_laplacian",spiky_lapl,my_spiky_lapl)


print("\nTesting viscosity kernel")
print("------   Value      -------")
test_kernel("visco_values",visco_values,my_visco_values)
print("-------  Gradient   -------")
test_kernel("visco_grads",visco_grads,my_visco_grads)
print("-------  Laplacian  -------")
test_kernel("visco_laplacian",visco_lapl,my_visco_lapl)




""" SPH """

print("\n\n     SPH\n")

fluid = sph.SPHSystem()

fluid.build_fluid(ppedge=3,
                    edge = 1.0,
                    dens = 980,
                    kernel_part = 35,
                    visco = 0.1,
                    surftens = 1.0)


print("""
  ==================================
    PERFORMING STEP WITH dt=0.01
  ==================================""")
fluid.solve(0.01)

print("""
STEP COMPLETE!

  ==================================
    PERFORMING STEP WITH dt=0.01
  ==================================""")
fluid.solve(0.01)
print("\nSTEP COMPLETE!")



