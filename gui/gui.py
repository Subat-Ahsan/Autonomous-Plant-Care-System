import tkinter as tk
import serial 
from tkinter import ttk
from tkinter import PhotoImage

def getData(ser):
    ser.write(";".encode())

    fin = b''
    data = ser.read(1)
    while (data):
        fin += data
        data = ser.read(1)
    try:
        s = fin.decode("ascii") 
    except:
        return "Error"
        
    return s
   
    
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Plant Tracker")
        self.root.geometry(f"{9*45}x{16*45}")
        self.root.resizable(False, False)
            
        self.data_dict = {"Temperature": "N/A", "Moisture": "N/A", "Humidity": "N/A",
        "Pressure": "N/A"}
            
        self.data_string = ""
        
        self.ser = serial.Serial("Com4", 9600, timeout = 2) 
        self.row_frame = tk.Frame(self.root, bg="lightblue")
        self.row_frame.pack(side=tk.TOP, fill=tk.X)

        self.title_label = tk.Label(self.row_frame, text="Plant Tracker", font=("Helvetica", 24), bg="lightblue")
        self.title_label.grid(row=0, column=0, columnspan = 2, padx=10, pady=10, sticky=tk.W)
        
        self.button = tk.Button(self.row_frame, text="R", compound=tk.LEFT, command=self.update_data, font=("Helvetica", 24))
        self.button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E)
        
        self.row_frame.columnconfigure(0, weight=1)  
        self.row_frame.columnconfigure(2, weight=0)   
        
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(side=tk.TOP,fill=tk.X)
            
        self.info_frame = tk.Frame(self.data_frame)
        self.info_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.info_label = tk.Label(self.info_frame, text="Information", font=("Helvetica", 16, "underline"))
        self.info_label.pack(side=tk.TOP,pady=10)
        
        self.temp_label = tk.Label(self.info_frame, text="Temperature: ", font=("Helvetica", 16))
        self.temp_label.pack(side=tk.TOP,pady=10)
        
        self.humidity_label = tk.Label(self.info_frame, text="Humidity: ", font=("Helvetica", 16))
        self.humidity_label.pack(side=tk.TOP,pady=10)
        
        self.pressure_label = tk.Label(self.info_frame, text="Pressure: ", font=("Helvetica", 16))
        self.pressure_label.pack(side=tk.TOP,pady=10)
        
        self.moist_label = tk.Label(self.info_frame, text="Moisture: ", font=("Helvetica", 16))
        self.moist_label.pack(side=tk.TOP,pady=10)
        
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("Custom.Horizontal.TProgressbar", background="blue")
        
        self.moist_bar = ttk.Progressbar(self.info_frame, style="Custom.Horizontal.TProgressbar", 
        orient="horizontal", length=300, mode="determinate")
        self.moist_bar.pack(side=tk.TOP,pady=10)

        self.update_data()
        
        self.m_pick_frame = tk.Frame(self.root)
        self.m_pick_frame.pack(side=tk.TOP,fill=tk.X, pady=25)
        
        self.m_min_select = tk.Spinbox(self.m_pick_frame, from_=0, to=1023)
        self.m_max_select = tk.Spinbox(self.m_pick_frame, from_=0, to=1023)
        self.m_submit_select = tk.Button(self.m_pick_frame, text="Submit", command=self.send_limits, font=("Helvetica", 12))
        
        desc2_text = "Use these inputs to calibrate the automatic watering system. If the moisture sensor value is less than the minimum(left) it will not water the plants. If it is more than the maximum(right) it will." 
        self.m_desc = tk.Label(self.m_pick_frame, text="Pick numbers between [0,1023]", font=("Helvetica", 16, "underline"))
        self.m_desc2 = tk.Label(self.m_pick_frame, text=desc2_text, font=("Helvetica", 12), wraplength=400)
        
        self.m_desc2.pack(side=tk.BOTTOM)
        self.m_desc.pack(side=tk.TOP)
        self.m_min_select.pack(side=tk.LEFT, padx=10)
        self.m_max_select.pack(side=tk.LEFT, padx=10)
        self.m_submit_select.pack(side=tk.LEFT, padx=10)
        
        
        self.image = PhotoImage(file="pink.png")
        self.image_label = tk.Label(self.root, image=self.image)
        self.image_label.pack(side=tk.BOTTOM)
        self.root.mainloop()
        
        

    def on_button_click(self):
        print("Button clicked!")
        
    def send_limits(self):
        try:
        
            self.ser.write("%".encode())
        except:
            return
        s = (4-len(self.m_min_select.get())) * '0' + self.m_min_select.get() + (4-len(self.m_max_select.get())) * '0' + self.m_max_select.get()
        print(s)
        self.ser.write(s.encode())
        
    def update_data(self):
        print("Called update data")
        self.data_string = getData(self.ser)
        
        try:
            print(self.data_string)
            lines = self.data_string.split("\n")
        
            self.data_dict["Temperature"] = lines[2].split(":")[1].strip()
            self.data_dict["Moisture"] = lines[1].split(":")[1].strip()
            self.data_dict["Humidity"] = lines[3].split(":")[1].strip()
            self.data_dict["Pressure"] = lines[4].split(":")[1].strip()
        except:
            print("Error extracting")
            return
        
        self.temp_label.config(text=f"Temperature: {self.data_dict['Temperature']} celsius")
        self.humidity_label.config(text=f"Humidity: {self.data_dict['Humidity']} %rH")
        self.pressure_label.config(text=f"Pressure: {self.data_dict['Pressure']} pa")
        
        positive_m_value = 1023 - int(self.data_dict["Moisture"])
        print(positive_m_value)
        if (positive_m_value >= 823):
            normal_m_value = 99.9 
        else:
            normal_m_value = (positive_m_value) * (100 / 823)
        print(normal_m_value)
        self.moist_label.config(text=f"Moisture: {round(normal_m_value,2)} %")
        self.moist_bar["value"] = normal_m_value
myApp = GUI()
