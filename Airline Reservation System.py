import tkinter as tk # Import the Tkinter library to create the GUI
from tkinter import messagebox
import json
import os

# Create main window
window = tk.Tk() # Initialize the Tkinter window
window.title("Shabo Airline") # Set window title
window.geometry("400x500") # Set window Size

# Dictionary of flights
flights = {
    "LA123": "Los Angeles",
    "TX456": "Texas",
    "NY789": "New York"
}

# Load existing reservations from JSON file
if os.path.exists("reservations.json"):
    with open("reservations.json", "r") as file:
        reservations = json.load(file)
else:
    reservations = {}

def save_reservations():
    with open("reservations.json", "w") as file:
        json.dump(reservations, file)

# Function to book flight
def book_flight():
    name = name_entry.get() # Get name entered by user
    flight_num = flight_entry.get() # Get flight number entered by user

# Check if name is entered and flight number is valid
    if name and flight_num in flights: 
        reservations[name] = flight_num  # Save booking (name ---> flight number)
        save_reservations() 
        messagebox.showinfo("Done", f"Booked {flight_num} to {flights[flight_num]} for {name}!") # Show confirmation message
        name_entry.delete(0, tk.END) # Clear the 'Name' input box
        flight_entry.delete(0, tk.END) # Clear the 'Flight Number" box
    else: 
        messagebox.showerror("Error", "Wrong flight number or no name entered!") # Show error message if something is wrong    

def view_flights():
    name = name_entry.get()
    if name in reservations:
        flight_num = reservations[name]
        messagebox.showinfo("Your Flight", f"{name}, you're booked on {flight_num} to {flights[flight_num]}")   
    elif name: 
        messagebox.showerror("Oops", "No booking for that name!")   
    else:
        messagebox.showerror("Oops", "Need a name first!")
    name_entry.delete(0, tk.END)
    flight_entry.delete(0, tk.END)

def cancel_booking():
    name = cancel_name_entry.get()
    if name in reservations:
        del reservations[name]
        save_reservations()
        messagebox.showinfo("Cancellation Successful", f"Booking for {name} has been canceled.")

    else:
        messagebox.showerror("No Booking Found", f"No booking found for {name}.") 



#-------------------------------------GUI-------------------------------------------------#
# Create frames for different pages
main_frame = tk.Frame(window) # Main menu frame
booking_frame = tk.Frame(window) # Booking flights frame
view_frame = tk.Frame(window) # Viewing booked flights frame
cancel_frame = tk.Frame(window) # Cancelling bookings frame

# Function to switch between frames
def show_frame(frame): # Function changes which page I see
    frame.tkraise() # Brings the chosen frame to the front

# Configure grid layout for frames
for frame in (main_frame, booking_frame, view_frame, cancel_frame): # Loops through all frames
    frame.grid(row=0, column=0, sticky="nsew") # Puts each frame in the same spot, stacked
window.grid_rowconfigure(0, weight=1) # Vertical
window.grid_columnconfigure(0, weight=1) # Horizontal

# Main Menu Frame
tk.Label(main_frame, text="Shabo Airline", font=("Arial", 20)).pack(pady=20) 
tk.Label(main_frame, text="Welcome to Shabo Airline Reservation System", font=("Arial", 12)).pack(pady=10) 

# Buttons
tk.Button(main_frame, text="Book a Flight", command=lambda: show_frame(booking_frame)).pack(pady=10) # This button takes me to the booking page
tk.Button(main_frame, text="View Bookings", command=lambda: show_frame(view_frame)).pack(pady=10) # This button takes me to the view page
tk.Button(main_frame, text="Cancel Booking", command=lambda: show_frame(cancel_frame)).pack(pady=10) # This button takes me to the cancel page

# Show main frame 
show_frame(main_frame)

# Start the GUI loop
window.mainloop() # Keeps the window open until closed by the user

