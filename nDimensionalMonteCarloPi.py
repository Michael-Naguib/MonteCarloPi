'''
Author:    Michael Sherif Naguib
Date:      March 13, 2020
@:         University of Tulsa
Description: see README.md

After my initial code written in montecarlopi.py that performs a Monte Carlo simulation using a circle inscribed in a
square ... I realized a similar simulation could be achieved in 3D ... I wondered if I could generalize the simulation
to an N Dimensional space ... I spent time to derive the necessary formulae ...in cases where n is an positive integer.

Note however .... I should also note that as the higher dimensional formulas involve a kth root the simulation will be
limited by the precision of the nth root function. (in addition to long division ... as in the 2D case)

'''

#imports
import numpy as np
import tqdm
import math
import random

def distSqr(x,y):
    '''
    :description: Calculates the distance squared from a point with coordinates x,y from the origin 0,0
    :param x: x coordinate
    :param y: y coordinate
    :return: distance squared
    '''
    return math.pow(x,2) + math.pow(y,2)

def magSquared(vector):
    '''
    :description: Calculate the squared magnitude of a vector
    :param vector: a numpy vector
    :return: the distance squared
    '''
    return sum([math.pow(vector[i],2) for i in range(len(vector))])

def nDFuncGenerator(dimension):
    '''
    :Description: Since a good portion of the function is itself seperable (i.e constant) with respect to the
    hypervolumes for the Hypersphere and Hypercube, much of the calculation can be precomputed... this function
    returns a function which has those values precomputed...
    :param dimension: the positive integer value that specifies the dimension (note the formula changes based on this dim)
    :return: a function that provides an estimate of PI in an N Dimensional Monte Carlo Simulation,
    (based on the hypervolumes for the Hypersphere and Hypercube)

    the returned function accepts two parameters
    param1: countForHyperSphere (or 2d circle 3d etc... )
    param2: countForHyperCube   (or 2d square 3d etc...)
    '''
    assert type(dimension) == type(1)# Assert it is an integer
    assert dimension >=2             # Assert we are at least in 2 Dimensions

    # 2 Dimensional case
    if dimension == 2:
        def d2Case(numInCircle,numInSquare):
            assert numInSquare != 0  # Catch Div by Zero
            return 4 * numInCircle / numInSquare
        return d2Case
    # 3 Dimensional Case
    elif dimension == 3:
        def d3Case(numInSphere,numInCube):
            assert numInCube != 0  # Catch Div by Zero
            return 6 * numInSphere / numInCube
        return d3Case
    # N Dimensional Case
    else:
        # Init a variable for the constant
        constant = None
        k = None
        # For the N dimensional case there are two scenarios: dimension is even or n is odd
        if dimension%2 ==0: #Even Case
            k = dimension //2
            assert k!=0
            # Derived formula
            constant = math.pow(math.factorial(k)*math.pow(2,2*k),1/k)
        else:# Odd Case
            k = (dimension -1)//2
            assert k!=0
            # Derived formula
            constant = math.pow(math.factorial(2*k +1)*math.pow(2,2*k+1)/(2*math.factorial(k)*math.pow(4,k)),1/k)
        # Return the function bound with the constant ... it turns out the seperable part of both the even and
        # the odd case are the same ... i.e    c*f(x)
        def dnCase(hypersphereCount,hypercubeCount):
            assert hypercubeCount!=0 # Catch Divide by zero
            if k%2==1:
                assert hypercubeCount>=0 and hypersphereCount>=0   # Catch - in nth roots odd ensure neither are negative (they never should be)
            return constant*math.pow(hypersphereCount/hypercubeCount,1/k)
        return dnCase

def monteCarloPiItrGenerator(dimension):
    '''
    :description: since points need to be generated differently i.e a point in 2D vs 3D vs nD ...
    a function is needed that can do this ... this function returns a function which is a generator ( in the sense of yield)
    for successive estimates of pi gi
    :param dimension: specifies the dimension for the simulation
    :return: a function which accepts two parameters
    a radius and a maximum iteration count... (this is based off the code in montecarlopi.py)
    '''

    def monteCarloPiItr(radius=10, iterations=100_000_000):
        '''
        :description: A generator that generates successive estimates of pi
        :param radius: the Radius of the Circle inscribed in the Square (both centered at 0,0)
        :param iterations: the number points to compute and use to update the estimate
        :yeild: the next estimate of pi
        '''


        # Count how many are in the hypersphere ( circle etc...)
        inHypersphereCount = 0
        # Store an estimate for Pi (will be updated as the simulation progresses)

        # Calculate the radius squared (once)
        radiusSquared = math.pow(radius, 2)
        # A numpy array used to shift the random nums into the desired range
        s = np.ones(dimension) / 2
        # Generate the pi esitmate calculator function (precomputing the constants)
        calcPiEstimate = nDFuncGenerator(dimension)

        # Begin iteration: i is the total up to that iteration .. (all points are in the square)
        for i in range(0, iterations + 1):
            # Pick random coords: the circle is centered @ 0,0 ... 0  so shift over the range of the square by subtracting 0.5
            # before scaling by the sidelength of the square ( side length = 2*radius)
            x = (np.random.rand(dimension)-s)*2*radius

            # Check if the point is within the circle: increment if it is (use squared distance to be efficient)
            inHypersphereCount = inHypersphereCount + 1 if  magSquared(x)<= radiusSquared else inHypersphereCount + 0

            # Update the pi estimate
            piEst = calcPiEstimate(inHypersphereCount,i+1)

            # Yield the pi esitmate
            yield piEst

    # Return the N- Dimensional configured Monte Carlo Pi calculator
    return monteCarloPiItr


if __name__ == "__main__":
    # Settings
    dimension = 6          # Run the simulation in nth Dimensional space
    radius = 1              # Radius of the hypersphere
    iterations = 10_000_000 # maximum iterations
    logEvery = 10_000       # Log every so many iterations

    # Run the simulation
    cnt=0
    for newEst in monteCarloPiItrGenerator(dimension)(radius=radius,iterations=iterations):
        cnt+=1
        if cnt%logEvery==0:
            print(newEst)
