"""SPH Smoothing Kernels"""

import numpy as np

dist_tolerance = 1.0e-9

def normsquared(x):
    return x[0]*x[0] + x[1]*x[1] + x[2]*x[2]
#

class StandardKernel:
    """ Standard order 6 polynomial Kernel.

    Proposed in Muller et al. 2003
    """

    def __init__(self,smoothlength):
        self.setSmoothingLength(smoothlength)
    # ------


    def setSmoothingLength(self,h):
        self._h = h
        self._h2 = self._h*self._h
        self._h9 = self._h**9
        self._coef_kern = 315/(64*np.pi*self._h9)
        self._coef_grad = 945/(32*np.pi*self._h9)
        self._coef_lapl = 945/(32*np.pi*self._h9)
    # ------
        

    def value(self,x):
        r2 = normsquared(x)
        # TODO: complete the kernel!
        return r2 #TPA
        #
    # ------




    def gradient(self,x):
        g = np.zeros((3,1))
        # TODO: complete the kernel!
        return g #TPA
    # ------



    def laplacian(self,x):
        r2 = normsquared(x)
        # TODO: complete the kernel!
        return r2 #TPA
        #
    # ------


class SpikyKernel:
    """ Spiky Kernel for pressure computation.
        Proposed in Muller et al. 2003
    """
    
    def __init__(self,smoothlength):
        self.setSmoothingLength(smoothlength)
    # ------


    def setSmoothingLength(self,h):
        self._h = h
        self._h2 = self._h*self._h
        self._h6 = self._h**6
        self._coef_kern = 15/(np.pi*self._h6)
        self._coef_grad = 45/(np.pi*self._h6)
        self._coef_lapl = 90/(np.pi*self._h6)
    # ------
        


    def value(self,x):
        r = np.linalg.norm(x)
        # TODO: complete the kernel!
        return r #TPA
        #
    # ------


    def gradient(self,x):
        g = np.zeros((3,1))
        # TODO: complete the kernel!
        return g #TPA
    # ------



    def laplacian(self,x):
        r = np.linalg.norm(x);
        # TODO: complete the kernel!
        return r #TPA
    # ------

####  End of class


class ViscosityKernel:
    """ Viscosity Kernel for viscosity computation.
        Proposed in Muller et al. 2003
    """
    
    def __init__(self,smoothlength):
        self.setSmoothingLength(smoothlength)
    # ------


    def setSmoothingLength(self,h):
        self._h = h
        self._h2 = self._h**2
        self._h3 = self._h**3
        self._h6 = self._h**6
        self._coef_kern = 15/(2*np.pi*self._h3)
        self._coef_grad = 15/(2*np.pi*self._h3)
        self._coef_lapl = 45/(  np.pi*self._h6)
    # ------
        


    def value(self,x):
        r = np.linalg.norm(x)
        # TODO: complete the kernel!
        return r #TPA
        #
    # ------


    def gradient(self,x):
        g = np.zeros((3,1))
        # TODO: complete the kernel!
        return g #TPA
    # ------



    def laplacian(self,x):
        r = np.linalg.norm(x);
        # TODO: complete the kernel!
        return r #TPA
    # ------

####  End of class



