
__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot

import VirusPropogation as virus


if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network")
    deltaList = [float(x)/10 for x in range(11)]
    virusStrength = [virus_propogation.getEffectiveStrengthOfVirus(beta=0.20, delta=val) for val in deltaList]
    print(virusStrength)
    plot.plot(deltaList,virusStrength, linestyle="--",color="r")
    plot.ylabel("Effective Virus Strength")
    plot.xlabel("Healing probabilities")
    plot.title("Plot for varying Delta with beta=0.20 for static graph")
    maximumDeltaForEpidemic = virus_propogation.eigenVal * 0.20;
    #plot.axvline(x=minimumDeltaForEpidemic, linewidth=2, color="r")
    #plot.text(minimumDeltaForEpidemic+0.01, 60 ,'Maximum value of delta for epidemic:' +str(minimumDeltaForEpidemic),rotation=90)
    print("Maximum value of delta for epidemic is:" + str(maximumDeltaForEpidemic))
    plot.show()