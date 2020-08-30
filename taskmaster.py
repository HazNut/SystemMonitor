# A simple GUI application to show various system statistics.

import tkinter as tk
import psutil


# Callback function to update the CPU usage. Calls after() again so that it is repeatedly updated.
def update_vars(values, window):
    values[0].set("CPU usage: " + str(psutil.cpu_percent()))
    values[1].set("RAM usage: " + str(psutil.virtual_memory()[2]))

    values[2].delete(0, tk.END)
    for i in psutil.pids():
        values[2].insert(tk.END, psutil.Process(i).name())

    window.after(1000, update_vars, values, window)


def main():
    # Set up the window.
    window = tk.Tk()
    window.title("System Monitor")
    window.minsize(300, 300)
    window.maxsize(300, 300)

    values = []

    # The CPU usage is stored in a StringVar, so when it is updated, the label using it is also updated.
    cpu_usage = tk.StringVar()
    cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()))
    cpu_usage_label = tk.Label(textvariable=cpu_usage, padx = 5)
    cpu_usage_label.pack(anchor=tk.W)
    values.append(cpu_usage)

    # % RAM used.
    ram_usage = tk.StringVar()
    ram_usage.set("RAM usage: " + str(psutil.virtual_memory()[2]))
    ram_usage_label = tk.Label(textvariable=ram_usage, padx = 5)
    ram_usage_label.pack(anchor=tk.W)
    values.append(ram_usage)

    # Sets up the list of processes and the scrollbar to scroll it with.
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox = tk.Listbox(window, yscrollcommand=scrollbar.set)
    for i in psutil.pids():
        listbox.insert(tk.END, psutil.Process(i).name())
    listbox.pack(anchor=tk.W, fill=tk.BOTH, expand=True, padx = (5, 0), pady = (0, 5))
    scrollbar.config(command=listbox.yview)
    values.append(listbox)

    # The CPU and RAM usage is updated after a second has elapsed. The update function calls it again, so it
    # repeatedly updates.
    window.after(1000, update_vars, values, window)

    window.mainloop()


if __name__ == "__main__":
    main()
