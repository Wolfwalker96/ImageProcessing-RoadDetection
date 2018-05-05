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


class SingleImageProvider(ProviderBase):
    _image = str()
    _has_next = bool()

    def __init__(self, filepath):
        self._image = filepath
        self._has_next = True

    @property
    def count(self):
        return 1

    @property
    def has_next(self):
        ret = self._has_next
        self._has_next = False
        return ret

    @property
    def next_image(self):
        return cv2.imread(self._image), self._image.split("/")[-1]


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


class VideoProvider(ProviderBase):

    def __init__(self,filename):
        from os import path
        self._filename = path.basename(path.normpath(filename))
        self._input = cv2.VideoCapture(filename)
        self._input.set(cv2.CAP_PROP_FPS, 1)
        self._has_next, self._next_frame = self._input.read()
        self._count = int(self._input.get(cv2.CAP_PROP_FRAME_COUNT))
        self._current_frame_number = 0

    @property
    def count(self):
        return self._count

    @property
    def has_next(self):
        return self._has_next

    @property
    def next_image(self):
        self._current_frame_number += 1
        current_frame = self._next_frame
        self._has_next, self._next_frame = self._input.read()
        return current_frame, f"{self._filename}_frame_{self._current_frame_number}"
