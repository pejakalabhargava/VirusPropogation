__author__ = 'pejakalabhargava'
import Alternate_Network as alt

"""
Transmission probabilities β1 = 0.20 and β2 = 0.01
Healing probabilities δ1 =0.70 and δ2 = 0.60
Number of available vaccines k1 = 200
"""
if __name__ == '__main__':
    alternate_Network = alt.Alternate_Network("input/alternating1.network", "input/alternating2.network", beta=0.2, delta=0.7)
    print("Effective Strength of the virus before immunization is " + str(alternate_Network.calculate_effective_strength()))
    alternate_Network.immunize_highest_degree_nodes(k=200);
    print("Effective Strength of the virus is after immunization " + str(alternate_Network.calculate_effective_strength()))