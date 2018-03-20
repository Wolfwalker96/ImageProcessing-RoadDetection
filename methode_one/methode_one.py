"""
Road contourdetection - Step : FreeScale Cup
Algorithm One - Test
"""
import cv2
import imageio
import time
import numpy as np
import os


def algorithm(filepath):
    img_i = cv2.imread(filepath)
    img = cv2.cvtColor(img_i,cv2.COLOR_BGR2GRAY)

    # Contrast increase
    # img = np.array([np.array([ 0 if pixel < 100 else 255 for pixel in row], dtype = np.uint8) for row in img], dtype = np.uint8 )

    trash,img = cv2.threshold(img,100,255.0,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Open
    kernel = np.ones((5,5),np.uint8)
    # img = cv2.
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.erode(img, kernel, iterations=3)
    img = cv2.dilate(img, kernel, iterations=3)

    #cv2.imshow("Morph",img)


    # Contour detection
    ret,thresh = cv2.threshold(img,127,255,0)
    image, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("Tresh",thresh)
    #cv2.imshow("Image",img)
    cv2.waitKey(0)
    
    
    # Contours that touch the bottom
    height, width  = img.shape[:2]
    height -= 5 # ptit marge
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
    
    return cv2.drawContours(img_i, [contour], -1, (0,255,0), 3)


if __name__ == "__main__":
    print(__doc__)
    inputdir = os.path.abspath("picture_freescale/15.04.16/Avant/Sequence6/")
    outputdir = os.path.abspath("output/")
    images = os.listdir(inputdir)
    out_images = []

    if not os.path.exists(outputdir):
        os.mkdir("output")
    if not os.path.exists(os.path.join(outputdir,"animate")):
        os.mkdir(os.path.join(outputdir,"animate"))
    counter = 0
    import re
    images.sort(key=lambda x: int(re.findall("\d+",x)[0]))
    for image in images:
        print(f"\r{counter}/{len(images)}",end="\r")
        if image.endswith(".JPG"): 
            counter+=1
            img = algorithm(os.path.join(inputdir, image))
            out_images.append(img)
            cv2.imwrite(os.path.join(outputdir,f"out_{image}"), img)
    print("Generating Animation")
    imageio.mimsave(os.path.join(outputdir,"animate",f"out_{time.strftime('%m_%d_%Y %H.%M.%S')}.gif"), out_images)
