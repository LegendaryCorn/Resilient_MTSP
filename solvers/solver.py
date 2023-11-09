###########################
# solver.py
#
# This is the base class for all solvers.
# This one in particular will generate random strings. It should not be used.
###########################

import numpy as np

class Solver:
    
    ########################################################################## 
    # Initializes a solver; distance matrix included.
    def __init__(self, dist_mat):
        self.dist_mat = dist_mat
    ########################################################################## 

    ##########################################################################  
    # The base solver.
    # pts_visit is the points to be visited; this should contain all points for the initial run.
    # pts_start is the points to start at. This should be an empty array [] for the initial run.
    def solve(self, num_robots, pts_visit, pts_start):

        all_pts_visit = pts_visit.copy()
        pts_list = []

        for i in range(num_robots):
            if not pts_start: # If no starting points
                pts_list.append([])
            else:
                pts_list.append([pts_start[i]])

        
        for pt in pts_visit:
            pts_list[np.random.randint(0, num_robots)].append(pt)

        # We will probably need some sort of evaluator class if we're using a GA.

        return pts_list # Should return a list of length num_robots with point arrays.
    ########################################################################## 