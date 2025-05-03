import tkinter as tk # Import the Tkinter library to create the GUI
from tkinter import messagebox # For showing popup messages
import json # To save and load booking data
import os # To check if the bookings file exists

# Flight Class to store info about each flight
class Flight:
    def __init__(self, code, destination, date_time):
        self.code = code # Flight code (like LA123)
        self.destination = destination # Where the flight is going
        self.date_time = date_time # When the flight is leaving

    def __str__(self):
        # This helps print the flight info in a readable way
        return f"{self.code}: {self.destination} at {self.date_time}"
    
# Reservation system class to manage all bookings and flights
class ReservationSystem:
    def __init__(self):
        self.flights = [] # List to store all flights
        self.bookings = {} # Dictionary to store user bookings
        self.load_flights() # Load flights into the list
        self.load_bookings() # Load previous bookings if any
    
    def load_flights(self):
        # Here we just add 3 flights manually
        self.flights = [
            Flight("LA123", "Los Angeles", "2025-05-01 10:00"),
            Flight("TX456", "Texas", "2025-05-02 14:30"),
            Flight("NY789", "New York", "2025-05-03 18:00")
        ]
    
    def load_bookings(self):
        # Load bookings from the JSON file if it exists
        if os.path.exists("bookings.json"):
            with open("bookings.json", "r") as f:
                self.bookings = json.load(f)

    def save_bookings(self):
        # Save bookings to the file so we don't lose them
        with open("bookings.json", "w") as f:
            json.dump(self.bookings, f)

    def get_flight(self, code):
        # Find a flight object by its code
        for flight in self.flights:
            if flight.code == code:
                return flight
        return None  # If not found, return nothing

    def book_flight(self, name, code):
        flight = self.get_flight(code)  # Look up the flight
        if name and flight:
            self.bookings[name] = code  # Save the booking
            self.save_bookings()  # Write to file
            return flight  # Return the flight object
        return None  # If something went wrong

    def view_booking(self, name):
        code = self.bookings.get(name)  # Get the flight code
        if code:
            return self.get_flight(code)  # Return the flight object
        return None  # If not booked

    def cancel_booking(self, name):
        if name in self.bookings:
            del self.bookings[name]  # Remove the booking
            self.save_bookings()  # Save changes
            return True
        return False  # Nothing to cancel

#-------------------------------------GUI SETUP------------------------------------------------#

system = ReservationSystem()  # Create system object
window = tk.Tk()  # Create main window
window.title("Shabo Airline")  # Window title
window.geometry("400x500")  # Size of the window

# Create frames for different pages
login_frame = tk.Frame(window) # Login page frame
main_frame = tk.Frame(window) # Main menu frame
booking_frame = tk.Frame(window) # Booking flights frame
view_frame = tk.Frame(window) # Viewing booked flights frame
cancel_frame = tk.Frame(window) # Cancelling bookings frame
admin_frame = tk.Frame(window) # Admin main menu frame
manage_flights_frame = tk.Frame(window) # Manage flights frame
add_flight_frame = tk.Frame(window)

# Configure grid layout for frames
for frame in (login_frame, main_frame, booking_frame, view_frame, cancel_frame, admin_frame, manage_flights_frame, add_flight_frame):#Loopsugh all frames
    frame.grid(row=0, column=0, sticky="nsew") # Puts each frame in the same spot, stacked
window.grid_rowconfigure(0, weight=1) # Vertical
window.grid_columnconfigure(0, weight=1) # Horizontal

#----------------------------------LOGIN PAGE GUI-------------------------------------------------#
tk.Label(login_frame, text="Login Page", font=("Arial", 20)).pack(pady=20) # Title
tk.Label(login_frame, text="Select User Type:").pack() # Ask user type

login_var = tk.StringVar() # This stores the user choice
login_var.set("Traveler") # Default is Traveler

# Function to handle User login
def handle_user_login():
    # This frame will pop up to enter user's name
    def submit_name():
        user_name = user_name_entry.get()
        if user_name:
            messagebox.showinfo("Login Successful", f"Welcome, {user_name}!")
            show_frame(main_frame)  # Go to the main menu
        else:
            messagebox.showerror("Error", "Please enter your name.")

    # New small window pops up for name input
    name_window = tk.Toplevel(window)  # Create a popup window
    name_window.title("Enter Name")  # Window title
    name_window.geometry("300x150")  # Window size

    tk.Label(name_window, text="Please enter your name:").pack(pady=10)
    user_name_entry = tk.Entry(name_window)
    user_name_entry.pack(pady=5)

    tk.Button(name_window, text="Submit", command=submit_name).pack(pady=10)

# Function for Admin Login page
def handle_admin_login():
    # Function to check the password prompt
    def submit_password():
        entered = password_entry.get()
        if entered == "2025":  # Correct password
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            password_window.destroy()  # Close the popup
            show_frame(admin_frame)  # Go to admin menu
        else:
            messagebox.showerror("Error", "Incorrect password.")
    
    # Create popup window to enter password
    password_window = tk.Toplevel(window)  # Small window on top
    password_window.title("Admin Login")  # Title
    password_window.geometry("300x150")  # Size

    tk.Label(password_window, text="Enter Admin Password:").pack(pady=10)  # Label
    password_entry = tk.Entry(password_window, show="*")  # Hide text
    password_entry.pack(pady=5)  # Entry box

    tk.Button(password_window, text="Submit", command=submit_password).pack(pady=10)  # Submit button


# Buttons for selecting user type
tk.Button(login_frame, text="User", width=15, command=handle_user_login).pack(pady=10)
tk.Button(login_frame, text="Admin", width=15, command=handle_admin_login).pack(pady=5)



#----------------------------------USER MAIN MENU GUI---------------------------------------------------#
# Main Menu UI
tk.Label(main_frame, text="Shabo Airline", font=("Arial", 20)).pack(pady=20) 
tk.Label(main_frame, text="Welcome to Shabo Airline Reservation System", font=("Arial", 12)).pack(pady=10) 
tk.Button(main_frame, text="Book a Flight", command=lambda: show_frame(booking_frame)).pack(pady=10) # This button takes me to the booking page
tk.Button(main_frame, text="View Bookings", command=lambda: show_frame(view_frame)).pack(pady=10) # This button takes me to the view page
tk.Button(main_frame, text="Cancel Booking", command=lambda: show_frame(cancel_frame)).pack(pady=10) # This button takes me to the cancel page
tk.Button(main_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10) # This button takes me back to login page

# Booking UI
tk.Label(booking_frame, text="Book a Flight", font=("Arial", 16)).pack(pady=10)

tk.Label(booking_frame, text="Your Name:").pack()
name_entry = tk.Entry(booking_frame)
name_entry.pack()

tk.Label(booking_frame, text="Select Flight:").pack()

# Dropdown menu for available flights
flight_var = tk.StringVar()
flight_var.set(system.flights[0].code if system.flights else "")  # Set default

# Show description of selected flight
selected_flight_label = tk.Label(booking_frame, text="", fg="gray")
selected_flight_label.pack()

def update_flight_info(*args):
    code = flight_var.get()
    flight = system.get_flight(code)
    if flight:
        selected_flight_label.config(text=f"{flight.destination} at {flight.date_time}")
    else:
        selected_flight_label.config(text="")

flight_var.trace("w", update_flight_info)

flight_options = [flight.code for flight in system.flights]
flight_menu = tk.OptionMenu(booking_frame, flight_var, *flight_options)
flight_menu.pack()

# Function to handle booking a flight
def handle_booking():
    name = name_entry.get().strip()
    code = flight_var.get()
    flight = system.book_flight(name, code)
    if flight:
        messagebox.showinfo("Success", f"{name} booked on {flight}")
        name_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid name or flight code.")

tk.Button(booking_frame, text="Book", command=handle_booking).pack(pady=5)
tk.Button(booking_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# View Booking UI
tk.Label(view_frame, text="View Booking", font=("Arial", 16)).pack(pady=10)
tk.Label(view_frame, text="Your Name:").pack()
view_name_entry = tk.Entry(view_frame)  # Text box for name
view_name_entry.pack()

# Function when "View" is clicked
def handle_view():
    name = view_name_entry.get()
    flight = system.view_booking(name)
    if flight:
        messagebox.showinfo("Booking Found", f"{name} is booked on {flight}")
    else:
        messagebox.showerror("Not Found", "No booking found.")

tk.Button(view_frame, text="View", command=handle_view).pack(pady=5)
tk.Button(view_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

# Cancel Booking UI
tk.Label(cancel_frame, text="Cancel Booking", font=("Arial", 16)).pack(pady=10)
tk.Label(cancel_frame, text="Your Name:").pack()
cancel_name_entry = tk.Entry(cancel_frame)  # Text box for name
cancel_name_entry.pack()

# Function when "Cancel Booking" is clicked
def handle_cancel():
    name = cancel_name_entry.get()
    if system.cancel_booking(name):
        messagebox.showinfo("Cancelled", f"Booking for {name} has been cancelled.")
    else:
        messagebox.showerror("Error", "No booking found to cancel.")

tk.Button(cancel_frame, text="Cancel Booking", command=handle_cancel).pack(pady=5)
tk.Button(cancel_frame, text="Back", command=lambda: show_frame(main_frame)).pack()

#----------------------------------ADMIN MAIN MENU GUI---------------------------------------------------#
tk.Label(admin_frame, text="Admin Dashboard", font=("Arial", 20)).pack(pady=20) # Title for Admin page
tk.Label(admin_frame, text="Welcome, Admin", font=("Arial", 12)).pack(pady=10) # Welcome message

# Function to load and display the flights
def display_flights():
    flights_text.delete("1.0", tk.END)  # Clear previous text
    for flight in system.flights:  # Loop through all flight objects
        flights_text.insert(tk.END, f"{flight}\n")  # Add each to the text box

# Call display_flights() whenever this page is shown
def show_manage_flights():
    display_flights() # Load all flights into the text box
    show_frame(manage_flights_frame)

tk.Button(admin_frame, text="Manage Flights", command=show_manage_flights).pack(pady=10)
tk.Button(admin_frame, text="Logout", command=lambda: show_frame(login_frame)).pack(pady=10)

# Manage Flights Page
tk.Label(manage_flights_frame, text="All Available Flights", font=("Arial", 16)).pack(pady=10)

# This text widget will show the list of flights
flights_text = tk.Text(manage_flights_frame, width=40, height=10)
flights_text.pack(pady=5)

# Add Flight button in Manage Flights frame
tk.Button(manage_flights_frame, text="Add Flight", command=lambda: show_frame(add_flight_frame)).pack(pady=10)

# Back button
tk.Button(manage_flights_frame, text="Back", command=lambda: show_frame(admin_frame)).pack(pady=10)

# Add Flight Page - where admin types in new flight info
tk.Label(add_flight_frame, text="Add New Flight", font=("Arial", 16)).pack(pady=10)

# Entry for flight code
tk.Label(add_flight_frame, text="Flight Code:").pack()
new_code_entry = tk.Entry(add_flight_frame)
new_code_entry.pack()

# Entry for destination
tk.Label(add_flight_frame, text="Destination:").pack()
new_destination_entry = tk.Entry(add_flight_frame)
new_destination_entry.pack()

# Entry for date/time
tk.Label(add_flight_frame, text="Date & Time (YYYY-MM-DD HH:MM):").pack()
new_datetime_entry = tk.Entry(add_flight_frame)
new_datetime_entry.pack()

# Function to handle adding a new flight
def add_new_flight():
    # Get user input from the entry boxes
    code = new_code_entry.get()
    destination = new_destination_entry.get()
    date_time = new_datetime_entry.get()

    # Basic validation: make sure none are empty
    if not code or not destination or not date_time:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Create a new Flight object with entered info
    new_flight = Flight(code, destination, date_time)

    # Add the flight to the system's list
    system.flights.append(new_flight)

    # Show a message to confirm it worked
    messagebox.showinfo("Success", f"Flight {code} added successfully!")

    # Clear the entry boxes for the next input
    new_code_entry.delete(0, tk.END)
    new_destination_entry.delete(0, tk.END)
    new_datetime_entry.delete(0, tk.END)

    # Refresh the flight display in manage flights page
    display_flights()

    # Go back to the Manage Flights page
    show_frame(manage_flights_frame)

# Submit button that adds the flight
tk.Button(add_flight_frame, text="Submit", command=add_new_flight).pack(pady=10)

# Back button to return to manage flights
tk.Button(add_flight_frame, text="Back", command=lambda: show_frame(manage_flights_frame)).pack()

# Function to switch between frames
def show_frame(frame): # Function changes which page I see
    frame.tkraise() # Brings the chosen frame to the front

# Show main menu when app starts
show_frame(login_frame)

# Run the app
window.mainloop()