import threading
from tkinter import *
from main import voice_changer, stop_voice_changer

# Create Object
root = Tk()

# Add Title
root.title('On/Off Switch!')

# Add Geometry
root.geometry("500x300")

# Keep track of the button state on/off
is_on = True

# Create Label
my_label = Label(root, 
	text = "The Switch Is On!", 
	fg = "green", 
	font = ("Helvetica", 32))

my_label.pack(pady = 20)

# Define our switch function
def switch():
    global is_on
    
    # Determine is on or off
    if is_on:
        on_button.config(image = off)
        my_label.config(text = "The Switch is Off", fg = "grey")
        is_on = False
        # Start the voice changer in a separate thread
        threading.Thread(target=voice_changer, daemon=True).start()
        
    else:
        on_button.config(image = on)
        my_label.config(text = "The Switch is On", fg = "green")
        is_on = True
        # Signal to stop the voice changer
        stop_voice_changer()

# Define Our Images
on = PhotoImage(file = "ON.png")
off = PhotoImage(file = "OFF.png")

# Create A Button
on_button = Button(root, image = on, bd = 0, command = switch)
on_button.pack(pady = 50)

# Execute Tkinter
root.mainloop()
