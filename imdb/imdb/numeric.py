from __future__ import division
import math


class Vector(list):
    def map(self, funct):
        return self.__class__(funct(x) for x in self)

    def map_pair(self, other, funct=lambda x, y: x * y):
        return self.__class__(funct(x, y) for x, y in zip(self, other))

    dot = map_pair

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dot(other)

        return self.map(lambda x: x * other)        

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, Vector):
            return self.map_pair(other, lambda x, y: x + y)

        return self.map(lambda x: x + other)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Vector(-x for x in self)
    
    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __abs__(self):
        return self.map(abs)


class StatVector(Vector):
    def mean(self):
        return sum(self)/len(self)

    def var(self):
        _xs = self - self.mean()
        return _xs.dot(_xs).mean()

    def std(self):
        return math.sqrt(self.var())

    def prob(self, cond):
        return self.map(lambda x: int(cond(x))).mean()

    def joint_prob(self, cond1, cond2):
        return self.prob(lambda x: cond1(x) and cond2(x))

    def cond_prob(self, cond1, cond2):
        return self.joint_prob(cond1, cond2)/self.prob(cond2)

    def min(self):
        return min(self)

    def max(self):
        return max(self)