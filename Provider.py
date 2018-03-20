import cv2

class ProviderBase:
    @property
    def count(self):
        pass

    @property
    def has_next(self):
        pass

    @property
    def next_image(self):
        pass


class SequenceProvider(ProviderBase):
    _images = list()

    def __init__(self, folder):
        import os, re
        self._input = folder
        self._images = list([file for file in os.listdir(folder) if file.endswith(".JPG")])
        self._images.sort(key=lambda x: int(re.findall("\d+",x)[0]))
        self._count = len(self._images)

    @property
    def count(self):
        return self._count

    @property
    def has_next(self):
        return len(self._images) != 0

    @property
    def next_image(self):
        import os
        filename = self._images.pop(0)
        return cv2.imread(os.path.join(self._input,filename)), filename
