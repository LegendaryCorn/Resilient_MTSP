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
    if(len(sys.argv) == 200):
        print("Invalid arguments. Please enter the appropriate config file.")
        print("python.exe main.py config.txt")
        return

    # tsp_name is just the file name
    # tsp_c_type is the coordinate system used
    # tsp_points are the points
    # tsp_dist_mat are the integer distances (.tsp uses integer distances)
    tsp_name, tsp_c_type, tsp_points = tsp_reader.read_tsp_file('tsp/burma14.tsp')
    tsp_dist_mat = tsp_reader.get_distances(tsp_points, tsp_c_type)

    robo_mgr = robot_manager.RobotMgr(3, tsp_dist_mat)
    robo_mgr.calc_robotpath_init() # Calculate initial paths

    path_steps = 0 # Used to measure the time_steps
    while True:

        path_steps += 1 # Count

        robo_mgr.move_robots() # Make robots move

        if False: # Do random probability that one of the robots breaks down
            robo_mgr.shutdown_random_robot()
            robo_mgr.calc_robotpath_error() # Reassign robot paths; robots must start at specific depots

        if robo_mgr.check_if_finished(): # If all robots are finished...
            break # Stop

    print(path_steps)

##########################################################################

##########################################################################  
# Uses the main function if run on.
if __name__ == "__main__":
    main()
##########################################################################  