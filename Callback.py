class CallbackBase:

    def image_processed(self, image, direction, filename):
        """
        Executed for each images
        :param image: The image
        :param direction: The road direction
        :param filename: The image filename
        :return: Nothings
        """
        pass

    def end(self):
        """
        Executed when they are not image left
        :return: Nothing
        """
        pass


class SaveImageCallback(CallbackBase):
    """
    Build an animate gif.
    """

    def __init__(self, output, animate=True):
        self._images = list()
        self._output = output
        self._animate=animate
        import os
        if not os.path.exists(output):
            os.mkdir(output)
        if not os.path.exists(os.path.join(output, "animate")):
            os.mkdir(os.path.join(output, "animate"))

    def image_processed(self, image, direction, image_title):
        import cv2, os, numpy as np
        cv2.imwrite(os.path.join(self._output, f"out_{image_title}.jpg"), image)
        self._images.append(np.copy(image))

    def end(self):
        if self._animate:
            import imageio, os, time
            print("Generating Animation")
            imageio.mimsave(os.path.join(self._output, "animate", f"out_{time.strftime('%m_%d_%Y %H.%M.%S')}.gif"), self._images)


class TurtleCallback(CallbackBase):
    """
    Build an animate gif.
    """

    def image_processed(self, image, direction, image_title):
        import turtle
        turtle.pendown()
        #turtle.left(direction*-12)
        turtle.seth(90-((-1*direction)*-90))

        print(f"{direction} - {turtle.heading()}")
        turtle.forward(10)

    def end(self):
        pass
