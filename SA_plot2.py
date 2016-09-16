#!/usr/bin/env python

import random
import time
import math
import matplotlib.pyplot as plt
import sys

"""This version will plot a graph of the results after simulating is done"""

#simulation parameters
T = start_temp = 1.1
coolingFactor = 0.99998
numPts= length = 300
maxIter = 300000
start_time = time.time()

#cooling function
def cooling(start_temp, alpha):
    T = start_temp * alpha
    return T

#create initial state
def getPath(numPts):
    path = []

    for i in range(numPts):
        x = random.random()
        y = random.random()

        path.append([x,y])
    return path


#determine the probability of accepting a move to a neighbor
def P(current_cost, next_cost, T):
    if next_cost < current_cost:
        return 1
    else:
        return math.exp( -abs(current_cost-next_cost)/T )

#generate a neighbor state and its cost
def getNeighbor(path):
    copy = path[:]
    # index1 = random.randrange(0,length)
    # index2 = (index1 + 1)%length
    # point1 = copy[index1]
    # point2 = copy[index2]
    #
    # copy[index1] = point2
    # copy[index2] = point1
    n = random.randrange(0,length+1)
    m = random.randrange(0,length+1)
    if n < m:
        copy[n:m] = reversed(copy[n:m])
    else:
        copy[m:n] = reversed(copy[m:n])

    i=0
    cost=0
    while i < length:
        a = copy[i]
        b = copy[(i+1)%length]
        cost += math.hypot(b[0]-a[0], b[1]-a[1])
        i+= 1

    # dist = np.diff(copy, axis=0)
    # segdists = np.hypot(dist[:,0], dist[:,1])
    # cost = np.sum(segdists)

    return copy, cost




##### MAIN BODY #####


current_path, current_cost = getNeighbor(getPath(numPts))
best_cost = start_cost = current_cost
costs = []
best_costs = []
iterations = 0
accepted_count = 0

#begin iterations
print('Working...'),
sys.stdout.flush()
while iterations < maxIter:
    next_path, next_cost = getNeighbor(current_path)  #get a neighbor for the current path
    iterations+= 1
    p=P(current_cost, next_cost, T)  # accept new path with probability
    T = cooling(T, coolingFactor)
    if random.random() < p:
        current_path = next_path
        current_cost = next_cost
        accepted_count+=1
    if current_cost < best_cost:
        best_cost = current_cost

    if iterations % 1000 == 0:       #every 100 iterations
        costs.append(current_cost)
        best_costs.append(best_cost)

x = range(0, maxIter,1000)
y = costs
y2 = best_costs
plt.plot(x,y,'-b', label='Selected Cost')
plt.plot(x,y2,'-r', label='Best Cost')
plt.ylabel("Path Cost")
plt.xlabel("Iterations")
legend = plt.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
plt.grid(True)
plt.title("Simulated Annealing on Traveling Salesman")
print("Done!")
print ('Finished %s iterations in %s seconds.' % (str(maxIter),(time.time() - start_time)))
print('Start Cost: %s' % (str(start_cost)))
print('Best Cost: %s' % (str(best_cost)))
plt.show()
