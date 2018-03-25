from Apply import apply_road_detection as detects
from Provider import SequenceProvider, VideoProvider
from Callback import SaveImageCallback
from OtsuBasedDetection import OtsuDetection


def freescale():
    detects(provider=SequenceProvider("../picture_freescale/15.04.16/Avant/Sequence6/"),
            algorithm=OtsuDetection(),
            callback=SaveImageCallback("output"),
            gui=True)


def gta():
    from Apply import Frequency
    detects(provider=VideoProvider("../gta.mp4"),
            algorithm=OtsuDetection(inverse=True),
            callback=SaveImageCallback("GTA_output"),
            gui=True,
            frequency=Frequency.HZ1000)


if __name__ == "__main__":
    freescale()
    # gta()
