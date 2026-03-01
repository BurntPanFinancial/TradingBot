# this program uses the black scholes call option pricer
# it takes some arbritaray inputs of a theoratical stock and 
# shows the value of the stock and graphes it's heat map 
# based on volitility 

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


# S: Current stock price (spot price)
# K: Strike price of the option
# T: Time to expiration (expressed in years)
# r: Risk-free interest rate (annualized decimal)
# (sigma): Volatility of the underlying asset
# n: is the wnormal distabution equation we will import this

def call_price (sigma, T, S, K, r, norm):
# Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Call Option Price Equation
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)



def put_price (sigma, T, S, K, r, norm):
# Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Put Option Price Equation
    return  K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


# promt user for values
choice = input ("Enter P for put option and C for call option : ")
S = float (input ("enter the current stock price : "))
K = float (input ("enter the strike price : "))
T = float (input ("enter time to expiration in years : "))
r = float (input ("Risk-free interest rate : "))
sigma = float (input ("Volatility of the underlying asset : "))


if(input == "P"):
    print("Put option price is: ", put_price (sigma, T, S, K, r, norm))
else:
    print("Call option price is: ",call_price (sigma, T, S, K, norm))