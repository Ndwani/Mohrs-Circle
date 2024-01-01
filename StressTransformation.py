try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    from pip._internal import main as pip
    pip(['install','--user','numpy'])
    pip(['install', '--user', 'matplotlib'])
    import numpy as np
    import matplotlib.pyplot as plt

"""
import numpy as np # aids with arrays and trig functions
import matplotlib.pyplot as plt #module that helps with plotting the mohrs cicle
"""
class StressTransform:
    def __init__(self,Xstress,Ystress,Shear):
        self.__Xstress = Xstress # x direction stress state
        self.__Ystress = Ystress # y direction stress state
        self.__Shear = Shear # shear stress in plane stress element
        self.__AvgStress = (self.__Xstress + self.__Ystress)/2  #average stress
        self.__Diffstress =(self.__Xstress -self.__Ystress)/2  # half the stress difference
    def PrincipleStress(self):  # this method returns the Principle stresses
        PrinSigma1 = np.round(self.__AvgStress + np.sqrt((self.__Diffstress)**2 + (self.__Shear)**2),2)
        PrinSigma2 = np.round(self.__AvgStress - np.sqrt((self.__Diffstress) ** 2 + (self.__Shear) ** 2),2)
        PrincipleStresses = dict() # A dictionary to store key and values of the principle stresses
        PrincipleStresses["SigmaMax"],PrincipleStresses["SigmaMin"] = PrinSigma1,PrinSigma2 # assigning the names SigmaMax and SigmaMin to respective Values


        return PrincipleStresses

    def MaxShear(self):

        return np.round(np.sqrt((self.__Diffstress) ** 2 + (self.__Shear) ** 2),2)  # computes and return the Maximum shear stress


    def StressAtTheta(self,theta):  #calculates the stress state of element at any angle, the method requires an angle as an input
        deg2rad =2*np.round(np.radians(theta),2) # conversion to radians
        theta = deg2rad #Theta in radians
        StressState = dict()
        b = np.round(np.cos(theta),2)
        c = np.round(np.sin(theta),2)

        SigmaX = self.__AvgStress + (self.__Diffstress * b) + (self.__Shear* c) # formula to calculate SigmaX
        SigmaY = self.__AvgStress - (self.__Diffstress * b) - (self.__Shear* c) # formula to calculate SigmaY
        StressState["SigmaX"],StressState["SigmaY"] = SigmaX,SigmaY  # results are stored in StressState Dictionary and assigned to their respective values

        return StressState
    def __Radius(self): # This method calculate the R in the mohr circle or the radius of the circle
        return np.sqrt((self.__Diffstress)**2 + (self.__Shear)**2)
    def __circleCenter(self): # this method simply calculate the average stress or distance of the mohr circle from datum(0,0)
        return self.__AvgStress

    def plot(self):
        radians = np.linspace(0,360,361) * (np.pi/180)
        sigmapts = self.__circleCenter() + self.__Radius()*np.cos(radians)
        taupts = self.__Radius()*np.sin(radians)
        plt.figure(figsize =[5,5])

        plt.plot(sigmapts,taupts)
        plt.title("Mohr's circle")
        plt.xlabel(r"$\sigma$")
        plt.ylabel(r"$\tau$")
        plt.grid()


        ax=plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))

        return plt.show()
