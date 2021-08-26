'''
A collection of distributions

normalDistribution()
logNormalDistribution()

'''

import numpy as np
import math

def normalDistribution(mean, standardDeviation, lowerBound = -math.inf, upperBound = math.inf):
    '''
    Returns a random scalar value on the normal distribution.

    mean: int or float that is center of distribution
    standardDeviation: int or float that is "width" of distribution
    lowerBound (optional): a constaint on the lowest value that can be returned
    upperBound (optional): a constaint on the highest value that can be returned
    
    The domain is (-inf, +inf), which may not be ideal for laboratory values unless
    lowerBound and upperBound are used.'''
    return min(upperBound,max(np.random.normal(mean, standardDeviation),lowerBound))

def logNormalDistribution(lnMean, lnStandardDeviation):
    '''
    Returns a random scalar value on the lognormal distribution.

    lnMean: int or float that represents the natural log of the mean/expected value
    lnStandardDeviation: int or float that is the natural log of the standard deviation
    
    The domain is (0, +inf), which may be more ideal for laboratory values.'''
    return np.random.normal(mean, standard_deviation)

if __name__ == "__main__":
    # Test, should give normally-distibuted numbers between 3.5 and 5.0
    print(normalDistribution(4,1,3.5,5.0))
