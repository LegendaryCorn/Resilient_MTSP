###########################
# robot_manager.py
#
# The central system that controls the robots.
# It will decide the paths of the robots.
###########################

import robot
from solvers import solver_tcxga
import numpy as np

class RobotMgr:
    
    ##########################################################################  
    # Initializes the robot manager; the number of robots must be specified.
    def __init__(self, num_robots, dist_mat):
        self.robots = []
        self.active_robots = list(range(num_robots))
        for i in range(num_robots):
            self.robots.append(robot.Robot(self, i))
        
        self.dist_mat = dist_mat # Matrix of distances, to be used by robots
        self.to_visit = list(range(len(dist_mat))) # Points which haven't been visited

        self.solv_init = solver_tcxga.Solver_TCXGA(dist_mat) # Initial solver

    ##########################################################################  
    # Moves the robots
    def move_robots(self):
        for robot in self.robots: 
            if not robot.is_finished and not robot.is_shutdown:
                robot.move()

    ##########################################################################  
    # Calculates the initial paths of the robots.
    def calc_robotpath_init(self):
        act_robo = []
        for active_robot_ind in self.active_robots:
            act_robo.append(self.robots[active_robot_ind])
        paths = self.solv_init.solve(act_robo, self.to_visit, [])

        for i in range(len(self.active_robots)):
            self.robots[self.active_robots[i]].init_path(paths[i])

    ##########################################################################  
    # Recalculates the paths of the currently working robots.
    def calc_robotpath_error(self):

        starting_pts = []
        act_robo = []
        for active_robot_ind in self.active_robots:
            starting_pts.append(self.robots[active_robot_ind].path[0])
            act_robo.append(self.robots[active_robot_ind])

        paths = self.solv_init.solve(act_robo, self.to_visit, starting_pts)

        for i in range(len(self.active_robots)):
            self.robots[self.active_robots[i]].modify_path(paths[i])
    
    ##########################################################################  
    # Shuts down a random robot.
    def shutdown_random_robot(self):

        # If there's only one active robot, then don't shut anything down.
        if len(self.active_robots) > 1:

            # This is just to assure that the robot is still running
            robo_down = self.active_robots[np.random.randint(0, len(self.active_robots))]
            
            self.robots[robo_down].is_shutdown = True
            self.active_robots.remove(robo_down)
            print(str(robo_down) + " shut down")

    ##########################################################################  
    # Removes a point from the "to visit" list.
    def visited_point(self, point):
        print(str(point) + " visited")
        self.to_visit.remove(point)

    ##########################################################################  
    # Checks the number of robots that are not finished or shut down.
    def num_robots_unfinished(self):
        r = 0
        for robot in self.robots: 
            if not robot.is_finished and not robot.is_shutdown:
                r += 1
        return r