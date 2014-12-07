#!/usr/bin/python

import myservo as s

class head():
    """Head is a collection of four servos - 2 for eyes, 2 for neck.
    0 - eyes up and down 40-130. 90 is straight ahead.
    1 - eyes left and right 50-140. 100 is straight ahead.
    2 - neck left and right 20-160. 90 is straight ahead.
    3 - neck up and down 5-90. 35 is straight ahead.
    """
    def __init__(self):
        """Set servo parameters"""
        self.eye = [90,90]
        self.neck = [90,90]
        self.neckX = s.servo(command="{0} 3s", offset=35-90, minLimit=5,  maxLimit=90)
        self.neckY = s.servo(command="{0} 2s", offset=90-90, minLimit=20, maxLimit=160)
        self.eyeX  = s.servo(command="{0} 1s", offset=100-90,minLimit=50, maxLimit=140)
        self.eyeY  = s.servo(command="{0} 0s", offset=90-90, minLimit=40, maxLimit=130)

    def look(self,direction):
        """[x-angle, y-angle]. Eyes straight ahead."""
        self.setEyes([90,90])
        self.setNeck(direction)
        pass

    def setEyes(self,direction):
        self.eyeX.set(direction[0])
        self.eyeY.set(direction[1])

    def setNeck(self,direction):
        self.neckX.set(direction[0])
        self.neckY.set(direction[1])

    def command(self):
        return self.eyeY.command()+self.eyeX.command()+self.neckX.command()+self.neckY.command()

if __name__=="__main__":
    import sys
    import serial
    import time

    portName = "/dev/ttyUSB0"

    try:
        port = serial.Serial(portName, 9600, timeout=1)
    except:
        print "Failed to open",portName
        sys.exit()

    if port:
        time.sleep(9)
        text ='Arduino booting..'
        while(text!=''):    # print messages until serial timeout
            print text.rstrip()
            text = port.readline()
        print 'Done booting.'
        port.flush()
#        port.write('?\n')
#        text = port.readline()
#        print text

    h = head()
    h.look([90,90])
    print h.command()
    if port: port.write(h.command()+"\n")

    input()
    if port:
        port.close()
