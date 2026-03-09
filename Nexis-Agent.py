#==============================
#Import Modules
#==============================

import random
import math
import tkinter as tk
from datetime import datetime
import subprocess
import platform
import requests

#==============================
#Define variables
#==============================

API_KEY = 'OWM_APi'

#==============================
#Define Time And Date Variables (Up here to be accessible to the Lists)
#==============================

now = datetime.now()
milliseconds = now.microsecond // 1000

#==============================
#Define Functions (Used by core)
#==============================
def update_vars():
    global now
    global milliseconds

    now = datetime.now()
    milliseconds = now.microsecond // 1000

#==============================
#Get Github response lists
#==============================

def get_list_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            items = response.text.strip().split('\n')
            return [eval(f'f"""{item}"""') for item in items if item]
        else:
            print(f"Failed to fetch file. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    
#==============================
#Get Ip Address
#==============================

ip = requests.get("https://api.ipify.org").text
city = requests.get(f"https://ipinfo.io/{ip}/json").json().get("city")
        
if not city:
    print("Could not detect city")
else:
    print(f"Detected city: {city}")

#==============================
#Check Wifi Connection
#==============================

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=5)
        return ""
    except (requests.ConnectionError, requests.Timeout):
        return "not"
    
#==============================
#Get Weather
#==============================

def getweather():
    try:        
        if not city:
            return "Could not detect city"

        weather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
        ).json()

        if "main" not in weather:
            return f"Error: {weather.get('message', 'Unknown error')}"

        temp = weather["main"]["temp"]
        return f"{temp}°F"

    except Exception as e:
        print(f"Error: {e}")

#==============================
#Create Lists (Used by core)
#==============================

inputs = [
    "hello",
    "hey",
    "what's up",
    "wassup",
    "how are you",
    "how are you doing",
    "how's it going",
    "what's the time",
    "what time is it",
    "what's the date today",
    "what's the date",
    "what's today's date",
    "are you connected to wifi",
    "are you connected to the wifi",
    "am i connected to wifi",
    "am i connected to the wifi",
]

responses = [
    random.choice(('Hello.', 'Hey whats up. ', 'Wassup.')),
    random.choice(('I am doing well, thank you for asking.', 'I am doing great, Thanks for asking.')),
    random.choice((f"The time is {now.strftime('%H:%M')}.", f"It's currently {now.strftime('%H:%M')}.", f"The current time is {now.strftime('%H:%M')}.")), 
    random.choice((f"Today's date is {now.strftime('%m-%d-%Y')}.", f"The date today is {now.strftime('%m-%d-%Y')}.", f"It's currently {now.strftime('%m-%d-%Y')}.")),
    random.choice((f"Your wifi is {is_connected()} connected.", f"Your wfif right now is {is_connected()} connected.", f"Your wifi is currently {is_connected()} connected.")),
    random.choice((f"My wifi is {is_connected()} connected.", f"My wfif right now is {is_connected()} connected.", f"My wifi is currently {is_connected()} connected."))
]
response_table = [
    f"{responses[0]}",
    f"{responses[0]}",
    f"{responses[0]}",
    f"{responses[0]}",
    f"{responses[1]}",
    f"{responses[1]}",
    f"{responses[1]}",
    f"{responses[2]}",
    f"{responses[2]}",
    f"{responses[3]}",
    f"{responses[3]}",
    f"{responses[3]}",
    f"{responses[4]}",
    f"{responses[4]}",
    f"{responses[5]}",
    f"{responses[5]}"
]

#==============================
#Update Response Table With Github Lists
#==============================

try:
    inputs = get_list_from_github("https://raw.githubusercontent.com/SpaceCoder1000/Nexis-Agent/refs/heads/main/inputs.txt")
    responses = get_list_from_github("https://raw.githubusercontent.com/SpaceCoder1000/Nexis-Agent/refs/heads/main/response.txt")
    response_table = get_list_from_github("https://raw.githubusercontent.com/SpaceCoder1000/Nexis-Agent/refs/heads/main/response_table.txt")
    print(inputs)
    print(responses)
    print(response_table)
except Exception as e:
    print(f"An error occurred while fetching GitHub lists: {e}")

#==============================
#Core Response Generator
#==============================

def generate_response(user_said):

    add_text(("right", user_said))

    user_said_list = []
    last_end = 0
    for i in range(len(user_said)):
        if user_said[i] == "." or user_said[i] == "!" or user_said[i] == "?":
            user_said_list.append(user_said[last_end:i])
            last_end = i + 1

    for a in range(len(user_said_list)):
        update_vars()

        response = ""

        response_index = 0

        for i in range(len(inputs)):
          if inputs[i] in user_said_list[a]:
               response = f"{response}{response_table[i]}"

        if response == "":
            response = "Something went wrong."

        add_text(("left", response))
        print(user_said_list)

#==============================
#Lowercase User Input
#==============================

def process_input(usersaid):
    generate_response(usersaid.lower())

#==============================
#Define GUI
#==============================

root =tk.Tk()

#==============================
#Configure GUI
#==============================

root.title("WIP")
root.geometry("500x200")
root.configure(bg="#282828")

#==============================
#Add Navbar
#==============================

top = tk.Frame(root, bg="#2d2d2d")
top.pack(side="top", fill="x")

bottom = tk.Frame(root,bg="#2d2d2d")
bottom.pack(side="bottom", fill="x")

title = tk.Label(top, text="Nexis Agent", anchor="w",bg="#2d2d2d", fg="#FFFFFF", font=("Arial", 16, "bold"))
title.pack(side="left", padx=8, pady=6)

navbar_var = tk.StringVar(value="navbar_text")
navbar_label = tk.Label(top, textvariable=navbar_var, anchor="e",bg="#2d2d2d", fg="#FFFFFF", font=("Arial", 12))
navbar_label.pack(side="right", padx=8, pady=6)

promt_box = tk.Entry(bottom, width=70,bg="#383838", fg="#FFFFFF", insertbackground="#FFFFFF")
promt_box.pack(side="left",padx=5,pady=10)

promt_submit = tk.Button(bottom, text="Submit", bg="#383838", fg="#FFFFFF", activebackground="#505050", activeforeground="#FFFFFF",command=lambda: process_input(promt_box.get()))
promt_submit.pack(side="right", padx=5, pady=10)

#==============================
#Add Center Text Box
#==============================

chat_frame = tk.Frame(root, bg="#282828")
chat_frame.pack(fill="both", expand=True, padx=5, pady=5)

chat_box = tk.Text(
    chat_frame,
    bg="#1e1e1e",
    fg="#ffffff",
    insertbackground="#ffffff",
    wrap="word",
    state="disabled"
)
chat_box.pack(fill="both", expand=True)

#==============================
#Function To Add Text
#==============================

def add_text(message):
    side, text = message

    chat_box.config(state="normal")

    if side == "left":
        chat_box.insert("end", f"{text}\n")
    elif side == "right":
        chat_box.insert("end", f"You:{text}\n", "right")

    chat_box.config(state="disabled")
    chat_box.see("end")

def refresh():
    update_vars()
    navbar_var.set(f"{now.strftime('%H:%M')} | {now.strftime('%m-%d-%Y')} | {city}")

#==============================
#core loop
#============================== 

def core_loop():
    refresh()
    root.after(10, core_loop)

#==============================
#Run App
#==============================

core_loop()
add_text(("left", "Hello! I'm Nexis Agent. How can I assist you today?"))
root.mainloop()
