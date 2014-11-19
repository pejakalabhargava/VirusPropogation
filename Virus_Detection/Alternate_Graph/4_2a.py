__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot
import numpy as np

import AlternateSimulatePropogation as simulation
if __name__ == '__main__':
    sp = simulation.AlternateSimulatePropogation(fileName1 = "input/alternating1.network", fileName2 = "input/alternating2.network",beta=0.20,delta=0.70,t=100)
    infectedNodeNumber =  sp.simulateInfectionMultipleTimes(run_times=10);
    infectedNodeNumber.insert(0,sp.c1);
    runs = [i for i in range(0,101)]
    plot.plot(runs,infectedNodeNumber,color="r")
    plot.ylabel("Number Of Infected Nodes")
    plot.xlabel("Experiment Run")
    plot.title("Plot for Simultaion of virus Propogation for beta=0.20 and delta=0.70")
    mean_infected = np.mean(infectedNodeNumber)
    plot.axhline(y=mean_infected, linewidth=2, color="r")
    plot.text(1, mean_infected+0.1 ,'Average number of infected Nodes after 10 runs:' +str(mean_infected))
    plot.show()