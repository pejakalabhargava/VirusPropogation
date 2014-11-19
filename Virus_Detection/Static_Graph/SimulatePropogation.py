__author__ = 'pejakalabhargava'
import random

import numpy as np

import VirusPropogation as virus


class SimulatePropogation:
    """
    Simulates the propagation of a virus with the SIS virus propogation model
    beta - transmission probability
    delta - healing probability
    c - a number of initially infected nodes
    t - number of time steps to run the simulation
    """

    def __init__(self, fileName, beta, delta, t, c=10,graph = None):
        """
        This constructor creates an instance of this program for simutaion
        This can take either the filename or the actual insatcne of igraph
        itself on which it performs the simulation.
        """
        if graph is None:
            self.graph, self.vertices = virus.readFromFile(fileName)
        else:
            self.graph = graph
            self.vertices = len(self.graph.vs)
        self.beta = beta
        self.delta = delta
        self.c = c
        self.c = int(self.vertices / 10)
        self.t = t

    def simulateInfection(self):
        """
        This methid simulates the infection on a graph.The initially infected nodes should be
        chosen from a random uniform probability distribution. At each time step,
        every susceptible (i.e., non-infected) node has a β probability of being
        infected by neighboring infected nodes, and every infected node has a δ
        probability of healing and becoming susceptible again
        """
        infected_nodes = set()
        #select random initial nodes determined by factor c
        infected_nodes = [random.randint(0, self.vertices - 1) for p in range(0, self.c - 1)]
        each_step_nodes_infected =list();
        #add the number of infected nodes to a list
        each_step_nodes_infected.append(len(infected_nodes))
        #create a set to hold all infected nodes at time t
        infected_nodes = set(infected_nodes)
        #run the simultion for time t
        for time in range(0, self.t):
            new_infected_set = set()
            #For each of the nodes that are infected it is possible
            #that its neighbour can be infected with probability β
            #We also try to cure infected nodes with probability δ
            for node in infected_nodes:
                #get neighbours of the node as vertexIds
                neighbours = self.graph.neighbors(node)
                #remove the nodes that are already infected
                neighbours = set(neighbours).difference(infected_nodes)
                new_nodes_to_be_infected_nodes = set()
                #Iterate through each neighbour node
                for node_id in neighbours:
                    #generate a random number between o.o and 1.0
                    random_no = random.random()
                    #if random number is less than beta then infect the neighbour node
                    if random_no <= self.beta:
                        new_nodes_to_be_infected_nodes.add(node_id)
                #Add it to the set
                new_infected_set = new_infected_set.union(new_nodes_to_be_infected_nodes)
            #time to cure
            new_nodes_to_cure = set()
            #cure the infected nodes with probability delta
            for nodeId in infected_nodes:
                random_no = random.random()
                if random_no <= self.delta:
                    new_nodes_to_cure.add(nodeId)
            #add the infected nodes of this step
            infected_nodes = infected_nodes.union(new_infected_set)
            #remove cured nodes
            infected_nodes = infected_nodes.difference(new_nodes_to_cure)
            #add the number of nodes still infected to the list
            each_step_nodes_infected.append(len(infected_nodes))
        return each_step_nodes_infected

    def simulateInfectionApproach2(self):
        """
        Different Approach to simulate the virus propogation. Wrote this to see the difference between approaches
        """
        infected_nodes = set()
        infected_nodes = [random.randint(0, self.vertices - 1) for p in range(0, self.c - 1)]
        # infected_nodes = np.random.choice(self.vertices, self.c, replace = False)
        infected_nodes = set(infected_nodes)
        for time in range(0, self.t):
            new_infected_set = set()
            for node in infected_nodes:
                neighbours = self.graph.neighbors(node)
                neighbours = set(neighbours).difference(infected_nodes)
                new_nodes_to_be_infected_nodes = random.sample(neighbours, int(len(neighbours) * self.beta))
                new_infected_set = new_infected_set.union(set(new_nodes_to_be_infected_nodes))
            #time to cure
            new_nodes_to_cure = random.sample(infected_nodes, int(len(infected_nodes) * self.delta))
            infected_nodes = infected_nodes.union(new_infected_set)
            #remove cured nodes
            infected_nodes = infected_nodes.difference(set(new_nodes_to_cure))
        return len(infected_nodes)

    def simulateInfectionMultipleTimes(self, run_times=10):
        print("Initial Infected Nodes:" + str(self.c))
        #Run the experiment as determined br runtimes and store it in a list
        experiment_result = [self.simulateInfection() for run in range(0, run_times)]
        mean_infected = list()
        #Find mean of each of the timeslot t in run_times using np.mean
        for i in range(self.t):
            mean_infected.append(np.mean([experiment_result[j][i] for j in range(run_times)]))
        return mean_infected

