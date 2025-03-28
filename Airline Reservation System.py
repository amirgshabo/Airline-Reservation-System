import tkinter as tk # Import the Tkinter library to create the GUI

# Create main window
window = tk.Tk() # Initialize the Tkinter window
window.title("Airline Reservation System") # Set window title
window.geometry("400x400") # Set window Size

# Title Label
tk.Label(window, text="Airline Reservation System", font=("Arial", 14)).pack(pady=10)

# Label and inpute box for passenger name
tk.Label(window, text="Name:").pack() # Label for name
name_entry = tk.Entry(window, width=25) #Input box for name
name_entry.pack(pady=5)

# Label and inpute box for flight number
tk.Label(window, text="Flight number: ").pack() # Label for flight number
flight_entry = tk.Entry(window, width=25) # Input box for flight number
flight_entry.pack(pady=5)

# Button to submit the booking
tk.Button(window, text="Book Flight").pack(pady=10) # Booking button

# Label to show the confirmation message
confirmation_label = tk.Label(window, text="") # Empty label for messages
confirmation_label.pack(pady=10)

# Start the GUI loop
window.mainloop() # Keeps the window open until closed by the user



