#!/usr/bin/python

import random, math, pprint

class Petal():
    """
    Represents one function.variation instance of the collection used in the Chaos Game
    """
    MaxFunc=4 # number of functions implemented
    def __init__(self, data = []):
        """
        default init with default coefficients
        1 argument - use it as the function number, otherwise default
        3 arguments - initialize with those data
        """
        if type(data) is int:
            self.projCoeff=[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
            self.prob=1.0
            self.func=data % self.MaxFunc;            
        elif len(data)==0:
            self.projCoeff=[1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
            self.prob=1.0
            self.func=0
        else:
            self.prob,  self.projCoeff,  self.func,  self.colors = data
        self.colors=[0]*3
        for i in range(9):
            self.colors[random.randint(0, 2)] +=1
            
    def get(self):
        """the mathematical parameters for the Petal"""
        return [self.prob, self.projCoeff, self.func, self.colors]
        
    def mutate(self):
        """randomly mutates one parameter"""
        p=random.randint(0, len(self.projCoeff))
        if p==0 :
            print('changing probability')
            self.prob*= random.random()+0.5
        else:
            p-=1
            print('changing coefficient %d' % (p))
            self.projCoeff[p]  += 0.1*(random.random()-0.5)
            pprint(self.projCoeff)
            
    def calculate(self, x, y):
        """calculates one jump"""
        c=self.projCoeff
        x, y=  c[0]*x+c[1]*y+c[2], c[3]*x+c[4]*y+c[5]
        if self.func ==0:
            # do nothing if func == 0, be the same
            pass
        if self.func == 1:
            '''sinusoidial'''
            x, y= math.sin(x), math.sin(y)
        elif self.func == 2:
            '''spherical'''
            r = 1.0 / (x * x + y * y)
            x, y= r*x,  r*y
        elif self.func == 3:
            '''swirl'''
            r = x * x + y * y
            x, y = x * math.sin (r) - y * math.cos (r),  x * math.cos (r) + y * math.sin (r)
        else:
            '''random square'''
            x, y = random.random()-0.5,  random.random()-0.5
        # done 
        x, y, w = c[6]*x+c[7]*y+c[8], c[9]*x+c[10]*y+c[11],  c[12]*x+c[13]*y+c[14]
        if w==0:
            x, y=0, 0
        else:
            x, y=x/w, y/w
        return x, y
