from Algorithm import AlgorithmBase
import cv2, numpy as np


class OtsuDetection(AlgorithmBase):
    """
    Road detection based on Otsu.
    """
    def __init__(self,inverse=False):
        self._inverse = inverse

    def detect(self, img_i):
        img = cv2.cvtColor(img_i, cv2.COLOR_BGR2GRAY)

        if self._inverse:
            img = cv2.bitwise_not(img)

        trash, img = cv2.threshold(img, 100, 255.0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Open
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.erode(img, kernel, iterations=3)
        img = cv2.dilate(img, kernel, iterations=3)

        # Contour detection
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Contours that touch the bottom
        height, width = img.shape[:2]
        height -= 5  # ptit marge
        bottom_contours = []
        for c in contours:
            for val in c:
                if val[0].item(1) >= height:
                    bottom_contours.append(c)
                    break

        # biggest area
        r_areas = [cv2.contourArea(c) for c in contours]
        max_rarea = np.max(r_areas)

        contour = bottom_contours[0]
        for c in bottom_contours:
            if cv2.contourArea(c) == max_rarea:
                contour = c

        return cv2.drawContours(img_i, [contour], -1, (0, 255, 0), 3), 0
