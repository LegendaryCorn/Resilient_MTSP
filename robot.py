###########################
# robot.py
#
# A robot that moves around.
###########################

class Robot:
    
    ##########################################################################  
    # Creates the robot; -1 indicates that the robot has nothing.
    def __init__(self, mgr, id):
        self.depot = -1 # Where the robot starts; it will head towards this if its path is empty.
        self.from_point = -1 # Where the robot is coming from. It has visited this point.
        self.path_len = -1 # The length of the path to travel along.
        self.id = id

        self.is_shutdown = False # Whether or not the robot suffered a failure
        self.is_returning = False # True if the robot is returnin to its depot.
        self.is_finished = False # Whether or not the robot finished
        
        self.path = [] # The current path to follow
        self.mgr = mgr # The robot manager

    ##########################################################################  
    # This will create initial paths for the robot; it will define the depot.
    def init_path(self, path):
        self.path = path.copy()
        start_point = self.path[0] # The start point

        self.depot = start_point
        self.from_point = start_point
        self.mgr.visited_point(start_point)
        self.path.remove(self.path[0])
        self.path_len = self.mgr.dist_mat[self.from_point][self.path[0]]

    ##########################################################################
    # This will change the path of the robot.
    def modify_path(self, new_path):
        path_entered = new_path.copy()

        if self.path[0] != path_entered[0]:
            path_entered.insert(0, self.path[0])

        self.path = path_entered

    ##########################################################################  
    # The robot will move. If the robot needs to change its path, it will do so.
    # This will assume that shutdown and finished have been checked.
    def move(self):

        # If movement is valid:
        if len(self.path) != 0 and self.from_point != -1:
            self.path_len -= 1

            if self.path_len == 0 and self.is_returning: # If it is finished
                self.is_finished = True
                print(str(self.id) + " finished")
    
            elif self.path_len == 0: # If path has been completed:
                # Report finished point
                self.mgr.visited_point(self.path[0])
                
                # Go to new point
                self.from_point = self.path[0]
                self.path.remove(self.path[0])

                # If there's no more points to check
                if len(self.path) == 0:
                    self.is_returning = True
                    self.path.append(self.depot)
                    self.mgr.active_robots.remove(self.id)
                    print(str(self.id) + " returning")
                
                self.path_len = self.mgr.dist_mat[self.from_point][self.path[0]]