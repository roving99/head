#!/usr/bin/python

import cv
import sys
import serial
import time

CAMERA_VIEW  = 60     # degrees
CAMERA_WIDTH = 213    # pixels

# Get user supplied values
cascPath = sys.argv[1]
portName = sys.argv[2]

# Create the haar cascade
faceCascade = cv.Load(cascPath)

def xToDegrees(x):
    d = 90-(CAMERA_VIEW/2)+(float(x)/float(CAMERA_WIDTH))*float(CAMERA_VIEW) # approximatelty!
    return int(d)

try:
    capture1=cv.CaptureFromCAM(0)
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
while cv.WaitKey(10)==-1:
    image = cv.QueryFrame(capture1)
    cv.Resize(image,image_result)
    # Detect faces in the image
    faces = cv.HaarDetectObjects(image_result, faceCascade, cv.CreateMemStorage())
    print "Found {0} faces!".format(len(faces))

    # Draw a rectangle around the faces
    for (x, y, w, h),n in faces:
            cv.Rectangle(image_result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv.Line(image_result, (x, y+h/3), (x+w, y+h/3), (0, 255, 0), 2)
    if len(faces)>0:
        (x, y, w, h),n = faces[0]
        target_x = x+w/2
        target_y = y+h/3
        target_x_degrees = xToDegrees(target_x)
        print target_x_degrees, target_y
        command = """%s 1s\n"""%(target_x_degrees)
        print command
        if port: port.write(command)

    cv.ShowImage("Faces found", image_result)

if port:
    port.close()
