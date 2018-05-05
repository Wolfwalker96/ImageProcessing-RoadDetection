from Algorithm import AlgorithmBase
import cv2, numpy as np


class OtsuHullDetection(AlgorithmBase):
    """
    Road detection based on Otsu.
    """
    def __init__(self,inverse=False):
        self._inverse = inverse
        self._last_ratios = list()

    def detect(self, img_i):
        img = cv2.cvtColor(img_i, cv2.COLOR_BGR2GRAY)

        if self._inverse:
            img = cv2.bitwise_not(img)

        ret, img = cv2.threshold(img, 100, 255.0, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


        # Open
        iterations = 5  # Find Best Value
        kernel_square_side = 6  # Find Best Value
        kernel = np.ones((kernel_square_side, kernel_square_side), np.uint8)
        img = cv2.erode(img, kernel, iterations=iterations)
        img = cv2.dilate(img, kernel, iterations=iterations)

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

        contour = bottom_contours[0] if len(bottom_contours)>0 else contours[0]
        for c in bottom_contours:
            if cv2.contourArea(c) == max_rarea:
                contour = c

        # overlay = img_i.copy()
        # # (2) draw shapes:
        # cv2.drawContours(overlay, [contour], -1, (0, 255, 0), -1)
        # # (3) blend with the original:
        # opacity = 0.4
        # cv2.addWeighted(overlay, opacity, img_i, 1 - opacity, 0, img_i)

        hull = cv2.convexHull(contour)

        height, width = img.shape


        img = np.zeros((height, width), np.uint8)

        cv2.drawContours(img, [hull], -1, (255, 255, 255), -1)

        left_side = list()
        right_side = list()

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

        contour = bottom_contours[0] if len(bottom_contours)>0 else contours[0]
        for c in bottom_contours:
            if cv2.contourArea(c) == max_rarea:
                contour = c

        for i, point in enumerate(contour[1:-2]):
            current_point = point[0]
            before_point = contour[i-1][0]
            after_point = contour[i+1][0]
            derivation = (after_point[1] - before_point[1])/(after_point[0] - before_point[0])
            if derivation < 0:
                right_side.append(current_point)
            elif derivation > 0:
                left_side.append(current_point)

        # cv2.drawContours(img_i, [contour], -1, (255, 255, 255), -1)

        for point in left_side:
            cv2.circle(img_i, tuple(point), 5, (255, 0, 0))
        for point in right_side:
            cv2.circle(img_i, tuple(point), 5, (0, 0, 255))

        left_ratio = len(left_side) / (len(right_side) + len(left_side))

        # self._last_ratios.append(left_ratio)
        # from statistics import median
        #
        # NB_MEDIAN = 1
        # if len(self._last_ratios) > NB_MEDIAN:
        #     left_ratio = median(self._last_ratios[-NB_MEDIAN:])

        right_ratio = 1 - left_ratio

        return img_i, (-1*left_ratio) + right_ratio
        # return cv2.drawContours(img_i, [contour], -1, (0, 255, 0), 3), ()
