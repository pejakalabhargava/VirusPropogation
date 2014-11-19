__author__ = 'pejakalabhargava'
import VirusPropogation as virus

"""
Transmission probabilities β1 = 0.20 and β2 = 0.01
Healing probabilities δ1 =0.70 and δ2 = 0.60
Number of available vaccines k1 = 200
"""
if __name__ == '__main__':
    virus_propogation = virus.VirusPropogation("input/static.network",beta=0.2, delta=0.7,k=200)
    print("Effective Strength of the virus before immunization is " + str(virus_propogation.getEffectiveStrengthOfVirus()))
    virus_propogation.immunize_highest_degree_nodes_step_by_step(k=200);
    print("Effective Strength of the virus is after immunization " + str(virus_propogation.getEffectiveStrengthOfVirus()))