from Algorithm import AlgorithmBase
import cv2, numpy as np


class OtsuDetection(AlgorithmBase):
    """
    Road detection based on Otsu.
    """
    @staticmethod
    def detect(img_i):
        img = cv2.cvtColor(img_i, cv2.COLOR_BGR2GRAY)

        trash, img = cv2.threshold(img, 100, 255.0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Open
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.erode(img, kernel, iterations=3)
        img = cv2.dilate(img, kernel, iterations=3)

        # Contour detection
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return cv2.drawContours(img_i, contours, -1, (0, 255, 0), 3), 0
