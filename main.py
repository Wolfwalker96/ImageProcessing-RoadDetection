from Apply import apply_road_detection as detects
from Provider import SequenceProvider
from Callback import AnimateGifCallback
from OtsuBasedDetection import OtsuDetection

def freescale():
    detects(provider=SequenceProvider("../picture_freescale/15.04.16/Avant/Sequence2/"),
            algorithm=OtsuDetection,
            callback=AnimateGifCallback("output"),
            gui=True)

if __name__ == "__main__":
    freescale()
