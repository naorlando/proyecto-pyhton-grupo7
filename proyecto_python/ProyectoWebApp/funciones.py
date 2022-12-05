import cv2 as cv
import numpy as np

def convertir_prioridad(value):
    if value == 1:
        return 'Alta'
    if value == 2:
        return 'Media'
    if value == 3:
        return 'Baja'

def convertir_estado(value):
    if value == 1:
        return 'Pendiente'
    if value == 2:
        return 'En Proceso'
    if value == 3:
        return 'Finalizado'


frameWidth = 1280
frameHeight = 720
cap = cv.VideoCapture(0,cv.CAP_DSHOW)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)



def preProcessing(img):
    imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv.erode(imgDial,kernel,iterations=1)

    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv.findContours(
        img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 5000:
            # cv.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            if area>maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    # cv.drawContours(imgContour, biggest, -1, (0, 255, 0), 23)
    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]=myPoints[np.argmin(diff)]
    myPointsNew[2]=myPoints[np.argmax(diff)]

    return myPointsNew


def getWarp(img,biggest):
    biggest = reorder(biggest)
    # pts0 = np.float32([[357, 59], [117, 66], [171, 455], [417, 389]])
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0], [frameWidth,0], [0,frameHeight], [frameWidth,frameHeight]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img,matrix,(frameWidth, frameHeight))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv.resize(imgCropped,(frameWidth,frameHeight))

    return imgCropped


def paperProcessing(img):
    imgWarpGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgAdaptativeThre = cv.adaptiveThreshold(imgWarpGray,255,1,1,7,2)
    imgAdaptativeThre = cv.bitwise_not(imgAdaptativeThre)
    imgAdaptativeThre = cv.medianBlur(imgAdaptativeThre,3)
    return imgAdaptativeThre