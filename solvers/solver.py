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
    # Initializes a solver; distance matrix and point positions included.
    def __init__(self, dist_mat, pts_pos):
        self.dist_mat = dist_mat
        self.pts_pos = pts_pos
    ########################################################################## 

    ##########################################################################  
    # The base solver.
    # pts_visit is the points to be visited; this should contain all points for the initial run.
    # pts_start is the points to start at. This should be an empty array [] for the initial run.
    def solve(self, robots, pts_visit, pts_start, config):

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

            chrom = pts_visit.copy()

            for i in range(len(robots) - 1):
                chrom.append(-1 * (i+1))
            
            for pt_st in pts_start:
                chrom.remove(pt_st)
                    
            np.random.shuffle(chrom)
            pts_list = self.chrom_to_path(chrom, pts_start, len(robots))

            # We will probably need some sort of evaluator class if we're using a GA.
            pts_val = eval.eval_minmax(pts_list)

            if pts_val < best_pts_val or best_pts_val == -1:
                best_pts_val = pts_val
                best_pts_list = pts_list

        print(best_pts_list, best_pts_val)
        return best_pts_list # Should return a list of length num_robots with point arrays.
    ########################################################################## 

    ########################################################################## 
    # Converts a chromosome into a list of lists containing each path.
    def chrom_to_path(self, chrom, pts_start, num_paths):
        paths = []

        for x in range(num_paths):
            if pts_start:
                paths.append([pts_start[x]])
            else:
                paths.append([])

        i = 0
        for chrom_val in chrom:
            if chrom_val < 0:
                i += 1
            else:
                paths[i].append(chrom_val)
        return paths
    ########################################################################## 