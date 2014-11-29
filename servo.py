#!/usr/bin/python

def clamp(n, min_, max_):
    return max(min(max_,n),min_)

class servo():
    def __init__(self, command = '{0}', x = 90, minLimit = 20, maxLimit = 160, offset = 0):
        self.controlCommand = command
        self.x = x
        self.minLimit = minLimit
        self.maxLimit = maxLimit
        self.offset = offset

    def command(self):
        return (self.controlCommand).format(self.x)

    def set(self,x):
        self.x = clamp(x, self.minLimit, self.maxLimit)

    def get(self):
        return self.x
