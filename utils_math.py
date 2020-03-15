#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math

def math_determinant(a, b, c, d, e, f, g, h, i):
    """
    returns the determinant of the 9 values of a 3 x 3 matrix
    """
    return (a * e * i - a * f * h - b * d * i + b * f * g + c * d * h - c * e * g)

def math_map_list(values,toMin=0,toMax=1):
    """
    Maps the values of a list from a minimum value to a maximum value.
    Arguments:
    ----------
    values : list to be mapped

    Optional Arguments:
    ----------
    toMin : minimum value of the list's target range (default = 0)
    toMax : maximum value of the list's target range (default = 1)
    """
    minValue=min(values)
    maxValue=max(values)
    delta=maxValue-minValue
    deltaTarget=toMax-toMin
    return list(map(lambda x: toMin+deltaTarget*(x-minValue)/delta, values))

def math_map(value, fromMin, fromMax, toMin, toMax):
    """
    Maps a value from one range to another.
    Arguments:
    ----------
    value : value to be mapped
    fromMin : lower bound of the value's current range
    fromMax : upper bound of the value's current range
    toMin : lower bound of the value's target range
    toMax : upper bound of the value's target range
    """
    delta = fromMax - fromMin
    if delta == 0 : return 0
    return toMin + ((toMax - toMin) / delta) * (value - fromMin)

# this object helps to encapsulate sinus functions
class SinusFunction(object):
    def __init__(self, frequency, amplitude=1, phase=0, offset=0):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.offset = offset

    def getValue(self,value):
        return math.sin(self.frequency * value + self.phase) * self.amplitude + self.offset
