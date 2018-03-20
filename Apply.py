from Provider import ProviderBase
from Algorithm import AlgorithmBase
from Callback import CallbackBase
import cv2


def apply_road_detection(provider:ProviderBase, algorithm:AlgorithmBase, gui=False, callback:CallbackBase=None):
    call = True if callback is not None else False
    print(algorithm.__doc__)
    print(f"Apply on {provider.count} images")
    count = 1
    while provider.has_next:
        input, filename = provider.next_image
        print(f"{filename} {count} / {provider.count}", end="\r")
        image, direction = algorithm.detect(input)
        if call:
            callback.image_processed(image, direction, filename)
        if gui:
            cv2.putText(image, f"{int(count * 100 / provider.count)}%",
                        (100,400),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA)
            cv2.imshow(f"Image processed", image)
            cv2.waitKey(100)
        count += 1
    print()
    if call:
        callback.end()
