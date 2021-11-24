'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________



 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import numpy as np
import itertools as it

import parameters as pm

np.seterr (over = 'raise')
np.random.seed ()

sigmoid = np.tanh

def sigmoidDeriv (vector):
    return 1 - np.square (sigmoid (vector))

def getScaled (array):
    offset = array - array.min (axis = 0)
    aRange = array.max (axis = 0) - array.min (axis = 0)
    aRange [aRange == 0] = 1
    return -1 + 2 * (offset / aRange)

class NeuralNet:
    def __init__(self, sampleFileName):
        self.sampleFileName = sampleFileName

        with open (self.sampleFileName) as self.sampleFile:
            self.samples = getScaled (np.array ([[float (word) for word in line.split ()] for line in self.sampleFile.readlines ()])) .T
            np.savetxt ('np_samples.txt', self.samples.T)
            print ('samples shape:', self.samples.shape)

        self.partitionSize = int (len (self.samples) / pm.nrOfPartitions)  # Rounds down, so in most cases a remainder of the samples will not be used
        self.weights0 = .0001 * np.random.rand (pm.hiddenDim, pm.inputDim)
        self.weights1 = .0001 * np.random.rand (pm.outputDim, pm.hiddenDim)

        self.cycle ()

    def partition (self):
        testStartIndex = self.partitionIndex * self.partitionSize
        testStopIndex = testStartIndex + self.partitionSize
        self.testSamples = self.samples [ : , testStartIndex : testStopIndex]
        self.trainingSamples = np.hstack ((self.samples [ : , : testStartIndex], self.samples [ : , testStopIndex : ]))

    def cost (self):
        return np.sum ((self.refOutputs - self.outputs) ** 2) / len (self.outputs)

    def select (self, samples):
        self.inputs = samples [ : pm.inputDim]
        self.refOutputs = samples [pm.inputDim : ]

    def report (self, samplesKind):
        print ('partition', self.partitionIndex, samplesKind, '- cost:', self.cost ())

    def classify (self):
        self.outputs0 = sigmoid (self.weights0 @ self.inputs)
        self.outputs = self.weights1 @ self.outputs0

    '''
    def correct (self): # For each layer: weights += d sum_of_squared_corrections / d weights
        commonFactor = 2  * sigmoidDeriv (self.outputs) * (self.refOutputs - self.outputs)
        self.weights0 += sigmoidDeriv (self.outputs0) * (self.weights1.T @ commonFactor) @ self.inputs.T  
        self.weights1 += commonFactor @ self.outputs0.T  
    '''
    
    def correct (self):
        weightsTensor = (self.weights0, self.weights1)
        bestWeightsIndex = 0
        bestRowIndex = 0
        bestColumnIndex = 0
        bestFactor = 1
        currentCost = self.cost ()
        lowestCost = currentCost

        for weightsIndex, weights in enumerate (weightsTensor):
            for rowIndex in range (weights.shape [0]):
                for columnIndex in range (weights.shape [1]):
                    for signedGain in (-pm.gain, pm.gain):
                        originalWeight = weights [rowIndex, columnIndex]
                        factor = 1 + signedGain  * currentCost
                        weightsTensor [weightsIndex][rowIndex, columnIndex] *= factor
                        self.classify ()
                        cost = self.cost ()

                        if cost < lowestCost:
                            lowestCost = cost
                            bestWeightsIndex = weightsIndex
                            bestRowIndex = rowIndex
                            bestColumnIndex = columnIndex
                            bestFactor = factor

                        weightsTensor [weightsIndex][rowIndex, columnIndex] = originalWeight

        weightsTensor [bestWeightsIndex][bestRowIndex, bestColumnIndex] *= bestFactor

    def train (self):
        self.select (self.trainingSamples)
        count = 0
        while True:
            self.classify ()
            if self.cost () < pm.maxCost:
                break
            self.correct ()
            count = (count + 1) % 1
            if not count:
                print ('cost:', self.cost ())
                # print ('ist:', self.outputs [:8])
                # print ('soll:', self.refOutputs [:8])

        self.report ('training set')

    def test (self):
        self.select (self.testSamples)
        self.classify ()
        self.report ('test set')

    def cycle (self):
        for self.partitionIndex in range (pm.nrOfPartitions):
            self.partition ()
            self.train ()
            self.test ()

neuralNet = NeuralNet (pm.sampleFileName)

