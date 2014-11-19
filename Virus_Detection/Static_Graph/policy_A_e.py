__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot

import VirusPropogation as virus

"""
Transmission probabilities β1 = 0.20 and β2 = 0.01
Healing probabilities δ1 =0.70 and δ2 = 0.60
Number of available vaccines k1 = 200
"""
if __name__ == '__main__':
    virusStrength = list()
    runs = [x for x in range(2000,5715,200)]
    for x in runs:
        virus_propogation = virus.VirusPropogation("input/static.network",beta=0.2, delta=0.7)
        virus_propogation.immunize_random_nodes(k=x)
        vs = virus_propogation.getEffectiveStrengthOfVirus()
        if vs<=1:
            print("value of k for contain network is:" + str(x))
        virusStrength.append(vs)

    print(virusStrength)
    plot.plot(runs,virusStrength, linestyle="--",color="r")
    plot.ylabel("Effective Virus Strength")
    plot.xlabel("Number of Immunized Nodes")
    plot.title("Plot for Policy A of virus Propogation")
    plot.axhline(y=1, linewidth=2, color="r")
    plot.text(2000, 1+0.1 ,'Threshold for network being epidemic')
    plot.show()