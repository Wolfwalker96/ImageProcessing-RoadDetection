from Provider import ProviderBase
from Algorithm import AlgorithmBase
from Callback import CallbackBase
import cv2


class Frequency:
    HZ1 = 1000
    HZ1000 = 1
    HZ60 = 1000//60
    HZ25 = 1000//25


def apply_road_detection(provider:ProviderBase,
                         algorithm:AlgorithmBase,
                         gui=False,
                         callback:CallbackBase=None,
                         frequency=Frequency.HZ60):
    call = True if callback is not None else False
    print(algorithm.__doc__)
    print(f"Apply on {provider.count} images")
    count = 1
    while provider.has_next:
        input, image_title = provider.next_image
        print(f"{image_title} {count} / {provider.count}", end="\r")
        image, direction = algorithm.detect(input)
        if call:
            callback.image_processed(image, direction, image_title)
        if gui:
            cv2.putText(image, f"{int(count * 100 / provider.count) if provider.count != -1 else 'NaN'}%",
                        (100,400),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA)
            cv2.imshow(f"Image processed", image)
            cv2.waitKey(frequency)
        count += 1
    print()
    if call:
        callback.end()
