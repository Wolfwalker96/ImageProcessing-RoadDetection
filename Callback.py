class CallbackBase:

    def imageProcessed(self, image, direction):
        pass

    def end(self):
        pass


class AnimateGifCallback(CallbackBase):
    _images = list()

    def __init__(self, output):
        self._output = output
        import os
        if not os.path.exists(output):
            os.mkdir("output")
        if not os.path.exists(os.path.join(output, "animate")):
            os.mkdir(os.path.join(output, "animate"))

    def imageProcessed(self, image, direction, filename):
        import cv2, os, numpy as np
        cv2.imwrite(os.path.join(self._output, f"out_{filename}"), image)
        self._images.append(np.copy(image))

    def end(self):
        import imageio, os, time
        print("Generating Animation")
        imageio.mimsave(os.path.join(self._output, "animate", f"out_{time.strftime('%m_%d_%Y %H.%M.%S')}.gif"), self._images)

