import math
# this object helps to encapsulate sinus functions
class SinusFunction(object):
    def __init__(self, frequency, amplitude=1, phase=0, offset=0):
		self.frequency = frequency
		self.amplitude = amplitude
		self.phase = phase
		self.offset = offset
    def getValue(self,value):
        return math.sin(self.frequency * value + self.phase) * self.amplitude + self.offset
