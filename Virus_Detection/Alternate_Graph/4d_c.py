
__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot
import Alternate_Network as alt


if __name__ == '__main__':
    alternate_Network = alt.Alternate_Network("input/alternating1.network", "input/alternating2.network",  beta=0.01, delta=0.60)
    deltaList = [float(x)/10 for x in range(6)]
    virusStrength = [alternate_Network.calculate_effective_strength(beta=0.01, delta=val) for val in deltaList]
    print(virusStrength)
    plot.plot(deltaList,virusStrength, linestyle="--",color="r")
    plot.ylabel("Effective Virus Strength")
    plot.xlabel("Healing probabilities")
    plot.title("Plot for varying Delta with beta=0.01 for Alternating graph")
    #plot.axvline(x=minimumDeltaForEpidemic, linewidth=2, color="r")
    #plot.text(minimumDeltaForEpidemic+0.01, 60 ,'Maximum value of delta for epidemic:' +str(minimumDeltaForEpidemic),rotation=90)
    plot.show()