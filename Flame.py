#!/usr/bin/python
"""
One fractal flame, which contains several Variations, here called Petals
"""
import io, json,  pprint, random, math
from Petal import Petal

class Flame():
    """
    calculates a fractal flame similar but not exactly like in flam3
    """
    
    MaxFill=100 # the exit criteria for stopping the chaos game
    
    def __init__(self):
        """puts 3 standard petals into the flame"""
        self.petals=[Petal(), Petal(1), Petal(2), Petal(3)]
            
    def getConfig(self):
        """the vector of all petals, themselves as data vectors"""
        data=[ pet.get() for pet in self.petals]
        return data
    
    def fillConfig(self, data):
        """replaces the petals with ones obtained from data"""
        self.petals=[ Petal(en) for en in data ]
        
    def read(self, fn):
        """reads a json file and creates the petals"""
        print('reading <- %s' %(fn))
        data=[]
        with io.open(fn, 'r') as datafile:
            data=json.load(datafile)
        self.fillConfig(data)
        
    def write(self, fn):
        """creates a json file with all parameters"""        
        print('writing -> %s' % (fn))
        data=self.getConfig()
        with io.open(self.fn, 'w') as datfile:
            json.dump(data, datfile)
            
    def mutate(self):
        """carries out one mutation"""
        probN=random.random()
        if probN < 0.001:
            pet=Petal(random.randomint(0, 1e9))
            pet.mutate()
            self.petals.append(pet)
        else:
            pet=random.choice(self.petals)
            pet.mutate()
            if pet.prob < 0.01:
                self.petals.remove(pet)
        probSum=0
        for pet in self.petals:
            probSum+= pet.prob
        probSum=1/probSum
        for pet in self.petals:
            pet.prob*=probSum
            
    def calculate(self, parent,  width,  height,  callback):
        """
        carries out the Chaos Game with all petals - time consuming
        
        It randomly selects a petal and let the petal calculate the new point, the points are recorded into histograms, one for each color.
        At the end the logarithm is taken of all buckets and the maximal value is recorded in maxd.
        The callback is called with the parent and self.
        Divergent flames are re-initialized with a random point in the center square.
        """
        self.pixmap = None
        buckets=[[ [0]*3 for i in range(height)] for j in range(width)]
        x, y= random.random()-0.5,  random.random()-0.5
        outside=0
        dim=width
        if height<dim:
            dim=height
        dim = dim/2
        mw=width
        hw=mw/2
        mh=height
        hh=mh/2
        iteration=0
        while True:
            iteration+=1
            petal=random.choice(self.petals)
            x, y = petal.calculate(x, y)
            fx=math.floor( x*dim+hw)
            fy=math.floor(y*dim+hh)
            if fx<0 or fx>=mw or fy<0 or fy>=mh:
                outside+=1
                if outside >10:
                    x, y = random.random()-0.5,  random.random()-0.5
                    #self.dead=True
                    #callback(self, buckets, 0)
                    #return
                continue    
            else:
                outside=0
            d=0
            for c in range(3):
                buckets[fx][fy][c]+=petal.colors[c]
                d+=buckets[fx][fy][c]
            if d > self.MaxFill:
                break
        pprint(iteration)
        maxd=0
        for i in range(width):
            for j in range(height):
                for c in range(3):
                    d=buckets[i][j][c]
                    if d>1:
                        d=math.log(d)
                        if d>maxd:
                            maxd=d
                    else:
                        d=0
                    buckets[i][j][c]=d
        self.buckets=buckets
        self.maxd=maxd
        callback(parent, self)
    
