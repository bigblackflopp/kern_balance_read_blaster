import serial
import time
import datetime
from collections import deque
import matplotlib.pyplot as plt

a = serial.Serial(baudrate=9600, port = "COM5", parity=None, stopbits=1)

lista = open(f"weight_values_{datetime.datetime.today()}.txt")

def live_plot(value, max_samples=300, title="Live data", pause=0.001):
    """Append `value` and redraw a rolling plot of the last `max_samples` samples."""
    s = live_plot.__dict__  # state stored on the function itself, no globals needed

    # First call (or window was closed): set everything up
    if "fig" not in s or not plt.fignum_exists(s["fig"].number):
        plt.ion()
        s["data"] = deque(maxlen=max_samples)   # old samples drop off automatically
        s["n"] = 0                              # total samples seen so far
        s["fig"], s["ax"] = plt.subplots()
        s["line"], = s["ax"].plot([], [])
        s["ax"].set_title(title)
        s["ax"].set_xlabel("Sample")

    s["data"].append(value)
    s["n"] += 1
    n, data, ax = s["n"], s["data"], s["ax"]

    s["line"].set_data(range(n - len(data), n), data)
    ax.set_xlim(max(0, n - max_samples), max(n, max_samples))  # scrolling window
    ax.relim()
    ax.autoscale_view(scalex=False)                            # auto-fit y only
    s["fig"].canvas.draw_idle()
    plt.pause(pause)  

while(1):
    
    a.write("SI") #tutaj komenda do odczytywania wagi
    readout = a.read(128)
    print(readout)
    lista.write(readout)
    live_plot(readout)
    time.sleep(1000)
    
    
     
