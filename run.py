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
    tsp_name, tsp_c_type, tsp_points = tsp_reader.read_tsp_file('tsp/berlin52.tsp')
    tsp_dist_mat = tsp_reader.get_distances(tsp_points, tsp_c_type)
    print(tsp_points, tsp_dist_mat)


    # Testing code

    solv = solver.Solver(tsp_dist_mat)
    num_robots = 5
    pts_to_visit = list(range(0, len(tsp_points)))
    paths = solv.solve(num_robots, pts_to_visit, [])
    print(paths)


    # Placeholder code
    
    # Calculate initial paths

    path_steps = 0 # Used to measure the time_steps
    while True:

        # Make robots move
        
        if False: # Do random probability that one of the robots breaks down
            1 # Reassign robot paths; robots must start at specific depots
        
        if True: # If robots have all reached their goals or they all have crashed
            break # Stop

        path_steps += 1

##########################################################################

##########################################################################  
# Uses the main function if run on.
if __name__ == "__main__":
    main()
##########################################################################  