# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 13:17:31 2018

@author: komal
"""

import numpy as np
from scipy import stats
np.random.seed(110) # for reproducible random results

# set parameters
red_mean = 3
red_std = 0.8
blue_mean = 7
blue_std = 1

# draw 40 samples from normal distributions with red/blue parameters
red = np.random.normal(red_mean, red_std, size=40)
blue = np.random.normal(blue_mean, blue_std, size=40)
both_colours = np.sort(np.concatenate((red, blue)))

#Since the colours are hidden from us, we will start the EM process
#Starting guesses are very critical because the EM Algorithm converges to
# a local maxima. Hence we can get different answers with different starting points
#One reasonably good guess would be to take the value from a different but less
#robust algorithm
# estimates for the mean
red_mean_guess = 2.1
blue_mean_guess = 6
# estimates for the standard deviation
red_std_guess = 1.5
blue_std_guess = 0.8

#These are pretty bad guesses
#To continue with EM and improve these guesses, we compute the likelihood
#of each data point (regardless of its secret colour) appearing under
#these guesses for the mean and standard deviation
#The variable both_colours holds each data point. The function stats.norm computes
#the probability of the point under a normal distribution with the given parameters:
for i in range(10):
    likelihood_of_red = stats.norm(red_mean_guess, red_std_guess).pdf(both_colours)
    likelihood_of_blue = stats.norm(blue_mean_guess, blue_std_guess).pdf(both_colours)
    #Normalize these weights so that they can total 1
    likelihood_total = likelihood_of_red + likelihood_of_blue
    red_weight = likelihood_of_red / likelihood_total
    blue_weight = likelihood_of_blue / likelihood_total

#With our current estimates and our newly-computed weights, we can now compute new,
#probably better, estimates for the parameters (step 4). We need a function for the
#mean and a function for the standard deviation:

def estimate_mean(data, weight):
    return np.sum(data * weight) / np.sum(weight)


def estimate_std(data, weight, mean):
    variance = np.sum(weight * (data - mean)**2) / np.sum(weight)
    return np.sqrt(variance)

# new estimates for standard deviation
blue_std_guess = estimate_std(both_colours, blue_weight, blue_mean_guess)
red_std_guess = estimate_std(both_colours, red_weight, red_mean_guess)

# new estimates for mean
red_mean_guess = estimate_mean(both_colours, red_weight)
blue_mean_guess = estimate_mean(both_colours, blue_weight)

#Lets print the model parameters (The means and the std deviation in our case)
print("red mean:", red_mean_guess, ":::::::::", "blue mean:", blue_mean_guess)
print("red std:", red_std_guess, ":::::::::", "blue std:", blue_std_guess)

#plot the data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

#The two Gaussian distributions
y = np.zeros(len(both_colours))
mured = red_mean_guess
sigmared = red_std_guess
x = np.linspace(mured - 2.5*sigmared, mured + 2.5*sigmared, 100)
plt.plot(x,mlab.normpdf(x, mured, sigmared))
mublue = blue_mean_guess
sigmablue = blue_std_guess
y = np.linspace(mublue - 2.5*sigmablue, mublue + 2.5*sigmablue, 100)
plt.plot(y,mlab.normpdf(y, mublue, sigmablue))

#The data points themselves
for i in range(len(both_colours)):
    plt.plot(both_colours[i],0,"bo")
plt.show()