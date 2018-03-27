from Algorithm import AlgorithmBase
import cv2, numpy as np


class PaulOtsuDetection(AlgorithmBase):
    """
    Road detection based on Otsu.
    """
    def __init__(self,inverse=False):
        self._inverse = inverse

    def _add_side_line(self, img, points, color=(255, 0, 0)):
        [vx, vy, x, y] = cv2.fitLine(np.array(points), cv2.DIST_L2, 0, 0.01, 0.01)

        # Now find two extreme points on the line to draw line
        lefty = int((-x * vy / vx) + y)
        righty = int(((img.shape[1] - x) * vy / vx) + y)

        # Finally draw the line
        try:
            cv2.line(img, (img.shape[1] - 1, righty), (0, lefty), color, 2)
        except Exception:
            pass

    def _get_left_right_derivation_method(self,img_i,contour):
        right = list()
        left = list()
        derivations = list()
        for i, current in list(enumerate(contour))[1:-2]:
            point_before = contour[i-1][0]
            point_current = current[0]
            point_after = contour[i+1][0]
            derivation = (point_after[1] - point_before[1]) / (point_after[0] - point_before[0])
            derivations.append(derivation)
            print(derivation)
            if derivation < 0:
                cv2.circle(img_i, tuple(point_current), 5, (255, 0, 0))
                right.append(point_current)
            elif derivation > 0:
                cv2.circle(img_i, tuple(point_current), 5, (0, 0, 255))
                left.append(point_current)
        return left, right

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

        parts = list()
        index = 0
        parts.append(list())
        previous_derivation = 0
        for i, point in enumerate(contour[1:-2]):
            previous_point = contour[i-1][0]
            next_point = contour[i+1][0]
            derivation = (next_point[1] - previous_point[1]) / (next_point[0] - previous_point[0])
            if point[0][1] == 0 or point[0][0] == 0 or point [0][1] == height or point[0][0] == width:
                index += 1
                parts.append(list())
            elif derivation-previous_derivation > 10:
                index += 1
                parts.append(list())
            else:
                parts[index].append(point[0])
            previous_derivation = derivation

        parts = sorted(parts, key=lambda part: len(part), reverse=True)
        for i, part in enumerate(parts):
            from random import randint
            random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            if len(part) > 0:
                for point in part:
                    cv2.circle(img_i, tuple(point), 5, random_color)
                self._add_side_line(img_i, part, color=random_color)
            print(i)
            if i >= 1:
                break

        # left, right = self._get_left_right_derivation_method(img_i, contour)
        # self._add_side_line(img_i, left, color=(125,125,0))
        # self._add_side_line(img_i, right, color=(0,125,125))
        return img_i, 0
        return cv2.drawContours(img_i, [contour], -1, (0, 255, 0), 3), 0
