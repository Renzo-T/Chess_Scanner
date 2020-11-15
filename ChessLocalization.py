import cv2
import numpy as np
import os

def cropBorder(img, lines):
    dims = img.shape
    minX = float('inf')
    maxX = float('-inf')
    minY = float('inf')
    maxY = float('-inf')
    for line in lines:
        for x1, y1, x2, y2 in line:
            if(x1 < minX):
                minX = x1
            if(x2 < minX):
                minX = x2
            if(x1 > maxX):
                maxX = x1
            if(x2 > maxX):
                maxX = x2
            if(y1 < minY):
                minY = y1
            if(y2 < minY):
                minY = y2
            if(y1 > maxY):
                maxY = y1
            if(y2 > maxY):
                maxY = y2 
    if(minY > 10): 
        minY = minY-10
    if(minX > 10): 
        minX = minX-10
    if(dims[1] > maxX +10): 
        maxX = maxX + 10
    if(dims[0] > maxY +10): 
        maxY = maxY + 10
    crop = img[minY:maxY, minX:maxX]
    return crop



def localization(img):
    scriptDir = os.path.dirname(__file__)

    img_blur = cv2.GaussianBlur(img,(7,7),0)

    gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)


    # ret, thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    # cv2.imshow("temp", thresh1)
    dims = gray.shape
    # crop_r = img
    # crop_img = edges
    crop_r = img[100:dims[0]-40,500:dims[1]-570]
    crop_img = gray[100:dims[0]-40,500:dims[1]-570]
    
    edges = cv2.Canny(crop_img,150,200)
    cv2.imshow("gray",gray)
    cv2.imshow("edges",edges)
    # edges = cv2.Canny(crop_img,0,50,apertureSize = 3)
    # edges = cv2.Canny(crop_img,100,200)


    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,50,20,20)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(crop_r,(x1,y1),(x2,y2),(255,0,0),5)
    cannyPath = os.path.join(scriptDir, 'images/canny.png')
    cv2.imwrite(cannyPath, edges)
    crop_r_path = os.path.join(scriptDir, 'images/crop_r.png')
    cv2.imwrite(crop_r_path, edges)

    cv2.imshow("temp-1", img)
    cv2.imshow("temp",crop_img)
    cv2.imshow("temp2", crop_r)
    cv2.waitKey(0)
    # return crop_r

    crop = cropBorder(crop_r, lines)
    dims = crop.shape
    crop = crop[10:dims[0]-10,10:dims[1]-10]

    edges = cv2.Canny(crop,50,150,apertureSize = 3)

    lines = cv2.HoughLinesP(edges,1,np.pi/180,15,50,300,20)
    # for line in lines:
        # for x1,y1,x2,y2 in line:
            # cv2.line(crop,(x1,y1),(x2,y2),(255,0,0),5)
    crop2 = cropBorder(crop, lines)
    cv2.imshow("1", crop)
    cv2.imshow("2", crop2)
    cv2.waitKey(0)
    return crop2


def dice(img):

    dims = img.shape
    y = dims[0]//8
    x = dims[0]//8

    curX = 0
    curY = 0
    for i in range(8):
        for j in range(8): 
            print(str(i) + " " + str(j))
            cv2.imshow(str(i*8+j+1), img[curY:curY+y, curX:curX+x])
            curX += x
        curX = 0
        curY += y
    
    cv2.waitKey(0)
    return img