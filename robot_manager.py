###########################
# robot_manager.py
#
# The central system that controls the robots.
# It will decide the paths of the robots.
###########################

import robot
from solvers import solver

class RobotMgr:
    
    ##########################################################################  
    # Initializes the robot manager; the number of robots must be specified.
    def __init__(self, num_robots, dist_mat):
        self.robots = []
        self.num_active_robots = num_robots
        for i in range(num_robots):
            self.robots.append(robot.Robot(self))
        
        self.dist_mat = dist_mat # Matrix of distances, to be used by robots
        self.to_visit = list(range(len(dist_mat))) # Points which haven't been visited

        self.solv_init = solver.Solver(dist_mat) # Initial solver

    ##########################################################################  
    # Moves the robots
    def move_robots(self):
        for robot in self.robots: 
            if not robot.is_finished and not robot.is_shutdown:
                robot.move()

    ##########################################################################  
    # Calculates the initial paths of the robots.
    def calc_robotpath_init(self):
        paths = self.solv_init.solve(self.num_active_robots, self.to_visit, [])
        print(paths)
        print(self.dist_mat)
        for i in range(self.num_active_robots):
            self.robots[i].init_path(paths[i])

    ##########################################################################  
    # Recalculates the paths of the currently working robots.
    def calc_robotpath_error(self):
        1 # Will be done tomorrow!
    
    ##########################################################################  
    # Shuts down a random robot.
    def shutdown_random_robot(self):
        1 # Will be done tomorrow!

    ##########################################################################  
    # Removes a point from the "to visit" list.
    def visited_point(self, point):
        self.to_visit.remove(point)

    ##########################################################################  
    # Checks if all of the robots are finished or shut down.
    def check_if_finished(self):
        for robot in self.robots: 
            if not robot.is_finished or robot.is_shutdown:
                return False
        return True