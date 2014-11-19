__author__ = 'pejakalabhargava'
from igraph import Graph
from scipy import linalg
import numpy as np
import scipy as sc
import  random

def readFromFile(file):
    """
    Function which forms igraph graph object by reading
    edgelsit from the input file
    :param file:
    :return:the graph g, number of vertices of g
    """
    with open(file, mode="r") as f:
        #read first line
        vertices, edges = f.readline().split()
        edgeList = list()
        #add each line to edgelist as (a,b) where a and b are vertex ids
        for line in f:
            edgeList.append((int(line.split()[0]), int(line.split()[1])))
    #create a new graph
    g = Graph(int(vertices))
    #add the edges to the graph
    g.add_edges(edgeList)
    #makes sure that edges are equal to nubmer specified in file
    assert (int(edges) == len(edgeList))
    return g, int(vertices)


class VirusPropogation:
    """
    This class represents all the functions required to perform various techniques for immunization
    and calcualting virus strengths for a static graph.
    """
    def __init__(self, fileName, beta=None, delta=None, immunization_policy=None, k = None):
        """
        Constructor to create an instance
        :param fileName:
        :param beta:
        :param delta:
        :param immunization_policy:
        :param k:
        """
        self.graph, self.vertices = readFromFile(fileName)
        self.eigenVal = None
        self.immunization_policy = immunization_policy
        self.beta = beta
        self.delta = delta
        self.k = k

    def resetGraph(self,g, calculateEigen = None):
        """
        Used to point the grpah to a new instance of igraph.
        This also makes sure new maximum eigen value is
        calulcated for the graph.
        :param g:
        :param calculateEigen:
        :return:
        """
        self.graph = g
        self.vertices = len(self.graph.vs)
        if calculateEigen is True:
            self.calculateLargestEigenValue()

    def getLargestEigenValue(self):
        """
        Calculates largest eigen value for a graph
        :return:
        """
        if self.eigenVal is None:
          self.calculateLargestEigenValue()
        return self.eigenVal

    def calculateLargestEigenValue(self):
        """
        This method calculates the largest eigen value for the grpah instance
        of the class
        :return:
        """
        print("Calculating Eigen Values")
        #the first parameter is the graph itself, setting eigvals_only to True ensures thaat
        #only eigen values are calculated. eigVals repesents the range of eigen values to be
        #calculated.Since we need the largest eigen value this value is equal to the
        #maximum possible vertex id
        eigenVal = linalg.eigh(self.graph.get_adjacency().data, eigvals_only=True,
                                        eigvals=(self.vertices - 1, self.vertices - 1))
        #retuen the first object since it points to eigen value. Second parameter
        #is eigen vector
        self.eigenVal = eigenVal[0]
        return self.eigenVal

    def getEffectiveStrengthOfVirus(self, beta=None, delta=None):
        """
        calcualates the effective virus strength for static graphs using the
        formula maxEigenVal * β / δ
        :param beta:
        :param delta:
        :return:
        """
        if beta is None:
            beta = self.beta
        if delta is None:
            delta= self.delta
        #make sure to consider absolute value of maxiumu eigen value
        highestEigenValue = abs(self.getLargestEigenValue())
        return (highestEigenValue * beta/delta)

    def immunize_random_nodes(self, k = None):
        """
        This immunization policy Selects k random nodes for immunization
        param k:
        return:
        """
        if k is None:
            k = self.k
        if self.vertices < k:
            print("Cannot immunize")
        #get random node Ids
        random_node_ids = random.sample(range(self.vertices), k)
        #print(random_node_ids)
        #print(len(self.graph.vs))
        #delete the vertices
        self.graph.delete_vertices(random_node_ids)
        #update the graph related data strucutres
        self.vertices = np.size(self.graph.vs())
        self.calculateLargestEigenValue()
        #print(len(self.graph.vs))

    def immunize_highest_degree_nodes(self, k = None):
        """
        Selects the k nodes with highest degree for immunization
        :param k:
        :return:
        """
        if k is None:
            k = self.k
        #get degree of each node in the graph
        node_degrees = [self.graph.degree(i) for i in range(self.vertices)]
        #sort it according to the degree and maintain the index of the value which is
        #nothign but the node id
        nodes_ordered_ascending = np.argsort(node_degrees)
        #retrieve top k nodeIds
        top_k_nodes = nodes_ordered_ascending[-k:]
        #print(len(self.graph.vs))
        #print(top_k_nodes)
        #delete the Nodes
        self.graph.delete_vertices(top_k_nodes)
        self.vertices = np.size(self.graph.vs())
        self.calculateLargestEigenValue()
        #print(len(self.graph.vs))

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
            #node_to_remove = self.graph.maxdegree()
            #get the current length of graph
            current_len = np.size(self.graph.vs())
            #get degree of each node
            node_degrees = [self.graph.degree(count) for count in range(current_len)]
            #sort and get indecies for those nodes
            nodes_ordered_ascending = np.argsort(node_degrees)
            #get node with highrst degree
            node_to_remove = nodes_ordered_ascending[current_len-1]
            #print(node_to_remove)
            #remove the node
            self.graph.delete_vertices(node_to_remove)
        self.vertices = np.size(self.graph.vs())
        self.calculateLargestEigenValue()

    def immunize_k_nodes_from_eigen_vector(self, k = None):
        """
        Steps:
        -Find the eigenvector corresponding to the largest eigenvalue of the contact network’s adjacency matrix.
        -Find the k largest (absolute) values in the eigenvector.
        -Select the k nodes at the corresponding positions in the eigenvector
        :param k:
        :return:
        """
        if k is None:
            k = self.k
        #get the maximum eigen value and vector fro the graph
        eigen_value,eigen_vectors = linalg.eigh(self.graph.get_adjacency().data,
                                              eigvals=(self.vertices - 1, self.vertices - 1))
        #get the maximum eigen vector
        prinicipal_eigen_vector = eigen_vectors[0:]
        prinicipal_eigen_vector = prinicipal_eigen_vector.tolist();
        #Get the entries in the vector
        vector_value = [prinicipal_eigen_vector[i][0] for i in range(self.vertices)]
        vector_value = list(vector_value)
        #convert vector entries to absoulte value
        x = np.array(vector_value)
        x = np.absolute(x)
        vector_value = x.tolist()
        #sort the vector values based on its value
        nodes_ordered_ascending = list(np.argsort(vector_value))
        #get k maximum nodes from it
        nodes_to_delete = nodes_ordered_ascending[-k:]
        #delete the k nodes
        self.graph.delete_vertices(nodes_to_delete)
        self.vertices = np.size(self.graph.vs())
        self.calculateLargestEigenValue()