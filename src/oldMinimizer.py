import math
from random import random
from copy import deepcopy
import time_estimator

eps = .000001
dT = .00001

def mag(x):
    return(math.sqrt(sum([q*q for q in x])))

def sub(a, b):
    return([a[i] - b[i] for i in range(len(a))])

#the derivatives of T at x in every direction; grad(T)
def gradient(T, x):
    #take a baseline
    T0 = T(x)

    nVars = len(x)

    ds = [0 for i in range(nVars)]

    for i in range(nVars):
        xPlus = deepcopy(x)
        xPlus[i] += eps
        dTPlus = T(xPlus) - T0

        xMinus = deepcopy(x)
        xMinus[i] -= eps
        dTMinus = T(xMinus) - T0

        #print(dTPlus, dTMinus)

        #somehow
        if(dTPlus == dTMinus):
            ds[i] = 0
        #if over 10% off, T is too sharp
        elif(abs(2*(dTPlus + dTMinus)/(dTPlus - dTMinus)) > .1):
            ds[i] = 0
        else:
            ds[i] = (dTPlus - dTMinus)/(2*eps)

    return(ds)

def find1DMin(newT):
    global n_jumps
    phi = (1 + math.sqrt(5)) / 2
    # a  b c  d
    a = 0
    d = .01

    lastT = newT(0)
    while (newT(d) < lastT):
        lastT = newT(d)
        d *= 1.5

    b = a + (d - a) * (phi - 1) / phi
    c = d - (d - a) * (phi - 1) / phi

    Ta = newT(a)
    Tb = newT(b)
    Tc = newT(c)
    Td = newT(d)

    #do a golden section search
    while (abs(d - a) > eps):
        # print("----------------------------------------------")
        # print(a, b, c, d)
        # print(Ta, Tb, Tc, Td)

        if (Tc < Tb):
            a = b
            Ta = Tb

            b = c
            Tb = Tc

            c = d - (d - a) * (phi - 1) / phi
            Tc = newT(c)

        else:
            d = c
            Td = Tc

            c = b
            Tc = Tb

            b = a + (d - a) * (phi - 1) / phi
            Tb = newT(b)

    return((a + d)/2)

#find a local minimum of T(x), starting at x0, descending until a minimum is reached
#T is the function to minimize; x is a vector that is its input
def minimizeFrom(T, x0):
    nVars = len(x0)

    #print(str(nVars) + " variables")

    x = x0

    dToMove = []

    def newT(t):
        newX = [x[i] + t*dToMove[i] for i in range(nVars)]
        return T(newX)

    while(True):
        dT_dx = gradient(T, x)
        mag_dT_dx = mag(dT_dx)

        #if the derivative's zero, there's no direction to go
        if(mag_dT_dx == 0):
            return(x)

        dToMove = [-g / mag_dT_dx for g in dT_dx]

        t = find1DMin(newT)
        newX = [x[i] + t * dToMove[i] for i in range(nVars)]

        #print("now at " + str(newX))

        if(mag(sub(x, newX)) < eps):
            return(newX)

        x = newX

def minimize(T, xAvg, xV, N, lastMinX=None):
    bestX = xAvg
    bestT = T(xAvg)

    if(lastMinX != None):
        xLM = minimizeFrom(T, lastMinX)
        TLM = T(xLM)
        if(TLM < bestT):
            bestT = TLM
            bestX = xLM

    for i in range(N):
        x1_0 = [xAvg[i] + 2*(random() - .5)*xV[i] for i in range(len(xAvg))]
        x1 = minimizeFrom(T, x1_0)
        T1 = T(x1)


        if(T1 < bestT):
            bestX = x1
            bestT = T1

        x2_0 = sub(xAvg, sub(x1, xAvg))
        x2 = minimizeFrom(T, x2_0)
        T2 = T(x2)

        if(T2 < bestT):
            bestX = x2
            bestT = T2

#        print(x1, T1)
#        print(x2, T2)

    return(bestX)

if(__name__ == '__main__'):
    a_s = 0
    lon_s = 0
    lat_s = 0
    
    lon_e = -.1
    lat_e = 5
    a_e = 0

    def T(x):
        lat = x[0]
        lon = x[1]
        return(time_estimator.total_time(lat_s, lon_s, a_s, lat, lon, lat_e, lon_e, wind_heading))
    
    
    dTotal = time_estimator.dist(lat_s, lon_s, lat_e, lon_e)/(111*1000.0)
    
    wind_heading = 30
    
    lastMin = [0, 0]
    
    print(T([1, 2]))
    
    print(minimize(T, [(lat_e + lat_s)/2, (lon_e + lon_s)/2], [dTotal/2, dTotal/2], 1, lastMinX=lastMin))


