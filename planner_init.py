###########################
# planner_init.py
#
# This code will initialize a path given a seed. Used so that we
# don't have to run the initial GA multiple times per seed.
###########################

import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import tsp_reader
import robot_manager

##########################################################################  
# The main function.
def main():

    # I will modify this when it is necessary. Right now, this code can be ignored.
    if(len(sys.argv) != 2):
        print("Invalid arguments. Please enter the appropriate config file.")
        print("python.exe run.py config.txt")
        return

    # In case there is something wrong with the config file
    config = parse_config(sys.argv[1])
    if len(config) == 0:
        print("The config file was not formatted correctly.")
        return   

    # Random seed   
    np.random.seed(int(config['EN_RND_SEED']))

    # tsp_name is just the file name
    # tsp_c_type is the coordinate system used
    # tsp_points are the points
    # tsp_dist_mat are the integer distances (.tsp uses integer distances)
    tsp_name, tsp_c_type, tsp_points = tsp_reader.read_tsp_file(config['EN_TSP_FILE'])
    tsp_dist_mat = tsp_reader.get_distances(tsp_points, tsp_c_type)

    robo_mgr = robot_manager.RobotMgr(int(config['EN_NUM_ROBS']), tsp_dist_mat, tsp_points, config)
    num_fails = int(config['EN_NUM_SHDS'])
    fail_prob = config['EN_SHD_PROB']

    t_start = time.time()
    robo_mgr.calc_robotpath_init() # Calculate initial paths
    t_end = time.time()

    print(t_end - t_start)

    plt.scatter(tsp_points[:,0], tsp_points[:,1])

    for robot in robo_mgr.robots:
        full_path = [robot.depot] + robot.path
        path_pts = np.zeros((len(full_path) + 1, 2))
        for p in range(len(full_path)):
            path_pts[p] = tsp_points[full_path[p] - 1]
        path_pts[len(full_path)] = tsp_points[robot.depot - 1]
        plt.plot(path_pts[:,0], path_pts[:,1])

    plt.show()

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