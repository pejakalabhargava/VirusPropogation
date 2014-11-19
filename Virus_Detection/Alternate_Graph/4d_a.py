__author__ = 'pejakalabhargava'
import Alternate_Network as alt
if __name__ == '__main__':
    alternate_Network = alt.Alternate_Network("input/alternating1.network", "input/alternating2.network", beta=0.01, delta=0.60)
    print(alternate_Network.calculate_effective_strength())
