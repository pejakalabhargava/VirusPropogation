__author__ = 'pejakalabhargava'
import time

import VirusPropogation as virus

if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network")
    start = time.time()
    print(virus_propogation.getLargestEigenValue())
    end = time.time()
    print("Effective Strength of the virus is " + str(virus_propogation.getEffectiveStrengthOfVirus(beta=0.01, delta=0.60)))
