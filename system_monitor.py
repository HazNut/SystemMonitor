# A simple GUI application to show various system statistics.

import tkinter as tk
import psutil


# Callback function to update the CPU usage. Calls after() again so that it is repeatedly updated.
def update_cpu_usage(cpu_usage, window):
    cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()))
    window.after(1000, update_cpu_usage, cpu_usage, window)


def main():
    # Set up the window.
    window = tk.Tk()
    window.title("System Monitor")
    window.minsize(300, 300)

    # The CPU usage is stored in a StringVar, so when it is updated, the label using it is also updated.
    cpu_usage = tk.StringVar()
    cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()))
    label = tk.Label(textvariable=cpu_usage)
    label.pack(anchor=tk.W)

    # The CPU usage is updated after a second has elapsed. The update function calls it again, so it
    # repeatedly updates.
    window.after(1000, update_cpu_usage, cpu_usage, window)

    window.mainloop()


if __name__ == "__main__":
    main()
