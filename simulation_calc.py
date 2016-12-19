import matplotlib
matplotlib.use("Gtk3agg")
import matplotlib.backends
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math

class OneD_simulate:
    def __init__(self):
        self.__fig,self.__ax=plt.subplots()
        self.__line, = self.__ax.plot([],[])

    def simulate(self,hbar, mass, L, numPoints, x, numBasis, wf, time):
        '''(OneD_animate, float,float,float, int, np.ndarray int, str, float) -> none
        Function that simulates a 1-D wavefunction wf, whether it is an eigenstates 
        or linear combination of eigenstates of particle in a box
        '''
        
        #System parameters
        #L= Max - Min
        # x = np.linspace(0,L,numPoints)
        dx =x[1]-x[0]    
        
        num_vec = np.arange(1,numBasis+1)
        num_vec = num_vec.T
        #print(num_vec)
    
        # basis functions   
        # np.outer(a,b) does the  nx1 and 1xm matrix multiplication
        psix = math.sqrt(2/L)* np.sin((np.pi/L)*np.outer(num_vec,x))
    
        #normalizing wf
        w = create_weights(numPoints,dx)
        wf = normalize(wf,w)
    
        #finding coefficients
        cn = psix.dot(wf*w)
    
        #energies
        En_vec = (num_vec**2)*((np.pi*hbar)**2/(2*mass*L))
        
        #animate
        #setting axes
        plt.xlim((0,L))
        plt.ylim((-1,1))
        
        # initial function
        def init():
            self.__line.set_data([],[])
            return self.__line,
        
        def animate(i):
            ht_real = cn *np.cos((En_vec/hbar)*i)
            wf_real  = ht_real.dot(psix)
            self.__line.set_data(x, wf_real)
            return self.__line,

        self.ani= animation.FuncAnimation(self.__fig, animate, init_func=init,frames=200, interval=20, blit=True,repeat=False)    
        plt.show() 
        return self.ani

def normalize(gx, weights):
    '''(np.ndarray, np.ndarray)-> np.ndarray
    Normalizes function gx
    '''
    trans_gx = gx.conj().T
    A_sqr_inv = np.dot(gx*weights, trans_gx)
    A = 1/np.sqrt(A_sqr_inv)
    gx = A*gx
    return gx

def create_weights(numPoints,dx):
    '''(int)-> np.ndarray
    Creating a 1xnumPoints array of the weights for trapezoidal rule
    '''
    weights =np.ones(numPoints)
    weights[0] = 0.5
    weights[numPoints-1]=0.5
    weights = dx*weights
    return weights