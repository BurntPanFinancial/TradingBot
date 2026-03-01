# this program uses the functions and ui made before
# and using 3d maps creates a visual representarion of 
# of the option price whith varing volitility, and strike price 
# basicaly keeping the stock pric, time to expire, and intrest same 
# output the value of the option 

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
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
    # clear off the data 
    ax.clear()

    # convert all values in text to usable vars
    S = int (price_Input.get())
    T = int (time_Input.get())
    r = float (intrest_Input.get())

    # create the values for vol and strike
    x = np.linspace(0,2,100) # vol
    y = np.linspace(S//3,S//3 * 5,100) # strike

    sigma,K = np.meshgrid(x,y)

    #calculate price
    if (int(option_input.get()) == 1 ):
        price =  call_price(sigma, T, S, K, r, norm)
    else:
        price = put_price(sigma, T, S, K, r, norm)

    # graph and display
    ax.plot_surface (sigma,K,price, cmap = "twilight_shifted")
    graph_panal.draw()

    return


# creating the Gui 
frame = tk.Tk()
frame.title("Black Schol's option price 3D maper")
frame.geometry("800x600")

# creat the plot 
fig,ax = plt.subplots()
ax = plt.axes(projection = "3d")

# creaet ethe graph panals and add to the frame
graph_panal = FigureCanvasTkAgg(fig, master = frame)
graph_panal.get_tk_widget().place(relx=0.65, rely=0.4, anchor="center", width= 500, height= 500) 


# array to create the spacing
y_location = [0.3]
for i in range (7):
    y_location.append((i*0.06) + y_location[0])

# price lable
price_Input_LBL = tk.Label(frame, text="Stock price ($)", font=("Arial", 13))
price_Input_LBL.place(relx=0.05, rely=y_location[1], anchor="nw", width=160) 

# text box for price
price_Input = tk.Entry(frame, width=30)
price_Input.place(relx=0.08, rely=y_location[2], anchor="nw", width=160)  

# time  lable
time_Input_LBL = tk.Label(frame, text="Time to close (years)", font=("Arial", 13))
time_Input_LBL.place(relx=0.05, rely=y_location[3], anchor="nw", width=200)  

# text box for  time til expiry 
time_Input = tk.Entry(frame, width=30)
time_Input.place(relx=0.08, rely=y_location[4], anchor="nw", width=160) 

# intrest  lable
intrest_Input_LBL = tk.Label(frame, text="Intrest (EX: 0.45)", font=("Arial", 13))
intrest_Input_LBL.place(relx=0.05, rely=y_location[5], anchor="nw", width=160)  

# text box for intrest 
intrest_Input = tk.Entry(frame, width=30)
intrest_Input.place(relx=0.08, rely=y_location[6], anchor="nw", width=160) 

# put or call option selector
# Radiobutton (radio buttons)
option_input = tk.StringVar(value="CALL") #initalise the value to CALL
option1 = tk.Radiobutton(frame, text="CALL", variable=option_input, value=1)
option2 = tk.Radiobutton(frame, text="PUT", variable=option_input, value=0)
option1.place(relx=0.2, rely=y_location[7]+0.2, anchor="n", width=150)  
option2.place(relx=0.8, rely=y_location[7]+0.2, anchor="n", width=150) 

# update button
update_BTN = tk.Button(frame, text="Update", command= updateBTN_Press, bg="white", fg="black")
update_BTN.place(relx=0.5, rely=y_location[7]+0.2, anchor="n", width=70)  

# run the frame
frame.mainloop()
