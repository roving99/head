#!/usr/bin/python

def clamp(n, min_, max_):
    """returns n where min<n<max."""
    return max(min(max_,n),min_)

class servo():
    def __init__(self, name = '', command = '{0}', x = 90, minLimit = 20, maxLimit = 160, offset = 0):
        self.name = name
        self.command_ = command
        self.x = x          #   ABSOLUTE value (disregards offsets or scaling, if used)
        self.minLimit = minLimit    # Absolute
        self.maxLimit = maxLimit    # Absolute
        self.offset = offset

    def command(self):
        """command to send to servo controller (arduino for example)."""
        return (self.command_).format(self.x)

    def set(self,x):
        """Set servo to position taking limits and offsets into account."""
        self.x = clamp(x+self.offset, self.minLimit, self.maxLimit)

    def get(self):
        """Gets current position of servo."""
        return self.x-self.offset

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

    s3 = servo(name="Neck up/down", command="{0} 3s", offset=35-90, minLimit=5,  maxLimit=90)
    s2 = servo(name="Neck left/right", command="{0} 2s", offset=90-90, minLimit=20, maxLimit=160)
    s1 = servo(name="Eyes left/right", command="{0} 1s", offset=100-90,minLimit=50, maxLimit=140)
    s0 = servo(name="Eyes up/down", command="{0} 0s", offset=90-90, minLimit=40, maxLimit=130)
    
    servos = [s0,s1,s2,s3]

    if port:
        time.sleep(9)
        text ='Arduino booting..'
        while(text!=''):    # print messages until serial timeout
            print text.rstrip()
            text = port.readline()
        print 'Done booting.'
        port.flush()

    for i in range(len(servos)):
        s = servos[i]
        print s.name, s.minLimit, s.maxLimit, s.offset, s.command_

    s = '0'
    while s!='':
        s = input("Enter servo number     [0-3]:")
        if s!='':
            p = input("Enter servo position [0-180]:")
            servos[s].set(p)
            print servos[s].command()
            if port: port.write(servos[s].command()+"\n")

    if port:
        port.close()
