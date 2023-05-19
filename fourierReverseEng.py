from math import *
import drawer
from plotter import *
def convertToFunction(pointList):
    functions = []
    sigmaDistance = 0
    for point in range(len(pointList)):
        pointX = pointList[point][0]
        pointY = pointList[point][1]
        originX = pointList[point-1][0]
        originY = pointList[point-1][1]
        if not (pointX == originX and pointY == originY):
            distance = sqrt((pointX-originX)**2 + (pointY-originY)**2)
            dx = (pointX-originX)/distance
            dy = (pointY-originY)/distance
            sigmaDistance += distance
            functions.append([originX,originY,dx,dy,sigmaDistance,distance])
    return functions
def functionsToPoints(functions,pointAmount):
    points = []
    totalLenght = functions[-1][4]
    partSize = totalLenght/pointAmount
    functionID = 0
    for x in range(pointAmount):
        while x*partSize >= functions[functionID][4]:
            functionID += 1
        sideDistance = functions[functionID][5]
        xSideDelta = (x/pointAmount*totalLenght - functions[functionID][4]+ functions[functionID][5])/totalLenght
        originX = functions[functionID][0]
        originY = functions[functionID][1]
        dx = functions[functionID][2]
        dy = functions[functionID][3]
        points.append([originX + xSideDelta*dx*totalLenght,originY + xSideDelta*dy*totalLenght])

    return points
function = functionsToPoints(convertToFunction(drawer.pointMatrix),1000)
def integrate(pointList, expID):
    integralR = 0
    integralI = 0
    for pointID in range(len(pointList)):
        pointR = pointList[pointID][0]
        pointI = pointList[pointID][1]
        x = pointID/len(pointList)
        expR = cos(-2*pi*expID*x)
        expI = sin(-2*pi*expID*x)
        integralR += (pointR * expR - pointI * expI)
        integralI += (pointR * expI + pointI * expR)
    return [integralR/len(pointList),integralI/len(pointList)]
def generateSpeeds(amount):
    speeds = []
    count = 0
    for n in range(amount):
        if n%2:
            speeds.append(count)
        else:
            speeds.append(-count)
            count += 1
    return speeds
def reverse(functionVal,precision):
    vectorSpeeds = generateSpeeds(precision)
    vectors = []
    for vectorSpeed in vectorSpeeds:
        vectors.append(integrate(function, vectorSpeed))
    return vectorSpeeds,vectors

