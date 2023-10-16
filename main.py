import os  #type: ignore
import sqlite3 #Datebase
import hashlib #Hashing
import tkinter as tk #import tkinter
from tkinter import Toplevel, messagebox #import tkinter
from tkinter import ttk #Imported for updating GUI style
import requests #imported for restful api calls

#Creat database instance
connection = sqlite3.connect("database.db") #Create database
cursor = connection.cursor() #Create cursor
#Create tables in the database for first name, last name, username, password and salt
cursor.execute('''CREATE TABLE IF NOT EXISTS user_information (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT,
                  last_name TEXT,
                  username TEXT,
                  password_hash BLOB,
                  salt BLOB)''') #Create table for user information
connection.commit() #Commit changes
connection.close() #Close connection

# Root Menu for user registration and login
root = tk.Tk() #Create tkinter root window
root.title("User Login") #Set title
style = ttk.Style(root) #Create style
style.theme_use("clam") #Set style

#Function to create menu to register user for a new account
def register_menu(): #Function to create menu to register user for a new account
  global firstNameEntry, lastNameEntry, usernameEntry, passwordEntry, register_window, register_warning #Global variables
  register_window = Toplevel(root) #Create toplevel window
  register_window.title("Register") #Set title
  register_window.geometry("500x240") #Set size

  #creates input lables and input fields
  firstNameLabel = ttk.Label(register_window, text="First Name*:") #Create label for first name
  lastNameLabel = ttk.Label(register_window, text="Last Name*:") #Create label for last name
  usernameLabel = ttk.Label(register_window, text="Username*:") #Create label for username
  passwordLabel = ttk.Label(register_window, text="Password*:") #Create label for password
  firstNameEntry = ttk.Entry(register_window) #Create entry for first name
  lastNameEntry = ttk.Entry(register_window) #Create entry for last name
  usernameEntry = ttk.Entry(register_window) #Create entry for username
  passwordEntry = ttk.Entry(register_window, show="*") #Create entry for password
  noteLabel = ttk.Label(register_window, text="         * Input Required") #Create label for note
  register_warning = tk.Label(register_window, text="",fg='#f00') #Warning for input information not meeting requirements

  #creates a submit button and save the register data to database
  saveButton = tk.Button(register_window, text="Submit")
  saveButton.configure(command=save_register)

  #Position buttons and input fields in grid layout
  firstNameLabel.grid(row=0, column=0, padx=30, pady=5) #Position label for first name
  firstNameEntry.grid(row=0, column=1, padx=30, pady=5) #Position entry for first name
  lastNameLabel.grid(row=1, column=0, padx=30, pady=5) #Position label for last name
  lastNameEntry.grid(row=1, column=1, padx=30, pady=5) #Position entry for last name
  usernameLabel.grid(row=2, column=0, padx=30, pady=5) #Position label for username
  usernameEntry.grid(row=2, column=1, padx=30, pady=5) #Position entry for username
  passwordLabel.grid(row=3, column=0, padx=30, pady=5) #Position label for password
  passwordEntry.grid(row=3, column=1, padx=30, pady=5) #Position entry for password
  noteLabel.grid(row=4, column=0, padx=10, pady=5) #Position label for note
  register_warning.grid(row=5, column=1, columnspan=2, padx=1, pady=5)#Position warning for input information not meeting requirements
  saveButton.grid(row=6, column=1, columnspan=2, padx=10, pady=10) #Position submit button


def save_register(): #Function to save registration information based on register menu inputs
  global register_window,register_warning #Global variables
  assert firstNameEntry is not None #Assert first name entry is not none
  first_name = firstNameEntry.get() #Get first name from entry
  assert lastNameEntry is not None #Assert last name entry is not none
  last_name = lastNameEntry.get() #Get last name from entry
  assert usernameEntry is not None #Assert username entry is not none
  username = usernameEntry.get() #Get username from entry
  assert passwordEntry is not None #Assert password entry is not none
  password = passwordEntry.get() #Get password from entry
  salt = os.urandom(16) #Generate salt - a random string added to the passoword and hashed togther to generate the irreversible hash
  #Check if first name was entered 
  if len(first_name) < 1: #If first name is empty
    register_warning.configure(text="* First Name Required") #Set warning to first name
    register_warning.config(text= "First Name is required.") #Set warning to first name
  else:
    #Check if username exits in the database
    connection = sqlite3.connect("database.db") #Connect to database
    cursor = connection.cursor() #Create cursor
    cursor.execute(
        "SELECT first_name, password_hash, salt FROM user_information WHERE username = ?", #Query to check if username exists
        (username, )) #Query database for username
    result = cursor.fetchone() #Get result
    connection.close() #Close connection
    if result: #If result is not none
      register_warning.config(text= "Username exits in the database.") #Set warning to username exits in the database
    else:
      #Check password inputs to meet requirements for 8 charactors, a number, an upper case letter and a lowercase letter.
      if len(password) < 8: #If password is less than 8 charactors
         register_warning.config(text= "Password to be at least 8 characters.") #Set warning to password to be at least 8 charactors
      elif not any(chr.isdigit() for chr in password): #If password does not contain a number
         register_warning.config(text= "Password needs a number.") #Set warning to password needs a number
      elif not any(chr.isupper() for chr in password): #If password does not contain an upper case letter
         register_warning.config(text= "Password needs an uppercase letter.") #Set warning to password needs an upper case letter     
      elif not any(chr.islower() for chr in password): #If password does not contain a lowercase letter
         register_warning.config(text= "Password needs a lowercase letter.") #Set warning to password needs a lowercase letter
      else:
         register_warning.config(text= "") #Set warning to none
         password_bytes = password.encode('utf-8') #Encode password to bytes
         password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000) #Hash password using pbkdf2
         connection = sqlite3.connect("database.db") #Connect to database
         cursor = connection.cursor()  
         
         cursor.execute(
          "INSERT INTO user_information (first_name, last_name, username, password_hash, salt) VALUES (?, ?, ?, ?, ?)",
          (first_name, last_name, username, password_hash, salt)) #Save inputs to the database for first name, last name, username and password
         connection.commit() #Commit changes
         connection.close() #Close connection
         #Show message that the user account has been created.
         messagebox.showinfo(
          "Register",
          f"User Account created successfully:\nFirst Name: {first_name}\nLast Name: {last_name}\nUsername: {username}"
         ) #Show message
         assert register_window is not None #Assert register window is not none
         register_window.destroy() #Destroy register window

# Create login menu
def login_menu():
  global loginUsernameEntry, loginPasswordEntry, login_window,login_warning
  login_window = tk.Toplevel(root)
  login_window.title("Login")
  login_window.geometry("500x160")

  #creates the username and password labels and inputs
  loginLabel = ttk.Label(login_window, text="Username:")
  loginUsernameEntry = ttk.Entry(login_window)
  loginLabel.grid(row=0, column=0, padx=30, pady=5)
  loginUsernameEntry.grid(row=0, column=1, padx=30, pady=5)
  loginPasswordLabel = ttk.Label(login_window, text="Password:")
  loginPasswordEntry = ttk.Entry(login_window, show="*")
  loginPasswordLabel.grid(row=1, column=0, padx=30, pady=5)
  loginPasswordEntry.grid(row=1, column=1, padx=30, pady=5)
  login_warning = tk.Label(login_window, text="",fg='#f00') #Warning for input information not meeting requirements
  login_warning.grid(row=2, column=1, columnspan=2, padx=30, pady=5)

  #Create login button
  loginButton = tk.Button(login_window, text="Login")
  loginButton.configure(command=login)
  loginButton.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

  #Create text for retry or register
  loginNoteLabel = tk.Label(
      login_window,
      text="Failed to login, please try again or register for new account.")
  loginNoteLabel.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

#Function to login user with the user inputs of username and password
def login():
  global welcome_window,login_window,first_name,login_warning
  assert loginUsernameEntry is not None
  enteredUsername = loginUsernameEntry.get()
  assert loginPasswordEntry is not None
  enteredPassword = loginPasswordEntry.get()

  #Verify from the database to see if username exits
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()
  cursor.execute(
      "SELECT first_name, password_hash, salt FROM user_information WHERE username = ?",
      (enteredUsername, ))
  result = cursor.fetchone()
  connection.close()
  if result:
    storedFirstName, storedPasswordHash, storedSalt = result
    enteredPasswordBytes = enteredPassword.encode('utf-8')
    enteredPasswordHash = hashlib.pbkdf2_hmac('sha256', enteredPasswordBytes,
                                              storedSalt, 100000)
    #If the login user's password is same to the password in database
    #Show welcome message and GUI
    if storedPasswordHash == enteredPasswordHash:
      first_name = storedFirstName
      loggedin_window = tk.Toplevel(root)
      loggedin_window.title("Logged In")
      loggedin_window.geometry("800x40")
      loggedin_label = tk.Label(loggedin_window,text=f"Welcome, {first_name}!")
      loggedin_label.pack(padx=20, pady=10)
      #Show graphic user interface
      GUI()
      #Close out root and login windows
      assert login_window is not None
      login_window.destroy()
      root.withdraw()
    else:
      login_warning.config(text= "Password is incorrect. Try again.")
  else:
    login_warning.config(text= "Username not found. Try agian or register.")

def exit_app(): #Function to exit the program
  root.quit()

# Functions for restful API call
# Function to fetch the robot's current state
def fetch_robot_state():
    api_url = "http://your_api_endpoint/move" #To be updated with the actual API endpoint
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('current_state', 'STOP')
    return 'STOP'

# Function to send a command to the robot
def send_command(direction):
    api_url = "http://your_api_endpoint/move" #To be updated with the actual API endpoint
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

def GUI(): #Function to create GUI after user logged in
  global state_label,user_window
  user_window = tk.Toplevel(root)
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

# Create starting login/register window 
# Create a width for all the buttons
button_width = 10
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Login with an existing account:").grid(row=0,column=0,padx=20,pady=10)
login_button = ttk.Button(frm, text="Login", command=login_menu,width=button_width)
login_button.grid(row=0, column=1, padx=20, pady=10)

ttk.Label(frm, text="Or register a new account:").grid(row=1,column=0,padx=20,pady=10)
register_button = ttk.Button(frm, text="Register", command=register_menu,width=button_width)
register_button.grid(row=1, column=1, padx=20, pady=10)

exit_button = ttk.Button(frm, text="Exit", command=exit_app)
exit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()