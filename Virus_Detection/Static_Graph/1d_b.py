__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot

import VirusPropogation as virus


if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network")
    betaList = [float(x)/10 for x in range(11)]
    virusStrength = [virus_propogation.getEffectiveStrengthOfVirus(beta=val, delta=0.60) for val in betaList]
    print(virusStrength)
    plot.plot(betaList,virusStrength, linestyle="--",color="r")
    plot.ylabel("Effective Virus Strength")
    plot.xlabel("Beta-Transmission probabilities")
    plot.title("Plot for varying Beta with delta=0.60 for static graph")
    minimumBetaForEpidemic = 0.60/virus_propogation.eigenVal;
    plot.axvline(x=minimumBetaForEpidemic, linewidth=2, color="r")
    plot.text(minimumBetaForEpidemic+0.01, 60 ,'Minimum value of beta for epidemic:' +str(minimumBetaForEpidemic),rotation=90)
    print("Minimum value of beta for epidemic is:" + str(minimumBetaForEpidemic))
    plot.show()