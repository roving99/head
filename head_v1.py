#!/usr/bin/python

import cv
import sys
import serial
import time

CAMERA_VIEW  = 60     # degrees
CAMERA_VIEW_H  = 40     # degrees
CAMERA_WIDTH = 213    # pixels
CAMERA_HEIGHT = 160    # pixels

# Get user supplied values
cascPath = sys.argv[1]
portName = sys.argv[2]

# Create the haar cascade
faceCascade = cv.Load(cascPath)

def xToDegrees(x):
    d = 90-(CAMERA_VIEW/2)+(float(x)/float(CAMERA_WIDTH))*float(CAMERA_VIEW) # approximatelty!
    d += 0
    return int(d)

def yToDegrees(x):
    d = 90+(CAMERA_VIEW_H/2)-(float(x)/float(CAMERA_HEIGHT))*float(CAMERA_VIEW_H) # approximatelty!
    d += 0
    return int(d)

try:
    capture1=cv.CaptureFromCAM(1)
except:
    print "Shit out of luck - no capture from CAM0"
    sys.exit()

try:
    image = cv.QueryFrame(capture1)
except:
    print "Failed to capture frame."
    sys.exit()
print "result image size :", image.width/3, image.height/3

try:
    port = serial.Serial(portName, 9600, timeout=1)
except:
    port = None

if port:
    time.sleep(9)
    text ='Arduino booting..'
    while(text!=''):    # print messages until serial timeout
        print text.rstrip()
        text = port.readline()
    print 'Done booting.'
    
    port.flush()
    port.write('?\n')
    text = port.readline()
    print text

image_result = cv.CreateImage((image.width/3, image.height/3),8,3)

target_n_degrees = 90

command = """50 3s 90 2s 100 1s 90 0s\n"""
print command
if port: port.write(command)

lastTime = time.time()

while cv.WaitKey(10)==-1:
    image = cv.QueryFrame(capture1)
    cv.Resize(image,image_result)
    # Detect faces in the image
    faces = cv.HaarDetectObjects(image_result, faceCascade, cv.CreateMemStorage())
    fps = 1.0/(time.time()-lastTime)
    lastTime = time.time()
    print "{0} faces {1}fps".format(len(faces), int(fps))

    # Draw a rectangle around the faces
    for (x, y, w, h),n in faces:
            cv.Rectangle(image_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.Line(image_result, (x, y+h/3), (x+w, y+h/3), (0, 255, 0), 2)
    if len(faces)>0:
        (x, y, w, h),n = faces[0]
        target_x = x+w/2
        target_y = y+h/3
        target_x_degrees = xToDegrees(target_x)
        target_y_degrees = yToDegrees(target_y)

        if (target_x_degrees>105) and (target_n_degrees>20):
            target_n_degrees+=10
        if (target_x_degrees<75) and (target_n_degrees<160):
            target_n_degrees-=10

        print target_x, target_y, target_x_degrees, target_y_degrees, target_n_degrees
        command = """%s 2s%s 1s%s 0s\n"""%(target_n_degrees, target_x_degrees+10, target_y_degrees)
        print command
        if port: port.write(command)

    cv.ShowImage("Faces found", image_result)

if port:
    port.close()
