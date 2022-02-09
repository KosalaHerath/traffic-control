"""
 Project A - Traffic Light System
"""
# import libraries
import json
import os
import time

# define file paths
params_path = "params.json"
config_path = "config.json"

# global varables
update_night_mode = False
pin_attempts = 1

# main function
def main():
    run_welcome_client()
    return get_data(params_path)

# data retrieve from json file
def get_data(file_path):
    with open(file_path, "r") as jsonFile:
        data = json.load(jsonFile)
        return data
    
def write_data(file_path,data):
    with open(file_path, "w") as jsonFile:
        json.dump(data, jsonFile)
        
def update_params(key,value):
    global update_night_mode
    params = get_data(params_path)
    if(update_night_mode):
        params["night"][key] = value
    else:
        params["default"][key] = value
    write_data(params_path,params)

def update_config(key,value):
    config = get_data(config_path)
    config[key] = value
    write_data(config_path,config)
    
def run_welcome_client():
    while(True):
        os.system("clear")
        print_logo()
        print("Welcome to Traffic Control System Admin")
        print("\nDo you want to make any changes to the system parameters? ")
        print("""
        1 : YES
        2 : NO
        0 : EXIT"""
                )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            run_pin_client()
        elif choice == '2' :
            print("selected NO...")
        elif choice == '0':
            os.system("clear")
            exit()  

def run_pin_client():
    os.system("clear")
    check_system_lock_status()
    print_logo()
    print("\nPlease enter the four-digit PIN (or 0 to exit).")
    input_pin = input("\nEnter the PIN : ")
    pin = get_data(config_path)["pin"]

    if input_pin == pin:
        for i in range(8):
            os.system("clear")
            print("Correct PIN. Please Wait... ")
            print("Initialize a secure connection with the database: " + i*"> ")
            time.sleep(1)
        run_night_mode_select_client()
    elif input_pin == '0':
        os.system("clear")
        exit()
    else:
        global pin_attempts
        pin_attempts +=  1
        run_pin_invalid_client()  

def run_pin_invalid_client():
    os.system("clear")
    global pin_attempts
    max_attempts = get_data(config_path)["max_attempts"]
    
    check_system_lock_status()
        
    if(pin_attempts > max_attempts):
        print_logo()
        print("Maximum number of attempt reached. System locked for 120 seconds :(")
        update_config("system_lock_timestamp",time.time())
        time.sleep(5)
        os.system("clear")
        exit()
    
    print_logo()
    print("\nInvalid PIN! Please re-enter the four-digit PIN (or 0 to exit).")
    input_pin = input("\nEnter the PIN : ")
    pin = get_data(config_path)["pin"]
    
    pin_attempts +=  1
    if input_pin == pin:
        pin_attempts = 0
        for i in range(8):
            os.system("clear")
            print("Correct PIN. Please Wait... ")
            print("Initialize a secure connection with the database: " + i*"> ")
            time.sleep(1)
        run_night_mode_select_client()
    elif input_pin == '0':
        os.system("clear")
        exit()     
    else:
        run_pin_invalid_client()

def check_system_lock_status():
    ts = time.time()
    last_system_lock_timestamp = get_data(config_path)["system_lock_timestamp"]
    diff = ts - last_system_lock_timestamp
    if(diff < 120):
        print_logo()
        print("System locked...")
        print("Try again in " + str(round(120 - diff)) +  " seconds")
        time.sleep(5)
        os.system("clear")
        exit()

def run_night_mode_select_client():
    while(True):
        os.system("clear")
        print_logo()
        print("\nPlease select the mode of the parameters? ")
        print("""
        1 : DEFAULT
        2 : NIGHT
        0 : EXIT"""
                )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            run_selection_client()
        elif choice == '2' :
            global update_night_mode
            update_night_mode = True;
            run_selection_client()
        elif choice == '0':
            os.system("clear")
            exit() 

def run_selection_client():
    while True:
        os.system("clear")
        print_logo()
        print("\nChoose the parameter you want to update : ")
        print("""
        1 : Fall Back Time 
        2 : Waiting time after vehicle detection
        3 : Waiting time after pedestrian button click detection
        4 : Pedestrian red flashing light duration
        5 : Pedestrian red flashing light frequency
        6 : Traffic and pedestrian simultaneous red light duration
        7 : Traffic green light duration
        8 : Traffic yellow light duration
        0 : Exit"""
              )
        choice = input("\nEnter your choice : ")

        if choice == '1':
            run_update_client("fall_back_time")
        elif choice == '2' :
            run_update_client("delay_after_vehicle_detection")
        elif choice == '3' :
            run_update_client("delay_after_button_detection")
        elif choice == '4' :
            run_update_client("pedestrian_red_flashing_duration")
        elif choice == '5' :
            run_update_client("pedestrian_red_flashing_frequency")
        elif choice == '6' :
            run_update_client("pedestrian_and_traffic_red_duration")
        elif choice == '7' :
            run_update_client("traffic_green_duration")
        elif choice == '7' :
            run_update_client("traffic_yellow_duration")
        elif choice == '0':
            os.system("clear")
            exit()

def run_update_client(param_name):
    os.system("clear")
    print_logo()
    print("\nPlease enter the new time parameter value.")
    new_param = input("\nNew value in seconds : ")
    while(True):
        os.system("clear")
        config_name = get_data(config_path)[param_name]
        print_logo()
        print("Are you sure to update the " + config_name + " with value " 
            + str(new_param) + " seconds?")
        print("""
        1 : YES
        2 : NO"""
                )
        choice = input("\nEnter your choice : ")
        if(choice == '1'):
            update_params(param_name,int(new_param))
            os.system("clear")
            print_logo()
            print("Parameter successfully updated...")
            time.sleep(3)
            run_selection_client()
        elif(choice == '2'):    
            run_selection_client()
            
def print_logo():
    print(r"""
 _____            __  __ _          ___            _             _ 
/__   \_ __ __ _ / _|/ _(_) ___    / __\___  _ __ | |_ _ __ ___ | |
  / /\/ '__/ _` | |_| |_| |/ __|  / /  / _ \| '_ \| __| '__/ _ \| |
 / /  | | | (_| |  _|  _| | (__  / /__| (_) | | | | |_| | | (_) | |
 \/   |_|  \__,_|_| |_| |_|\___| \____/\___/|_| |_|\__|_|  \___/|_|
                                                                   
              __           _                                       
             / _\_   _ ___| |_ ___ _ __ ___                        
             \ \| | | / __| __/ _ \ '_ ` _ \                       
             _\ \ |_| \__ \ ||  __/ | | | | |                      
             \__/\__, |___/\__\___|_| |_| |_|                      
                 |___/                                             
          """
    )
            
if __name__ == "__main__": main()