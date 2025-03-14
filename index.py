import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        type TEXT,
                        fuel_type TEXT,
                        fuel_consumption REAL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS fuel_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vehicle_id INTEGER,
                        fuel_added REAL,
                        km_possible REAL,
                        FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS service_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vehicle_id INTEGER,
                        service_type TEXT,
                        service_date TEXT,
                        cost REAL,
                        FOREIGN KEY(vehicle_id) REFERENCES vehicles(id))''')
    
    conn.commit()
    conn.close()

# Function to add vehicle
def add_vehicle():
    name = entry_name.get()
    v_type = entry_type.get()
    fuel_type = entry_fuel_type.get()
    fuel_consumption = entry_fuel_consumption.get()
    
    if not name or not fuel_consumption:
        messagebox.showerror("Error", "Vehicle Name and Fuel Consumption are required")
        return
    
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (name, type, fuel_type, fuel_consumption) VALUES (?, ?, ?, ?)", 
                   (name, v_type, fuel_type, float(fuel_consumption)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Vehicle added successfully")

# Function to add service record
def add_service():
    vehicle_id = entry_service_vehicle_id.get()
    service_type = entry_service_type.get()
    service_date = entry_service_date.get()
    cost = entry_service_cost.get()
    
    if not vehicle_id or not service_type or not service_date or not cost:
        messagebox.showerror("Error", "All fields are required")
        return
    
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service_records (vehicle_id, service_type, service_date, cost) VALUES (?, ?, ?, ?)", 
                   (vehicle_id, service_type, service_date, float(cost)))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Service record added successfully")
    
# Function to calculate possible distance based on fuel added
def calculate_distance():
    vehicle_id = entry_vehicle_id.get()
    fuel_added = entry_fuel_added.get()
    
    if not vehicle_id or not fuel_added:
        messagebox.showerror("Error", "Vehicle ID and Fuel Added are required")
        return
    
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fuel_consumption FROM vehicles WHERE id = ?", (vehicle_id,))
    result = cursor.fetchone()
    
    if result:
        fuel_consumption = result[0]
        km_possible = float(fuel_added) / fuel_consumption
        cursor.execute("INSERT INTO fuel_records (vehicle_id, fuel_added, km_possible) VALUES (?, ?, ?)",
                       (vehicle_id, float(fuel_added), km_possible))
        conn.commit()
        messagebox.showinfo("Result", f"The vehicle can travel approximately {km_possible:.2f} Km.")
    else:
        messagebox.showerror("Error", "Vehicle not found")
    
    conn.close()


# Function to view service history for a specific vehicle
def view_service_history():
    vehicle_id = entry_service_history_vehicle_id.get()
    
    if not vehicle_id:
        messagebox.showerror("Error", "Please provide a Vehicle ID")
        return
    
    conn = sqlite3.connect("vehicles.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT service_type, service_date, cost FROM service_records WHERE vehicle_id = ?", (vehicle_id,))
    results = cursor.fetchall()
    
    if results:
        service_history_text.delete(1.0, tk.END)  # Clear previous results
        for record in results:
            service_history_text.insert(tk.END, f"Service Type: {record[0]}\nService Date: {record[1]}\nCost: {record[2]}\n\n")
    else:
        messagebox.showinfo("No Record", "No service history found for this vehicle.")
    
    conn.close()


# Initialize the database
init_db()

# Create the GUI
root = tk.Tk()
root.title("Vehicle Management System")
root.geometry("500x600")
root.configure(bg="#2C3E50")

style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#1ABC9C")
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 10, "bold"))

# Vehicle Input (Add Vehicle)
frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=10)
ttk.Label(frame, text="Vehicle Name:").grid(row=0, column=0)
entry_name = ttk.Entry(frame)
entry_name.grid(row=0, column=1)
ttk.Label(frame, text="Vehicle Type:").grid(row=1, column=0)
entry_type = ttk.Entry(frame)
entry_type.grid(row=1, column=1)
ttk.Label(frame, text="Fuel Type:").grid(row=2, column=0)
entry_fuel_type = ttk.Entry(frame)
entry_fuel_type.grid(row=2, column=1)
ttk.Label(frame, text="Fuel Consumption (L/Km):").grid(row=3, column=0)
entry_fuel_consumption = ttk.Entry(frame)
entry_fuel_consumption.grid(row=3, column=1)
ttk.Button(frame, text="Add Vehicle", command=add_vehicle).grid(row=4, columnspan=2, pady=5)

# Fuel Input (Add Fuel Record)
frame2 = tk.Frame(root, bg="#2C3E50")
frame2.pack(pady=10)
ttk.Label(frame2, text="Vehicle ID:").grid(row=0, column=0)
entry_vehicle_id = ttk.Entry(frame2)
entry_vehicle_id.grid(row=0, column=1)
ttk.Label(frame2, text="Fuel Added (L):").grid(row=1, column=0)
entry_fuel_added = ttk.Entry(frame2)
entry_fuel_added.grid(row=1, column=1)
ttk.Button(frame2, text="Calculate Distance", command=calculate_distance).grid(row=2, columnspan=2, pady=5)

# Service Input (Add Service)
frame_service = tk.Frame(root, bg="#2C3E50")
frame_service.pack(pady=10)
ttk.Label(frame_service, text="Vehicle ID:").grid(row=0, column=0)
entry_service_vehicle_id = ttk.Entry(frame_service)
entry_service_vehicle_id.grid(row=0, column=1)
ttk.Label(frame_service, text="Service Type:").grid(row=1, column=0)
entry_service_type = ttk.Entry(frame_service)
entry_service_type.grid(row=1, column=1)
ttk.Label(frame_service, text="Service Date (YYYY-MM-DD):").grid(row=2, column=0)
entry_service_date = ttk.Entry(frame_service)
entry_service_date.grid(row=2, column=1)
ttk.Label(frame_service, text="Service Cost:").grid(row=3, column=0)
entry_service_cost = ttk.Entry(frame_service)
entry_service_cost.grid(row=3, column=1)
ttk.Button(frame_service, text="Add Service", command=add_service).grid(row=4, columnspan=2, pady=5)

# View Service History
frame_service_history = tk.Frame(root, bg="#2C3E50")
frame_service_history.pack(pady=10)
ttk.Label(frame_service_history, text="Vehicle ID:").grid(row=0, column=0)
entry_service_history_vehicle_id = ttk.Entry(frame_service_history)
entry_service_history_vehicle_id.grid(row=0, column=1)
ttk.Button(frame_service_history, text="View Service History", command=view_service_history).grid(row=1, columnspan=2, pady=5)

# Service History Display (Text Box)
service_history_text = tk.Text(root, height=10, width=40)
service_history_text.pack(pady=10)

root.mainloop()
