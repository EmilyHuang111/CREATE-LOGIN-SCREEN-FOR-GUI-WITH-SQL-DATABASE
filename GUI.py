import tkinter as tk
import requests #imported for restful api calls
from tkinter import ttk #Imported for updating GUI style

# Root Menu for user registration and login
root = tk.Tk()
root.title("User Login")
#define style
style = ttk.Style(root)
style.theme_use("clam")

# Functions for restful API call
# Function to fetch the robot's current state
def fetch_robot_state():
    api_url = "http://your_api_endpoint/move" #To be updated with the actural API endpoint
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('current_state', 'STOP')
    return 'STOP'

# Function to send a command to the robot
def send_command(direction):
    api_url = "http://your_api_endpoint/move" #To be updated with the actural API endpoint
    data = {'direction': direction}
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return f"Moved {direction} successfully."
    return f"Failed to move {direction}."

# Function to update the current state label
def update_state_label():
  global state_label,user_window
  current_state = fetch_robot_state()
  state_label.config(text=f"Current State: {current_state}")
  user_window.after(1000, update_state_label)  # Update every 1 second

def exit_app(): #Function to exit the program
  root.quit()

def GUI(): #Function to create GUI after user logged in
  global state_label,user_window
  user_window = tk.Toplevel()
  user_window.title("GUI")
  user_window.geometry("800x460")

  # Create four grid cells as Frame widgets without background colors
  frame1 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame1.grid(row=0, column=0, padx=2, pady=2)

  frame2 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame2.grid(row=0, column=1, padx=2, pady=2)

  frame3 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame3.grid(row=1, column=0, padx=2, pady=2)

  frame4 = tk.Frame(user_window, width=400, height=200, relief=tk.SUNKEN, borderwidth=2)
  frame4.grid(row=1, column=1, padx=2, pady=2)

  # Create a frame for direction buttons in the first grid cell
  direction_frame = tk.Frame(frame1)
  direction_frame.grid(row=0, column=0, rowspan=2, columnspan=2)
  # Create a width for all the buttons
  button_width = 10
  # Add direction buttons to the frame
  btn_Label = ttk.Label(direction_frame, text="Direction Control Buttons")
  btn_fwd = ttk.Button(direction_frame, text="FWD", command=lambda: send_command("FWD"),width=button_width)
  btn_bkwd = ttk.Button(direction_frame, text="BKWD", command=lambda: send_command("BKWD"),width=button_width)
  btn_left = ttk.Button(direction_frame, text="LEFT", command=lambda: send_command("LEFT"),width=button_width)
  btn_right = ttk.Button(direction_frame, text="RIGHT", command=lambda: send_command("RIGHT"),width=button_width)
  btn_stop = ttk.Button(direction_frame, text="STOP", command=lambda: send_command("STOP"),width=button_width)
  btn_Label.grid(row=0, column=0,columnspan=2)
  btn_fwd.grid(row=1, column=0)
  btn_bkwd.grid(row=2, column=0)
  btn_left.grid(row=1, column=1)
  btn_right.grid(row=2, column=1)
  btn_stop.grid(row=1, column=2)

  # Define the lable for the movement state
  state_label = ttk.Label(direction_frame, text="   Current State: STOP")
  state_label.grid(row=3, column=0)

  log_frame = tk.Frame(frame2)
  log_frame.grid(row=2, column=0, rowspan=2, columnspan=2)
  log_Label = ttk.Label(log_frame, text="Log feed information")
  log_Label.grid(row=0, column=0,columnspan=2)

  video_frame = tk.Frame(frame3)
  video_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
  video_Label = ttk.Label(video_frame, text="Video feed information")
  video_Label.grid(row=0, column=0,columnspan=2)
  videoinput1_Label = ttk.Label(video_frame, text="")
  videoinput1_Label.grid(row=1, column=0,columnspan=2)
  videoinput2_Label = ttk.Label(video_frame, text="")
  videoinput2_Label.grid(row=2, column=0,columnspan=2)

  blank_frame = tk.Frame(frame4)
  blank_frame.grid(row=1, column=1, rowspan=2, columnspan=2)
  blank_Label = ttk.Label(blank_frame, text="Blank for future use")
  blank_Label.grid(row=0, column=0,columnspan=2)

  #Create an exit button to quite the program  
  exit_button = ttk.Button(user_window, text="Exit", command=exit_app)
  exit_button.grid(row=3, column=1, columnspan=2, padx=20, pady=10)
