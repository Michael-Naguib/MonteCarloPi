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
import numpy as np
import matplotlib.pyplot as plt
import tqdm

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

def monteCarloPiItr(radius=1,iterations=100_000_000):
    '''
    :description: A generator that generates successive estimates of pi
    :param radius: the Radius of the Circle inscribed in the Square (both centered at 0,0)
    :param iterations: the number points to compute and use to update the estimate
    :yeild: the next estimate of pi
    '''
    # Count how many are in the circle
    inCircleCount = 0
    # Store an estimate for Pi (will be updated as the simulation progresses)
    piEst = 0
    # Calculate the radius squared (once)
    radiusSquared = math.pow(radius, 2)

    # Begin iteration: i is the total up to that iteration .. (all points are in the square)
    for i in range(1, iterations + 1):
        # Pick random coords: the circle is centered @ 0,0 so shift over the range of the square by subtracting 0.5
        # before scaling by the sidelength of the square ( side length = 2*radius)
        x = (random.random() - 0.5) * radius * 2
        y = (random.random() - 0.5) * radius * 2

        # Check if the point is within the circle: increment if it is (use squared distance to be efficient)
        inCircleCount = inCircleCount + 1 if distSqr(x, y) <= radiusSquared else inCircleCount + 0

        # Update the pi estimate
        piEst = calcPiEstimate(inCircleCount,i)  # (all the points we select are in the square so our inSquareCount would be just i)

        # Yield the pi esitmate
        yield piEst

def plotSeries(series, x_name="x", y_name="y", title="Graph", x_key='x',y_key='y'):
    # Code adapted from my chaotic IFS project
    # Plotting Code: Passed a series list [series1,series2] where series {name:"",x:[],y:[]}
    # NOTE! CAN ONLY PLOT 3 colors before it starts using random values for colors
    # TAKEN from my PlotUtil Lib on github on 3/13/2020@10:48AM
    colors = [(70 / 255, 240 / 255, 240 / 255), (240 / 255, 50 / 255, 230 / 255), (210 / 255, 245 / 255, 60 / 255)]
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    idx = 0
    r = random.random
    for group in series:
        # Plot the points
        plt.scatter(group[x_key], group[y_key], c=[colors[idx] if idx < len(colors) else (r(), r(), r())],
                    s=np.pi * 3, alpha=0.5, label=group['name'])
        idx += 1
    plt.legend(loc='upper left')
    plt.show()

def reject_outliers(data, m=2):
    '''
    NOT MY CODE: i take no credit for this code...
    thanks to: https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
    :Description: this code rejects outliers ....
    :param data: array
    :param m:
    :return: data without outliers
    '''
    return data[abs(data - np.mean(data)) < m * np.std(data)]

# Main Simulation
if __name__ == "__main__":

    cnt=0
    for newEst in monteCarloPiItr():
        cnt+=1
        if cnt%10000==0:
            print(newEst)

    # Sample every k iterations:
    k = 10

    # Different Radius Values to Try:
    radii = [1,10,100]
    assert(len(radii)<=3) # a requirement of my plotting function ....
    # Point Quanty per Simulation]
    pointQuantity= 1000

    # Number of times to redo the simulation
    redos = 50
    allSeries=[]
    # Run the Simulation(s)
    for radius in radii:
        # Data structure to hold info about the series
        currentSeries = {
           "name": "radius = {0}".format(radius),
           "x":[],
           "y":[],
        }
        for rd in range(redos):
            # Use a counter to keep track of iterations
            cntr=0
            # Run the simulation getting the next estimate
            for newEstimate in tqdm.tqdm(monteCarloPiItr(radius=radius,iterations=pointQuantity)):
                if cntr%k==0:# Sample every k iters
                    if rd==0: # i.e it is the first time data is going in ... do nothing just add the data
                        currentSeries["x"].append(cntr)
                        currentSeries["y"].append(newEstimate)
                    else:
                        # Update the value as a running average

                        # Index the list of sampled data... since we log every k ... the index is cntr/k which is an int
                        indx = int(cntr/k)
                        assert float(indx) == cntr/k#check

                        currentSeries["y"][indx] = updateRunningAvg(currentSeries["y"][indx],newEstimate,rd+1)
                cntr+=1
            # Append the current series to all the series
        allSeries.append(currentSeries)

    # Graph the Data

    # Plot the convergence of the different simulations
    plotSeries(
        allSeries,
        x_name="Iterations  (sampled every {0}, redos={1})".format(k,redos),
        y_name="Estimate Value",
        title=" Estimate Value vs Iterations"
        )

    # Plot the histogram data for each radius
    bins = 100
    for i in range(len(radii)):
       cleaned_data= reject_outliers(np.array(allSeries[i]["y"]),m=2)
       plt.hist(cleaned_data,bins)
       plt.title("Estimates for radius={0} redos={1}".format(radii[i],redos))
       plt.xlabel("Estimate Values")
       plt.ylabel("Estimate Counts (outliers excluded)")
       plt.show()












