###########################
# run.py
#
# The main code that will carry the simulation and the various components.
# For now, run this file.
###########################

import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import tsp_reader
from solvers import solver
import robot_manager

##########################################################################  
# The main function.
def main():

    # I will modify this when it is necessary. Right now, this code can be ignored.
    if(len(sys.argv) != 2):
        print("Invalid arguments. Please enter the appropriate config file.")
        print("python.exe main.py config.txt")
        return

    # In case there is something wrong with the config file
    config = parse_config(sys.argv[1])
    if len(config) == 0:
        print("The config file was not formatted correctly.")
        return   

    # Random seed   
    np.random.seed(int(config['RND_SEED']))

    # tsp_name is just the file name
    # tsp_c_type is the coordinate system used
    # tsp_points are the points
    # tsp_dist_mat are the integer distances (.tsp uses integer distances)
    tsp_name, tsp_c_type, tsp_points = tsp_reader.read_tsp_file(config['TSP_FILE'])
    tsp_dist_mat = tsp_reader.get_distances(tsp_points, tsp_c_type)

    robo_mgr = robot_manager.RobotMgr(int(config['NUM_ROBS']), tsp_dist_mat)
    num_fails = int(config['NUM_SHDS'])
    fail_prob = config['SHD_PROB']
    robo_mgr.calc_robotpath_init() # Calculate initial paths

    path_steps = 0 # Used to measure the time_steps
    while True:

        path_steps += 1 # Count

        robo_mgr.move_robots() # Make robots move

        if np.random.random() < fail_prob and num_fails > 0 and robo_mgr.num_robots_unfinished() > 1: # Do random probability that one of the robots breaks down
            print(path_steps)
            robo_mgr.shutdown_random_robot() # Shut down a robot
            robo_mgr.calc_robotpath_error() # Reassign robot paths; robots must start at specific depots
            num_fails -= 1

        if robo_mgr.num_robots_unfinished() == 0: # If all robots are finished...
            break # Stop

    print(path_steps)

##########################################################################

##########################################################################  
# Will read the config file and convert it into a dictionary.
# Numeric values are converted into floats.
def parse_config(filename):
    config = {}
    f = open(filename)

    l = f.readline()
    while l:
        l_arr = l.strip().split(" | ")
        try:
            config[l_arr[0]] = float(l_arr[1]) # If it is numeric
        except:
            config[l_arr[0]] = l_arr[1] # If it is not numeric
        l = f.readline()

    return config
##########################################################################  

##########################################################################  
# Uses the main function if run on.
if __name__ == "__main__":
    main()
##########################################################################  