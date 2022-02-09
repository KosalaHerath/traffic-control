"""
 Project A - Traffic Light System
"""

# import libraries
from distutils.errors import DistutilsModuleError
from this import d
from pymata4 import pymata4
import time
import sys

# define pin numbers
PUSH_BUTTON_PIN = 2
PEDESTRIAN_GREEN_PIN = 3
PEDESTRIAN_RED_PIN = 4
TRAFFIC_GREEN_PIN = 5
TRAFFIC_YELLOW_PIN = 6
TRAFFIC_RED_PIN = 7
BUZZER_PIN = 8
TRIGGER_PIN = 12
ECHO_PIN = 13

# system parameters
DISTANCE_THRESHOLD = 20
DEBOUNCE_DELAY = 20

# system variables
fall_back_time = 120
delay_after_vehicle_detection = 1
delay_after_button_detection = 1
pedestrian_red_flashing_duration = 3
pedestrian_red_flashing_frequency = 5
pedestrian_and_traffic_red_duration = 3
traffic_green_duration = 10
traffic_yellow_duration = 3

# create a board instance
board = pymata4.Pymata4()

# set the pin modes
board.set_pin_mode_digital_output(PEDESTRIAN_GREEN_PIN)
board.set_pin_mode_digital_output(PEDESTRIAN_RED_PIN)
board.set_pin_mode_digital_output(TRAFFIC_GREEN_PIN)
board.set_pin_mode_digital_output(TRAFFIC_YELLOW_PIN)
board.set_pin_mode_digital_output(TRAFFIC_RED_PIN)
board.set_pin_mode_digital_output(BUZZER_PIN)
board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN)
board.set_pin_mode_digital_input(PUSH_BUTTON_PIN)

# main function runs at the beginning
def main():
    # update time parameters for night 
    use_night_time_parameters(False)
    # handle errors and interrupts
    try: 
        # initialize the system
        time.sleep(1)
        print("System Starting...")
        last_vehicle_detection_time = time.time()
        
        # run infinitely
        while(True):  
            run_state0()
            time.sleep(0.05) 
            if((is_vehicle_detect()) or 
            (is_fall_back_time_pass(last_vehicle_detection_time))):
                wait_after_vehicle_detection(delay_after_vehicle_detection)
                run_state1(pedestrian_red_flashing_duration, pedestrian_red_flashing_frequency)
                run_state2(pedestrian_and_traffic_red_duration)
                run_state3(traffic_green_duration)
                run_state4(traffic_yellow_duration)
                run_state2(pedestrian_and_traffic_red_duration)
                last_vehicle_detection_time = time.time()      
    except (KeyboardInterrupt,RuntimeError):
        # clean up
        board.shutdown()
        sys.exit(0)

# state0 : Traffic: Red & Pedestrian: Green
def run_state0():
    board.digital_write(PEDESTRIAN_GREEN_PIN, 1)
    board.digital_write(PEDESTRIAN_RED_PIN, 0)
    board.digital_write(TRAFFIC_GREEN_PIN, 0)
    board.digital_write(TRAFFIC_YELLOW_PIN, 0)
    board.digital_write(TRAFFIC_RED_PIN, 1)
    board.digital_write(BUZZER_PIN, 0)

# wait after detection a vehicle
def wait_after_vehicle_detection(delay):
    board.digital_write(BUZZER_PIN, 1)
    time.sleep(delay)
    board.digital_write(BUZZER_PIN, 0)

# state1 : Traffic: Red & Pedestrian: Red
def run_state1(duration, frequency):
    time_period = 1/frequency
    ts = time.time()
    board.digital_write(PEDESTRIAN_GREEN_PIN, 0)
    while(time.time() - ts <= duration):
        board.digital_write(PEDESTRIAN_RED_PIN, 1)
        board.digital_write(BUZZER_PIN, 1)
        time.sleep(time_period)
        board.digital_write(PEDESTRIAN_RED_PIN, 0)
        board.digital_write(BUZZER_PIN, 0)
        time.sleep(time_period)
        
# state2 : Traffic: Red & Pedestrian: Red
def run_state2(duration):
    board.digital_write(PEDESTRIAN_GREEN_PIN, 0)
    board.digital_write(PEDESTRIAN_RED_PIN, 1)
    board.digital_write(TRAFFIC_GREEN_PIN, 0)
    board.digital_write(TRAFFIC_YELLOW_PIN, 0)
    board.digital_write(TRAFFIC_RED_PIN, 1)
    time.sleep(duration)   
    
# state3 : Traffic: Green & Pedestrian: Red
def run_state3(duration):
    board.digital_write(PEDESTRIAN_GREEN_PIN, 0)
    board.digital_write(PEDESTRIAN_RED_PIN, 1)
    board.digital_write(TRAFFIC_GREEN_PIN, 1)
    board.digital_write(TRAFFIC_YELLOW_PIN, 0)
    board.digital_write(TRAFFIC_RED_PIN, 0)
    listen_push_button(PUSH_BUTTON_PIN,DEBOUNCE_DELAY,duration,delay_after_button_detection) 
    
# state4 : Traffic: Yellow & Pedestrian: Red
def run_state4(duration):
    board.digital_write(PEDESTRIAN_GREEN_PIN, 0)
    board.digital_write(PEDESTRIAN_RED_PIN, 1)
    board.digital_write(TRAFFIC_GREEN_PIN, 0)
    board.digital_write(TRAFFIC_YELLOW_PIN, 1)
    board.digital_write(TRAFFIC_RED_PIN, 0)
    time.sleep(duration)     
    
# get distance from sonar sensor  
def get_distance():
    distance = board.sonar_read(TRIGGER_PIN)[0]
    return distance

# check and night mode
def use_night_time_parameters(is_night):
    if(is_night):
        fall_back_time = 120
        delay_after_vehicle_detection = 1
        pedestrian_red_flashing_duration = 3
        pedestrian_red_flashing_frequency = 5
        pedestrian_and_traffic_red_duration = 3
        traffic_green_duration = 10
        traffic_yellow_duration = 3
    else:
        fall_back_time = 120
        delay_after_vehicle_detection = 1
        pedestrian_red_flashing_duration = 3
        pedestrian_red_flashing_frequency = 5
        pedestrian_and_traffic_red_duration = 3
        traffic_green_duration = 10
        traffic_yellow_duration = 3

# detect vehicles using distance to the vehicle
def is_vehicle_detect():
    if(get_distance() < DISTANCE_THRESHOLD):
        print("Vehicle detected!")
        return True
    else:
        return False
    
# check fall back time 
def is_fall_back_time_pass(ts):
    if(time.time() - ts > fall_back_time):
        print("Fallback time passed!")
        return True
    else:
        return False   

# debounce function to get stable state from button
def get_stable_switch_state(button_pin,debounce_delay):
    previous_state = board.digital_read(button_pin)[0]
    count = 0
    while(count < debounce_delay):
        time.sleep(0.001) # 1 millisecond delay
        state = board.digital_read(button_pin)[0]
        if(state != previous_state):
            count = 0
            previous_state = state
        count+=1 
    return state

# check push button input
def listen_push_button(button_pin,debounce_delay,listening_duration,delay):
    ts = time.time()
    print("Button Listening...")
    while(time.time() - ts <= listening_duration):
        if(get_stable_switch_state(button_pin,debounce_delay)):
            print("Button pressed!")
            time.sleep(delay)
            break
        
if __name__ == "__main__": main()