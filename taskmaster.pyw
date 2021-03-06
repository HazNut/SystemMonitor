# A simple GUI application to view CPU and RAM usage, and view running processes.

import bisect
import tkinter as tk
import tkinter.ttk as ttk
import psutil


class GUI:

    # Initialise and run the GUI.
    # cpu_usage, ram_usage and treeview are set as instance attributes as they need to be updated.
    # Other GUI elements are just left as locals, as they do not need to be accessed after the window setup.
    def __init__(self):
        # Set up the window.
        self.window = tk.Tk()
        self.window.title("TaskMaster")
        self.window.geometry("300x300")
        self.window.resizable(False, False)
        self.sorting_mode = "pid"

        # The CPU usage is stored in a StringVar, so when it is updated, the label using it is also updated.
        self.cpu_usage = tk.StringVar()
        self.cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()) + "%")
        cpu_usage_label = tk.Label(textvariable=self.cpu_usage, padx=5)
        cpu_usage_label.pack(anchor=tk.W)

        # Percentage of RAM used.
        self.ram_usage = tk.StringVar()
        self.ram_usage.set("RAM usage: " + str(psutil.virtual_memory()[2]) + "%")
        ram_usage_label = tk.Label(textvariable=self.ram_usage, padx=5)
        ram_usage_label.pack(anchor=tk.W)

        frame = tk.Frame(self.window)
        frame.pack()
        # Sets up the list of processes in a Treeview, and the scrollbar to scroll it with.
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview = ttk.Treeview(frame, columns=("Name", "PID"), show="headings", selectmode="browse",
                                     yscrollcommand=scrollbar.set)
        self.treeview.heading("#1", text="Name", anchor=tk.W)
        self.treeview.heading("#2", text="PID", anchor=tk.W)
        self.treeview.column("#1", width=200)
        self.treeview.column("#2", width=100)
        self.treeview.bind("<Button-1>", self.handle_treeview_click)
        self.treeview.pack(anchor=tk.W, fill=tk.BOTH, expand=True, padx=(5, 0))
        scrollbar.config(command=self.treeview.yview)
        for i in psutil.pids():
            self.treeview.insert("", "end", values=(psutil.Process(i).name(), i))

        # This button allows the user to end a selected process.
        end_button = tk.Button(text="End process", command=self.end_process)
        end_button.pack(side=tk.LEFT, padx=(5, 0), pady=(5, 5))

        self.window.after(1000, lambda: self.update())
        self.window.mainloop()

    # Callback function to update usages and the process list. Runs itself again after a second.
    def update(self):
        # Set the CPU and RAM usage labels.
        self.cpu_usage.set("CPU usage: " + str(psutil.cpu_percent()) + "%")
        self.ram_usage.set("RAM usage: " + str(psutil.virtual_memory()[2]) + "%")

        # Get pids currently in treeview.
        treeview_pids = []
        treeview_names = []
        for child in self.treeview.get_children():
            treeview_names.append(self.treeview.item(child)["values"][0].lower())
            treeview_pids.append(self.treeview.item(child)["values"][1])

        treeview_names.sort(key=lambda process: process.lower())
        treeview_pids.sort()

        # Add any processes to the treeview if they are not already in it.
        for system_pid in psutil.pids():
            if system_pid not in treeview_pids:
                if self.sorting_mode == "name":
                    self.treeview.insert("", bisect.bisect(treeview_names, psutil.Process(system_pid).name().lower()),
                                         values=(psutil.Process(system_pid).name(), system_pid))
                elif self.sorting_mode == "pid":
                    self.treeview.insert("", bisect.bisect(treeview_pids, system_pid),
                                         values=(psutil.Process(system_pid).name(), system_pid))

        # Delete processes from the treeview if they are no longer running.
        for treeview_pid in treeview_pids:
            if not psutil.pid_exists(treeview_pid):
                for child in self.treeview.get_children():
                    if self.treeview.item(child)["values"][1] == treeview_pid:
                        self.treeview.delete(child)

        self.window.after(1000, self.update)

    # Function called when the 'end process' button is clicked - terminates the selected process.
    def end_process(self):
        if self.treeview.selection():
            process_to_end = self.treeview.selection()[0]
            pid = self.treeview.item(process_to_end)["values"][1]
            psutil.Process(pid).terminate()

    # If the user clicks on the treeview, check if they clicked on a column header. If they clicked on one, sort by that
    # column.
    def handle_treeview_click(self, event):
        if self.treeview.identify_region(event.x, event.y) == "heading":
            column = self.treeview.identify_column(event.x)
            if column == "#1":
                self.sort_treeview("name")
                self.sorting_mode = "name"
            elif column == "#2":
                self.sort_treeview("pid")
                self.sorting_mode = "pid"

    # Sort the treeview by a given key (name or PID).
    def sort_treeview(self, key):
        processes = []

        if key == "name":
            for child in self.treeview.get_children():
                processes.append((child, self.treeview.item(child)["values"][0]))
            processes.sort(key=lambda process: process[1].lower())
        elif key == "pid":
            for child in self.treeview.get_children():
                processes.append((child, self.treeview.item(child)["values"][1]))
            processes.sort(key=lambda process: process[1])

        for i, process in enumerate(processes):
            self.treeview.move(process[0], parent="", index=i)


if __name__ == "__main__":
    gui = GUI()
