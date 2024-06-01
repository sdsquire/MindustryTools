import Materials as M
import Collectors as C
import Factories as F

if __name__ == '__main__':
    print(F.ImpactReactor() @ F.BlastMixer() @ F.PyratiteMixer() @ F.Cultivator() @ F.CryofluidMixer())