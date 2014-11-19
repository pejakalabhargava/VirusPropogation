__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot

import Alternate_Network as alt

if __name__ == '__main__':
    alternate_Network = alt.Alternate_Network("input/alternating1.network", "input/alternating2.network", beta=0.01, delta=0.60)
    betaList = [float(x+1)/10 for x in range(6)]
    virusStrength = [alternate_Network.calculate_effective_strength(beta=val, delta=0.60) for val in betaList]
    print(virusStrength)
    plot.plot(betaList,virusStrength, linestyle="--",color="r")
    plot.ylabel("Effective Virus Strength")
    plot.xlabel("Beta-Transmission probabilities")
    plot.title("Plot for varying Beta with delta=0.6 for Alternating graph")
    #plot.axvline(x=minimumBetaForEpidemic, linewidth=2, color="r")
    #plot.text(minimumBetaForEpidemic+0.01, 60 ,'Minimum value of beta for epidemic:' +str(minimumBetaForEpidemic),rotation=90)
    #print("Minimum value of beta for epidemic is:" + str(minimumBetaForEpidemic))
    plot.show()