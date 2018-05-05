from Apply import apply_road_detection as detects
from Provider import SequenceProvider, VideoProvider, SingleImageProvider
from Callback import SaveImageCallback, TurtleCallback, MultipleCallback
from OtsuBasedDetection import OtsuDetection
from OtsuHullBasedDetection import OtsuHullDetection


def freescale():
    detects(provider=SequenceProvider("../picture_freescale/15.04.16/Avant/Sequence1/"),
            algorithm=OtsuDetection(),
            callback=SaveImageCallback("output"),
            # callback=TurtleCallback(),
            # callback=MultipleCallback(SaveImageCallback("output"), TurtleCallback()),
            gui=True)


def single_image_demo():
    detects(provider=SingleImageProvider("../picture_freescale/15.04.16/Avant/Sequence6/25HEARC.JPG"),
            algorithm=OtsuDetection(),
            callback=SaveImageCallback("output_2"),
            gui=True)


def gta():
    from Apply import Frequency
    detects(provider=VideoProvider("../gta.mp4"),
            algorithm=OtsuHullDetection(inverse=True),
            # callback=TurtleCallback(),
            gui=True,
            frequency=Frequency.HZ1000)


if __name__ == "__main__":
    from sys import argv
    from Provider import ProviderBase
    if len(argv) == 3:
        provider = ProviderBase()
        if argv[1] == "Video":
            provider = VideoProvider(argv[2])
        elif argv[1] == "Sequence":
            provider = SequenceProvider(argv[2])
        elif argv[1] == "Image":
            provider = SingleImageProvider(argv[2])

        detects(provider=provider,
                algorithm=OtsuDetection(),
                callback=SaveImageCallback("output"),
                gui=True)

    else:
        # single_image_demo()
        # freescale()
        # gta()
        print("This command need 2 arguments!")
