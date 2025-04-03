import tkinter as tk # Import the Tkinter library to create the GUI
from tkinter import messagebox

# Create main window
window = tk.Tk() # Initialize the Tkinter window
window.title("Shabo Airline") # Set window title
window.geometry("400x400") # Set window Size

# List of flights
flights = {
    "LA123": "Los Angeles",
    "TX456": "Texas",
    "NY789": "New York"
}

# Store bookings in a dictionary
reservations = {}

# Function to book flight
def book_flight():
    name = name_entry.get() # Get name entered by user
    flight_num = flight_entry.get() # Get flight number entered by user

# Check if name is entered and flight number is valid
    if name and flight_num in flights: 
        reservations[name] = flight_num  # Save booking (name ---> flight number)
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

# Title Label
tk.Label(window, text="Shabo Airline", font=("Arial", 14)).pack(pady=10)

# Label and inpute box for passenger name
tk.Label(window, text="Name:").pack() # Label for name
name_entry = tk.Entry(window, width=25) #Input box for name
name_entry.pack(pady=5)

# Label and inpute box for flight number
tk.Label(window, text="Flight number: ").pack() # Label for flight number
flight_entry = tk.Entry(window, width=25) # Input box for flight number
flight_entry.pack(pady=5)

# Button to submit the booking
tk.Button(window, text="Book Flight", command=book_flight).pack(pady=10) # Booking button

# Button to view flights
tk.Button(window, text="View Flights", command=view_flights).pack(pady=10)

# Label to show the confirmation message
confirmation_label = tk.Label(window, text="") # Empty label for messages
confirmation_label.pack(pady=10)



# Start the GUI loop
window.mainloop() # Keeps the window open until closed by the user

