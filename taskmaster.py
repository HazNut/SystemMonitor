# A simple GUI application to view CPU and RAM usage, and view running processes.

import tkinter as tk
import tkinter.ttk as ttk
import psutil


# Callback function to update the CPU and RAM usage, as well as the list of processes. Calls after() again so that it is
# repeatedly updated.
def update_vars(values, window):
    # Set the CPU and RAM usage labels.
    values[0].set("CPU usage: " + str(psutil.cpu_percent()) + "%")
    values[1].set("RAM usage: " + str(psutil.virtual_memory()[2]) + "%")

    # Get pids currently in treeview.
    treeview_pids = []
    for child in values[2].get_children():
        treeview_pids.append(values[2].item(child)["values"][1])

    # Add any processes to the treeview if they are not already in it.
    for pid in psutil.pids():
        if pid not in treeview_pids:
            values[2].insert("", "end", values=(psutil.Process(pid).name(), pid))

    # Delete processes from the treeview if they are no longer running.
    for pid in treeview_pids:
        if not psutil.pid_exists(pid):
            for child in values[2].get_children():
                if values[2].item(child)["values"][1] == pid:
                    values[2].delete(child)

    # Runs the callback function again after a second.
    window.after(1000, update_vars, values, window)


def main():
    # Set up the window.
    window = tk.Tk()
    window.title("TaskMaster")
    window.minsize(300, 300)
    window.maxsize(300, 300)

    values = []

    # The CPU usage is stored in a StringVar, so when it is updated, the label using it is also updated.
    cpu_usage = tk.StringVar()
    cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()) + "%")
    cpu_usage_label = tk.Label(textvariable=cpu_usage, padx=5)
    cpu_usage_label.pack(anchor=tk.W)
    values.append(cpu_usage)

    # % RAM used.
    ram_usage = tk.StringVar()
    ram_usage.set("RAM usage: " + str(psutil.virtual_memory()[2]) + "%")
    ram_usage_label = tk.Label(textvariable=ram_usage, padx=5)
    ram_usage_label.pack(anchor=tk.W)
    values.append(ram_usage)

    # Sets up the list of processes and the scrollbar to scroll it with.
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree = ttk.Treeview(window, columns=("Name", "PID"), show="headings", yscrollcommand=scrollbar.set)
    tree.heading("#1", text="Name", anchor=tk.W)
    tree.heading("#2", text="PID", anchor=tk.W)
    tree.column("#1", width=200)
    tree.column("#2", width=100)
    tree.pack(anchor=tk.W, fill=tk.BOTH, expand=True, padx=(5, 0), pady=(0, 5))
    scrollbar.config(command=tree.yview)
    for i in psutil.pids():
        tree.insert("", "end", values=(psutil.Process(i).name(), i))
    values.append(tree)

    # The CPU and RAM usage is updated after a second has elapsed. The update function calls it again, so it repeatedly
    # updates.
    window.after(1000, update_vars, values, window)

    window.mainloop()


if __name__ == "__main__":
    main()
