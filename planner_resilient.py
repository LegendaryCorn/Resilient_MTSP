###########################
# planner_resilient.py
#
# The code that will test the new methods.
# Needs the paths to be initialized.
###########################

import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import tsp_reader
import robot_manager

# Initializes the paths
init_paths = [[29, 13, 16, 27, 22, 32, 46, 48, 39, 44, 75, 84, 90, 19, 7, 5, 10], [63, 80, 73, 69, 68, 72, 101, 91, 81, 55, 42, 11, 14, 6, 0, 18, 30, 50, 79, 76, 70], [38, 15, 35, 41, 65, 86, 93, 94, 87, 98, 100, 97, 88, 61, 49, 54, 59], [2, 1, 4, 3, 60, 64, 37, 12, 33, 34, 24, 102, 21, 28, 17, 25, 8], [78, 71, 51, 40, 36, 45, 67, 95, 96, 77, 58, 23, 26, 52, 62, 92, 85, 83, 82], [103, 9, 20, 47, 104, 66, 31, 43, 53, 56, 74, 89, 99, 57]]

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

    # Initialize the paths
    for i in range(len(robo_mgr.active_robots)):
            robo_mgr.robots[robo_mgr.active_robots[i]].init_path(init_paths[i])

    path_steps = 0 # Used to measure the time_steps
    while True:

        path_steps += 1 # Count

        robo_mgr.move_robots() # Make robots move

        if path_steps == 2000: # I will instead do this after a set amount of time
            robo_mgr.shutdown_random_robot() # Shut down a robot
            t_start = time.time()
            robo_mgr.calc_robotpath_error() # Reassign robot paths; robots must start at specific depots
            t_end = time.time()
            print(t_end - t_start)

            # Record points
            pts_array = np.zeros((len(robo_mgr.to_visit) + len(robo_mgr.active_robots), 2))
            for pt in range(len(robo_mgr.to_visit)):
                pts_array[pt] = tsp_points[robo_mgr.to_visit[pt] - 1]

            # Record paths
            path_arrays = []
            ind = 0
            for robot in robo_mgr.active_robots:
                robo = robo_mgr.robots[robot]
                full_path = robo.path + [robo.depot]
                path_pts = np.zeros((len(full_path), 2))
                for p in range(len(full_path)):
                    path_pts[p] = tsp_points[full_path[p] - 1]
                path_arrays.append(path_pts)
                pts_array[len(robo_mgr.to_visit) + ind] = tsp_points[robo.depot - 1]
                ind += 1

            num_fails -= 1

        if robo_mgr.num_robots_unfinished() == 0: # If all robots are finished...
            break # Stop

    print(path_steps)

    plt.scatter(pts_array[:,0], pts_array[:,1])
    for path in path_arrays:
        plt.plot(path[:,0],path[:,1])
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