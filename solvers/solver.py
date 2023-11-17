###########################
# solver.py
#
# This is the base class for all solvers.
# This one in particular will generate random strings. It should not be used.
###########################

import numpy as np
import evaluator

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
    def solve(self, robots, pts_visit, pts_start):

        best_pts_list = []
        best_pts_val = -1

        # Sets up the evaluator
        lens = []
        depots = []
        for robot in robots:
            lens.append(max(robot.path_len, 0)) # path_len is -1 if there's no path
            depots.append(robot.depot)
        eval = evaluator.Evaluator(lens, depots, self.dist_mat)

        for x in range(10):
            pts_list = []
            all_pts_visit = pts_visit.copy()
            for i in range(len(robots)):
                if not pts_start: # If no starting points
                    pts_list.append([])
                else:
                    pts_list.append([pts_start[i]])
                    all_pts_visit.remove(pts_start[i])
            
            for pt in all_pts_visit:
                pts_list[np.random.randint(0, len(robots))].append(pt)

            # We will probably need some sort of evaluator class if we're using a GA.
            pts_val = eval.eval_minmax(pts_list)

            if pts_val < best_pts_val or best_pts_val == -1:
                best_pts_val = pts_val
                best_pts_list = pts_list

        print(best_pts_list, best_pts_val)
        return best_pts_list # Should return a list of length num_robots with point arrays.
    ########################################################################## 