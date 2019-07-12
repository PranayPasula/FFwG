import math
import numpy as np

class QFTclass:

    imagematrix = []
    QFTmatrix = []
    IQFTMatrix = []
    h = 0
    w = 0
    c = 0

    @classmethod
    def computeQFT(cls, u, v):
        for x in range(cls.h):
            for y in range(cls.w):
                quat = np.quaternion(0, cls.imagematrix[x, y, 0], cls.imagematrix[x, y, 1], cls.imagematrix[x, y, 2])
                mu = 1 / math.sqrt(3)
                exponentfactor = -(2 * mu * math.pi) * (((x * u) / cls.h) + ((y * v) / cls.w))
                coef = quat * math.exp(exponentfactor)
                cls.QFTmatrix[u, v] = cls.QFTmatrix[u, v] + coef
        cls.QFTmatrix[u, v] = cls.QFTmatrix[u, v] * (1 / math.sqrt(cls.h * cls.w))

    @classmethod
    def computeIQFT(cls, u, v):
        for x in range(cls.h):
            for y in range(cls.w):
                quat = cls.QFTmatrix[x, y]
                mu = 1 / math.sqrt(3)
                exponentfactor = (2 * mu * math.pi) * (((x * u) / cls.h) + ((y * v) / cls.w))
                coef = quat * math.exp(exponentfactor)
                cls.IQFTMatrix[u, v] = cls.IQFTMatrix[u, v] + coef

        cls.IQFTMatrix[u, v] = cls.IQFTMatrix[u, v] * (1 / math.sqrt(cls.h * cls.w))

    def getQFTMatrix(self):
        return self.QFTmatrix

    def getIQFTMatrix(self):
        return self.IQFTMatrix