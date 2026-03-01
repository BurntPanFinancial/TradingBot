# this program uses the functions created before and displayes them 
# using a ui using t kinter 

import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from scipy.stats import norm

# func to caluclate call price
def call_price (sigma, T, S, K, r, norm):
# Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Call Option Price Equation
    return np.round (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))

# func to caluclate put price
def put_price (sigma, T, S, K, r, norm):
# Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Put Option Price Equation
    return  np.round (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))

#func for when the update btn is pressed 
def updateBTN_Press ():
    # convert all values in text to usable vars
    S = int (price_Input.get())
    K = int (strike_price_Input.get())
    T = int (time_Input.get())
    r = float (intrest_Input.get())
    sigma = float (vol_Input.get())

    # displat the asnwer
    if (int(option_input.get()) == 1 ):
        answer.config(text = call_price(sigma, T, S, K, r, norm))
    else:
        answer.config(text = put_price(sigma, T, S, K, r, norm))

    return

# creating the Gui 
frame = tk.Tk()
frame.title("Black Schol's option price calculator")
frame.geometry("300x400")

# title
title = tk.Label(frame, text="Option Price", font=("Arial", 14))
title.place(relx=0.5, rely=0.05, anchor="center", width=150)  # place relative to the window

# output lable
answer = tk.Label(frame, text="$0", font=("Arial", 35))
answer.place(relx=0.5, rely=0.2, anchor="center", width=300)  # place relative to the window

# price lable
price_Input_LBL = tk.Label(frame, text="Stock price ($)", font=("Arial", 13))
price_Input_LBL.place(relx=0.0, rely=0.3, anchor="nw", width=150)  # place relative to the window

# text box for price
price_Input = tk.Entry(frame, width=30)
price_Input.place(relx=0.6, rely=0.3, anchor="nw", width=100)  # place relative to the window

# strike price lable
strike_price_Input_LBL = tk.Label(frame, text="Strike price ($)", font=("Arial", 13))
strike_price_Input_LBL.place(relx=0.0, rely=0.37, anchor="nw", width=150)  # place relative to the window

# text box for strike price
strike_price_Input = tk.Entry(frame, width=30)
strike_price_Input.place(relx=0.6, rely=0.37, anchor="nw", width=100)  # place relative to the window

# time  lable
time_Input_LBL = tk.Label(frame, text="Time to close (years)", font=("Arial", 13))
time_Input_LBL.place(relx=0.05, rely=0.44, anchor="nw", width=155)  # place relative to the window

# text box for  time til expiry 
time_Input = tk.Entry(frame, width=30)
time_Input.place(relx=0.6, rely=0.44, anchor="nw", width=100) 

# volitilety  (sigma) lable
vol_Input_LBL = tk.Label(frame, text="Volitility (EX: 0.45)", font=("Arial", 13))
vol_Input_LBL.place(relx=0.03, rely=0.51, anchor="nw", width=150)  # place relative to the window

# text box for volitiluty 
vol_Input = tk.Entry(frame, width=30)
vol_Input.place(relx=0.6, rely=0.51, anchor="nw", width=100) 

# intrest  lable
intrest_Input_LBL = tk.Label(frame, text="Intrest (EX: 0.45)", font=("Arial", 13))
intrest_Input_LBL.place(relx=0.02, rely=0.58, anchor="nw", width=150)  # place relative to the window

# text box for volitiluty 
intrest_Input = tk.Entry(frame, width=30)
intrest_Input.place(relx=0.6, rely=0.58, anchor="nw", width=100) 

# put or call option selector
# Radiobutton (radio buttons)
option_input = tk.StringVar(value="CALL") #initalise the value to CALL
option1 = tk.Radiobutton(frame, text="CALL", variable=option_input, value=1)
option2 = tk.Radiobutton(frame, text="PUT", variable=option_input, value=0)
option1.place(relx=0.2, rely=0.8, anchor="s", width=150)  # place relative to the window
option2.place(relx=0.8, rely=0.8, anchor="s", width=150)  # place relative to the window

# update button
update_BTN = tk.Button(frame, text="Update", command= updateBTN_Press, bg="white", fg="black")
update_BTN.place(relx=0.5, rely=0.8, anchor="s", width=50)  # place relative to the window

# run the frame
frame.mainloop()
