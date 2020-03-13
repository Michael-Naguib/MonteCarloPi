# MonteCarloPi
An admittedly somewhat naive approach to computing PI using a Monte Carlo Simulation with standard python floating point implementation

## Methodology
![explanation](explanation.jpg)
![graph](graph.jpg)
- Graph generated using [Desmos](https://www.desmos.com/)
## Implementation:
- A monte carlo simulation was configured to calculate Pi given a fixed number of iterations and a specified radius for the circle. 
- Calculations were repeated and averaged for each iteration a pre specified number of times
## Results
- The following graph depicts the convergence of the simulations on the value given different values for the radius.
- Data was averaged over 50 redundant redos of the simulations
![EstimatedValueVsIterations](EstimatedValueVsIterations.png)
- The following three graphs are the histogram charts for for the estimated values of pi given the radius. 
- The graphs indicate that the value of Pi lies somewhere between 3.14 and 3.15
- A hand inspection of the data also revealed that the closest estimate the simulation could achieve was 3.141; This method for iterations up to 7k only yielded 3 digits of precision at best. 
![EstimatesRadius1](EstimatesRadius1.png)
![EstimatesRadius10](EstimatesRadius10.png)
![EstimatesRadius100](EstimatesRadius100.png)


