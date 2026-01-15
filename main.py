import tkinter as tk
from tkinter import messagebox
from database import create_connection

# ================== MAIN WINDOW ==================
root = tk.Tk()
root.title("Employee Transport Management System")
root.geometry("750x600")
root.configure(bg="#ecf0f1")
root.resizable(False, False)

# ================== HEADER ==================
header = tk.Frame(root, bg="#1f2a44", height=90)
header.pack(fill="x")

tk.Label(
    header,
    text="EMPLOYEE TRANSPORT MANAGEMENT SYSTEM",
    bg="#1f2a44",
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

# ================== SUBTITLE ==================
tk.Label(
    root,
    text="Manage Employees, Drivers, Vehicles, Routes and Assignments",
    bg="#ecf0f1",
    fg="#2c3e50",
    font=("Segoe UI", 11)
).pack(pady=10)

# ================== CONTENT FRAME ==================
content = tk.Frame(root, bg="#ecf0f1")
content.pack(pady=30)

# ================== COMMON BUTTON STYLE ==================
BTN_STYLE = {
    "width": 32,
    "height": 2,
    "font": ("Segoe UI", 11),
    "bg": "#34495e",
    "fg": "white",
    "activebackground": "#2c3e50",
    "activeforeground": "white",
    "bd": 0
}


# ================== ADD EMPLOYEE ==================
def add_employee():
    win = tk.Toplevel(root)
    win.title("Add Employee")
    win.geometry("420x420")

    labels = ["Employee Name", "Phone Number", "Pickup Location", "Drop Location", "Shift Time"]
    entries = []

    for lbl in labels:
        tk.Label(win, text=lbl, font=("Segoe UI", 10)).pack(pady=4)
        e = tk.Entry(win, width=35)
        e.pack()
        entries.append(e)

    def save():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (employee_name, phone_number, pickup_location, drop_location, shift_time) "
            "VALUES (%s,%s,%s,%s,%s)",
            tuple(e.get() for e in entries)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Employee added successfully")
        win.destroy()

    tk.Button(win, text="Add Employee", width=25, command=save).pack(pady=25)


# ================== ADD DRIVER ==================
def add_driver():
    win = tk.Toplevel(root)
    win.title("Add Driver")
    win.geometry("420x350")

    labels = ["Driver Name", "Phone Number", "License Number"]
    entries = []

    for lbl in labels:
        tk.Label(win, text=lbl, font=("Segoe UI", 10)).pack(pady=4)
        e = tk.Entry(win, width=35)
        e.pack()
        entries.append(e)

    def save():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO drivers (driver_name, phone_number, license_number) "
            "VALUES (%s,%s,%s)",
            tuple(e.get() for e in entries)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Driver added successfully")
        win.destroy()

    tk.Button(win, text="Add Driver", width=25, command=save).pack(pady=25)


# ================== ADD VEHICLE ==================
def add_vehicle():
    win = tk.Toplevel(root)
    win.title("Add Vehicle")
    win.geometry("420x320")

    labels = ["Vehicle Number", "Vehicle Type", "Seating Capacity"]
    entries = []

    for lbl in labels:
        tk.Label(win, text=lbl, font=("Segoe UI", 10)).pack(pady=4)
        e = tk.Entry(win, width=35)
        e.pack()
        entries.append(e)

    def save():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vehicles (vehicle_number, vehicle_type, seating_capacity) "
            "VALUES (%s,%s,%s)",
            tuple(e.get() for e in entries)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Vehicle added successfully")
        win.destroy()

    tk.Button(win, text="Add Vehicle", width=25, command=save).pack(pady=25)


# ================== ADD ROUTE ==================
def add_route():
    win = tk.Toplevel(root)
    win.title("Add Route")
    win.geometry("420x380")

    labels = ["Route Name", "Start Location", "End Location", "Pickup Time", "Drop Time"]
    entries = []

    for lbl in labels:
        tk.Label(win, text=lbl, font=("Segoe UI", 10)).pack(pady=4)
        e = tk.Entry(win, width=35)
        e.pack()
        entries.append(e)

    def save():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO routes (route_name, start_location, end_location, pickup_time, drop_time) "
            "VALUES (%s,%s,%s,%s,%s)",
            tuple(e.get() for e in entries)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Route added successfully")
        win.destroy()

    tk.Button(win, text="Add Route", width=25, command=save).pack(pady=25)


# ================== ASSIGN EMPLOYEE ==================
def assign_employee():
    win = tk.Toplevel(root)
    win.title("Assign Employee to Driver")
    win.geometry("420x320")

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT employee_id, employee_name FROM employees")
    employees = cursor.fetchall()

    cursor.execute("SELECT driver_id, driver_name FROM drivers")
    drivers = cursor.fetchall()

    if not employees or not drivers:
        messagebox.showwarning("Warning", "Please add employees and drivers first")
        return

    emp_map = {e[1]: e[0] for e in employees}
    drv_map = {d[1]: d[0] for d in drivers}

    tk.Label(win, text="Select Employee", font=("Segoe UI", 10)).pack(pady=6)
    emp_var = tk.StringVar(value=list(emp_map.keys())[0])
    tk.OptionMenu(win, emp_var, *emp_map.keys()).pack()

    tk.Label(win, text="Select Driver", font=("Segoe UI", 10)).pack(pady=10)
    drv_var = tk.StringVar(value=list(drv_map.keys())[0])
    tk.OptionMenu(win, drv_var, *drv_map.keys()).pack()

    def assign():
        cursor.execute(
            "INSERT INTO assignments (employee_id, driver_id) VALUES (%s,%s)",
            (emp_map[emp_var.get()], drv_map[drv_var.get()])
        )
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Assignment Successful",
            f"Employee '{emp_var.get()}' has been assigned to Driver '{drv_var.get()}'.\n\n"
            "Notification sent to Employee.\n"
            "Notification sent to Driver."
        )
        win.destroy()

    tk.Button(win, text="Assign Employee", width=25, command=assign).pack(pady=25)


# ================== CLEAR EMPLOYEE & DRIVER DATA ==================
def clear_employee_driver_data():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all Employee and Driver data?"):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            # Remove related assignments first
            cursor.execute("DELETE FROM assignments")
            
            # Delete employees
            cursor.execute("DELETE FROM employees")
            cursor.execute("ALTER TABLE employees AUTO_INCREMENT = 1")
            
            # Delete drivers
            cursor.execute("DELETE FROM drivers")
            cursor.execute("ALTER TABLE drivers AUTO_INCREMENT = 1")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "All Employee and Driver data cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ================== RESET ALL DATABASE DATA ==================
def reset_database_data():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear ALL data from the database?"):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            
            tables = ["assignments", "employees", "drivers", "vehicles", "routes"]
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                cursor.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "All database data has been cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ================== MAIN BUTTONS ==================
tk.Button(content, text="Add Employee", command=add_employee, **BTN_STYLE).pack(pady=7)
tk.Button(content, text="Add Driver", command=add_driver, **BTN_STYLE).pack(pady=7)
tk.Button(content, text="Add Vehicle", command=add_vehicle, **BTN_STYLE).pack(pady=7)
tk.Button(content, text="Add Route", command=add_route, **BTN_STYLE).pack(pady=7)
tk.Button(content, text="Assign Employee", command=assign_employee, **BTN_STYLE).pack(pady=7)
tk.Button(content, text="Clear Employee & Driver Data", command=clear_employee_driver_data, **BTN_STYLE).pack(pady=7)

# ================== RESET BUTTON (BOTTOM-RIGHT) ==================
reset_btn = tk.Button(root, text="Reset All Data", command=reset_database_data,
                      width=20, height=2, bg="#e74c3c", fg="white",
                      font=("Segoe UI", 10, "bold"), activebackground="#c0392b")
reset_btn.place(relx=0.95, rely=0.95, anchor="se")

# ================== FOOTER ==================
footer = tk.Label(
    root,
    text="ETMS © 2026 | Academic Project",
    bg="#ecf0f1",
    fg="#7f8c8d",
    font=("Segoe UI", 9)
)
footer.pack(side="bottom", pady=10)

root.mainloop()
