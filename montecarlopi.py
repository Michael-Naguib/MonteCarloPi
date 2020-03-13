'''
Author:    Michael Sherif Naguib
Date:      March 13, 2020
@:         University of Tulsa
Description: see README.md

( the coronavirus hit so we were sent home from college ... I had the idea to finally code this last week and finished the
first working code @ DFW ... I have touched it up now and put it on github)

'''

# Imports
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

def calcPiEstimate(numInCircle,numInSquare):
    '''
    :description: Calculates an Estimate of Pi using the given parameters;
    NOTE! The calculation is based off of a circle inscribed in a square.
    Derivation
    where s is a scaling factor
    let r = s where r is the radius of the circle
    thus the side length of the square  = 2s = 2r
    1) As = Area Square = (2r)^2 = 4*r^2
    2) Ac = Area Circle = pi*r^2
    3) thus pi = Ac/r^2
    4) r^2 = Area Square/4           (from stmt 1)
    5) thus pi = Ac/ (As/4) = 4Ac/As

    :param numInCircle: a count of the number of points within the circle
    :param numInSquare: a count of the number of points within the square
    :return: an estimate of pi

    '''
    assert numInSquare !=0 # Catch Div by Zero
    return 4*numInCircle/numInSquare

def updateRunningAvg(curAvg,val,valCnt):
    '''
    :description: compute a running average
    :param curAvg: the current value of the average
    :param val: the new value to factor into the average
    :param valCnt: the number of values taken into account for the curAvg
    :return: the updated average

    (NOTE! this function does not change any of the parameters --> no side effect...)
    it is the prgmr's responsibility to update those vals
    '''
    assert valCnt != 0
    return (curAvg*valCnt + val)/(valCnt+1)
    
# Main Simulation
if __name__ == "__main__":

    # The Radius of the Circle inscribed in the Square (both centered at 0,0)
    radius=1000
    # Iterations: the number points to compute and use to update the estimate
    iterations = 100000000
    # Print the updated Estimate every n iterations
    n = 100000

    # Count how many are in the circle
    inCircleCount = 0
    # Store an estimate for Pi (will be updated as the simulation progresses)
    piEst = 0
    # Calculate the radius squared (once)
    radiusSquared = math.pow(radius,2)

    # Begin iteration: i is the total up to that iteration .. (all points are in the square)
    for i in range(1,iterations+1):
        # Pick random coords: the circle is centered @ 0,0 so shift over the range of the square by subtracting 0.5
        # before scaling by the sidelength of the square ( side length = 2*radius)
        x = (random.random()-0.5)*radius*2
        y = (random.random()-0.5)*radius*2

        # Check if the point is within the circle: increment if it is (use squared distance to be efficient)
        inCircleCount = inCircleCount + 1 if distSqr(x,y) <= radiusSquared else inCircleCount + 0

        # Update the pi estimate
        piEst = calcPiEstimate(inCircleCount,i)# (all the points we select are in the square so our inSquareCount would be just i)

        # Print every n iterations
        if i%n==0:
            print("Iteration: {0} Estimate: {1}".format(i,piEst))


