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

        if np.sqrt(r2) > self._h:
            return 0
        
        return self._coef_kern * pow(self._h2 - r2, 3)
            
    # ------




    def gradient(self,x):
        g = np.zeros((3,1))
        r2 = normsquared(x)

        if np.sqrt(r2) > self._h:
            return g

        for i in range(3):
            g[i][0] = - self._coef_grad * x[i] * pow(self._h2 - r2, 2)

        return g #TPA
    # ------



    def laplacian(self,x):
        r2 = normsquared(x)
        
        if np.sqrt(r2) > self._h:
            return 0

        return - self._coef_lapl * (self._h2 - r2) * (3 * self._h2 - 7 * r2)
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
        
        if r > self._h:
            return 0

        return self._coef_kern * pow(self._h - r, 3)
        #
    # ------


    def gradient(self,x):
        g = np.zeros((3,1))
        r = np.linalg.norm(x)
        dist_squared = pow(self._h - r, 2)

        if r > self._h or r == 0:
            return g

        for i in range(3):
            g[i][0] = - self._coef_grad * x[i] / r * dist_squared

        return g
            
    # ------



    def laplacian(self,x):
        r = np.linalg.norm(x);
        
        if r > self._h or r == 0:
            return 0
        
        return - self._coef_lapl * 1 / r *  (self._h - r) * (self._h - 2 * r)
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
        
        if r > self._h or r == 0:
            return 0

        return self._coef_kern * (- pow(r, 3) / (2 * self._h3) + pow(r, 2) / self._h2 + self._h / (2 * r) - 1)
        #
    # ------


    def gradient(self,x):
        g = np.zeros((3,1))
        
        r = np.linalg.norm(x)

        if r > self._h or r == 0:
            return g

        for i in range(3):
            g[i][0] = self._coef_grad * x[i] * (- 3 * r / (2 * self._h3) + 2 / self._h2 - self._h / (2 * pow(r, 3)) )

        return g #TPA
    # ------



    def laplacian(self,x):
        r = np.linalg.norm(x)

        if r > self._h:
            return 0

        return self._coef_lapl * (self._h - r) #TPA
    # ------

####  End of class



