__author__ = 'pejakalabhargava'
import random

import numpy as np

import Alternate_Network as alt


class AlternateSimulatePropogation:
    """
    Simulates the propagation of a virus with the SIS VPM
    beta - transmission probability
    delta - healing probability
    c - a number of initially infected nodes
    t - number of time steps to run the simulation
    """

    def __init__(self, fileName1, fileName2, beta, delta, t,graph1=None,graph2=None):
        if graph1 is None:
            self.graph1, self.vertices1 = alt.readFromFile(fileName1)
        else:
            self.graph1 = graph1
            self.vertices1 = len(self.graph1.vs)
        if graph1 is None:
            self.graph2, self.vertices2 = alt.readFromFile(fileName2)
        else:
            self.graph2 = graph2
            self.vertices2 = len(self.graph2.vs)
        self.beta = beta
        self.delta = delta
        self.c1 = int(self.vertices1 / 10)
        self.c1 = int(self.vertices2 / 10)
        self.t = t

    def simulateInfection(self):
        """
        This method simulates the infection on time varying network .
        The initially infected nodes should be chosen from a random uniform probability distribution.
        At each time step, every susceptible (i.e., non-infected) node has a β probability of being
        infected by neighboring infected nodes, and every infected node has a δ
        probability of healing and becoming susceptible again
        """
        infected_nodes = set()
        infected_nodes = [random.randint(0, self.vertices1 - 1) for p in range(0, self.c1 - 1)]
        # infected_nodes = np.random.choice(self.vertices, self.c, replace = False)
        each_step_nodes_infected = list();
        each_step_nodes_infected.append(len(infected_nodes))
        infected_nodes = set(infected_nodes)
        for time in range(0, self.t):
            #Alternatively switch between graph1 and graph2
            if time%2 == 0:
                cur_graph = self.graph1
            else:
                cur_graph = self.graph2
            new_infected_set = set()
            #For each of the nodes that are infected it is possible
            #that its neighbour can be infected with probability β
            #We also try to cure infected nodes with probability δ
            for node in infected_nodes:
                neighbours = cur_graph.neighbors(node)
                neighbours = set(neighbours).difference(infected_nodes)
                new_nodes_to_be_infected_nodes = set()
                #Iterate through each neighbour node
                for node_id in neighbours:
                    random_no = random.random()
                    if random_no <= self.beta:
                        new_nodes_to_be_infected_nodes.add(node_id)
                new_infected_set = new_infected_set.union(new_nodes_to_be_infected_nodes)
            # time to cure
            new_nodes_to_cure = set()
            for nodeId in infected_nodes:
                random_no = random.random()
                if random_no <= self.delta:
                    new_nodes_to_cure.add(nodeId)
            #add the infected nodes of this step
            infected_nodes = infected_nodes.union(new_infected_set)
            #remove cured nodes
            infected_nodes = infected_nodes.difference(new_nodes_to_cure)
            each_step_nodes_infected.append(len(infected_nodes))
        return each_step_nodes_infected

    def simulateInfectionMultipleTimes(self, run_times=10):
        print("Initial Infected Nodes:" + str(self.c1))
        #Run the experiment as determined br runtimes and store it in a list
        experiment_result = [self.simulateInfection() for run in range(0, run_times)]
        mean_infected = list()
        #Find mean of each of the timeslot t in run_times using np.mean
        for i in range(self.t):
            mean_infected.append(np.mean([experiment_result[j][i] for j in range(run_times)]))
        return mean_infected


