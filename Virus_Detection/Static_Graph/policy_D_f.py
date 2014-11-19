__author__ = 'pejakalabhargava'
import matplotlib.pyplot as plot
import numpy as np

import SimulatePropogation as simulation
import VirusPropogation as virus


if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network",beta=0.2, delta=0.7)
    virus_propogation.immunize_k_nodes_from_eigen_vector(k=200)
    sp = simulation.SimulatePropogation("input/static.network",beta=0.20,delta=0.70,t=100, graph=virus_propogation.graph)
    infectedNodeNumber =  sp.simulateInfectionMultipleTimes(run_times=10);
    mean_infected = np.mean(infectedNodeNumber)
    infectedNodeNumber.insert(0,sp.c);
    runs = [i for i in range(0,101)]
    plot.plot(runs,infectedNodeNumber,color="r")
    plot.ylabel("Number Of Infected Nodes")
    plot.xlabel("Experiment Run")
    plot.rcParams.update({'font.size': 12})
    plot.title("Plot for Simultaion of virus Propogation for \n immunized contact network using plolicy D")
    plot.axhline(y=mean_infected, linewidth=1, color="r",ls='dashed')
    plot.text(1, mean_infected+2 ,'Average number of infected Nodes after 10 runs:' +str(mean_infected))
    plot.show()