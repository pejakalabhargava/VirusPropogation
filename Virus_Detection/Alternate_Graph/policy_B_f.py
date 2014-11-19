__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot
import numpy as np

import Alternate_Network as alt
import AlternateSimulatePropogation as simulation

if __name__ == '__main__':
    alternate_Network = alt.Alternate_Network("input/alternating1.network", "input/alternating2.network", beta=0.2, delta=0.7)
    alternate_Network.immunize_highest_degree_nodes(k=200)
    sp = simulation.AlternateSimulatePropogation(fileName1=None,fileName2 = None,beta=0.20,delta=0.70,t=100,graph1 = alternate_Network.graph1, graph2 = alternate_Network.graph2)
    infectedNodeNumber =  sp.simulateInfectionMultipleTimes(run_times=10);
    mean_infected = np.mean(infectedNodeNumber)
    infectedNodeNumber.insert(0,sp.c1);
    runs = [i for i in range(0,101)]
    plot.plot(runs,infectedNodeNumber,color="r")
    plot.ylabel("Number Of Infected Nodes")
    plot.xlabel("Experiment Run")
    plot.rcParams.update({'font.size': 12})
    plot.title("Plot for Simultaion of virus Propogation for \n alternate immunized contact network using plolicy B")
    plot.axhline(y=mean_infected, linewidth=1, color="r",ls='dashed')
    plot.text(1, mean_infected+10 ,'Average number of infected Nodes after 10 runs:' +str(mean_infected))
    plot.show()