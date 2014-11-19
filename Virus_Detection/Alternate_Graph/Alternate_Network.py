__author__ = 'pejakalabhargava'

from igraph import Graph
from scipy import linalg
import numpy as np
import scipy as sc
import random

def readFromFile(file):
    """
    Function which forms igraph graph object by reading
    edgelsit from the input file
    :param file:
    :return:the graph g, number of vertices of g
    """
    with open(file, mode="r") as f:
        vertices, edges = f.readline().split()
        edgeList = list()
        for line in f:
            #add each line to edgelist as (a,b) where a and b are vertex ids
            edgeList.append((int(line.split()[0]), int(line.split()[1])))
    g = Graph(int(vertices))
    g.add_edges(edgeList)
    #makes sure that edges are equal to nubmer specified in file
    assert (int(edges) == len(edgeList))
    return g, int(vertices)


class Alternate_Network:
    """
    This class represents all the functions required to perform various techniques for immunization
    and calculating virus strengths for Time-Varying Networks.
    """
    def __init__(self, fileName1, fileName2, beta=None, delta=None, k=None):
        self.graph1, self.vertices1 = readFromFile(fileName1);
        self.graph2, self.vertices2 = readFromFile(fileName2);
        self.eigenVal = None
        self.beta = beta
        self.delta = delta
        self.k = k


    def calculate_system_matrix(self,beta,delta):
        """
        Calculates the system matrix using two graphs
        :param beta:
        :param delta:
        :return:
        """
        #get the identity matrix equall to legnth of first graph
        I1 = np.identity(len(self.graph1.vs))
        #calculate the value as beta * Adjacency matrix of graph1
        #Note:without converting to np.array it
        # gives error(http://stackoverflow.com/questions/3890621/matrix-and-array-multiplication-in-numpy)
        T1 = beta * np.array(self.graph1.get_adjacency().data)
        #Matrix S calculated as (1-delta) *I + T
        S1 = (1 - delta) * I1 + T1
        #get the identity matrix equal to legnth of second graph
        I2 = np.identity(len(self.graph2.vs))
        #Matrix S calculated as (1-delta) *I + T
        T2 = beta * np.array(self.graph2.get_adjacency().data)
        S2 = (1 - delta) * I2 + T2
        #return the matrix multiplication product of S1 and S2
        return np.dot(S1, S2)


    def calculate_effective_strength(self,beta=None,delta=None):
        """
        calculates the effective strength of the time varying network as determined by the maximum eigen
        value of the system matrix
        :param beta:
        :param delta:
        :return:
        """
        if beta is None:
            beta = self.beta
        if delta is None:
            delta= self.delta
        #get the system matrix
        M = self.calculate_system_matrix(beta=beta,delta=delta)
        #get the numeber of rows which is equal to possible number of eigen values
        rows = M.shape[0]
        #calcaulte the mazimum eigen value
        eigenVal = linalg.eigh(M, eigvals_only=True,eigvals=(rows - 1, rows - 1))
        self.eigenVal = eigenVal[0]
        return self.eigenVal

    def immunize_random_nodes(self, k = None):
        """
        This immunization policy Selects k random nodes for immunization
        param k:
        return:
        """
        if k is None:
            k = self.k
        if self.vertices1 < k:
            print("Cannot immunize")
        #select random nodeIds
        random_node_ids = random.sample(range(self.vertices1), k)
        #print(random_node_ids)
        #print(len(self.graph.vs))
        #delete the nodes from graph1 and graph2
        self.graph1.delete_vertices(random_node_ids)
        self.vertices1 = np.size(self.graph1.vs())
        self.graph2.delete_vertices(random_node_ids)
        self.vertices2 = np.size(self.graph2.vs())


    def immunize_highest_degree_nodes(self, k = None):
        """
        Selects the k nodes with highest degree for immunization
        :param k:
        :return:
        """
        if k is None:
            k = self.k
        node_degrees1 = [self.graph1.degree(i) for i in range(self.vertices1)]
        node_degrees2 = [self.graph2.degree(i) for i in range(self.vertices2)]
        avg_degree = (np.array(node_degrees1)+ np.array(node_degrees2))/2
        #sort it according to the degree and maintain the index of the value which is
        #nothign but the node id
        nodes_ordered_ascending = np.argsort(avg_degree)
        #Selects the k nodes with highest degree for immunization
        top_k_nodes = nodes_ordered_ascending[-k:]
        #delete the nodeIds from both graphs
        self.graph1.delete_vertices(top_k_nodes)
        self.graph2.delete_vertices(top_k_nodes)
        self.vertices1 = np.size(self.graph1.vs())
        self.vertices2 = np.size(self.graph2.vs())


    def immunize_highest_degree_nodes_step_by_step(self, k = None):
        """
        Steps:
        Select the node with the highest degree for immunization.
        Remove this node and its incident edges from the contact network.
        Repeat the same step until all vaccines are administered
        :param k:
        :return:
        """
        if k is None:
            k = self.k
        for i in range(k):
         #call immunize_highest_degree_nodes with node count as 1
         self.immunize_highest_degree_nodes(1)

    def immunize_k_nodes_from_eigen_vector(self, k = None, beta = None, delta = None):
        """
        Steps:
        -Find the eigenvector corresponding to the largest eigenvalue of the time g
         contact network’s adjacency matrix.
        -Find the k largest (absolute) values in the eigenvector.
        -Select the k nodes at the corresponding positions in the eigenvector
        :param k:
        :return:
        """
        if k is None:
            k = self.k
        if beta is None:
            beta = self.beta
        if delta is None:
            delta = self.delta
        #get the system matrix fro graph G1 and G2
        system_matrix = self.calculate_system_matrix(beta,delta)
        #get the maximum eigen value and vector for the system matrix
        eigen_value,eigen_vectors = linalg.eigh(system_matrix,eigvals=(self.vertices1 - 1, self.vertices1 - 1))
        prinicipal_eigen_vector = eigen_vectors[0:]
        prinicipal_eigen_vector = prinicipal_eigen_vector.tolist();
        vector_value = [prinicipal_eigen_vector[i][0] for i in range(self.vertices1)]
        vector_value = list(vector_value)
        #convert vector entries to absoulte value
        x = np.array(vector_value)
        x = np.absolute(x)
        vector_value = x.tolist()
        nodes_ordered_ascending = list(np.argsort(vector_value))
        nodes_to_delete = nodes_ordered_ascending[-k:]
        #delete the k nodes from both graphs
        self.graph1.delete_vertices(nodes_to_delete)
        self.vertices1 = np.size(self.graph1.vs())
        self.graph2.delete_vertices(nodes_to_delete)
        self.vertices2 = np.size(self.graph2.vs())
