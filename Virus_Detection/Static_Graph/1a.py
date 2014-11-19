__author__ = 'pejakalabhargava'
import time

import VirusPropogation as virus

if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network",beta=0.2, delta=0.7,k=100)
    start = time.time()
    print(virus_propogation.getLargestEigenValue())
    end = time.time()
    print("Effective Strength of the virus is " + str(virus_propogation.getEffectiveStrengthOfVirus()))