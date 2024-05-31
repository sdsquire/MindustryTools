import Materials as M
import Collectors as C
import Factories as F

if __name__ == '__main__':
    print(F.PlastaniumCompressor())
    print(F.CryofluidMixer())
    print(F.PlastaniumCompressor() + F.CryofluidMixer())