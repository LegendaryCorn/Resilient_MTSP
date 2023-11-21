###########################
# solver_tcxga.py
#
# Solver that uses a GA with TCX crossover.
###########################

from solvers import solver
import evaluator
import numpy as np

class Individual_TCXGA:

    ########################################################################## 
    # Initializes the individual. Needs work.
    def __init__(self):
        self.chrom = []
        self.fitness = -1
    ########################################################################## 

class Solver_TCXGA(solver.Solver):

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

            chrom = pts_visit.copy()
            
            for pt_st in pts_start:
                chrom.remove(pt_st)
                    
            np.random.shuffle(chrom)

            route_len = self.rand_sum(len(chrom), len(robots))

            chrom.append(-1) # Signifies separation of two chromosomes
            for r_length in route_len:
                chrom.append(r_length)
            print(chrom)
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

        sep = chrom.index(-1)
        routes = chrom[0:sep]
        route_lens = chrom[sep+1:len(chrom)]

        for x in range(num_paths):
            if pts_start:
                paths.append([pts_start[x]])
            else:
                paths.append([])

        i = 0
        j = 0
        for chrom_val in routes:
            if j >= route_lens[i]:
                i += 1
                j = 0
            else:
                paths[i].append(chrom_val)
                j += 1
        return paths
    ########################################################################## 

    ##########################################################################
    # Generates a random set of n numbers that sum to sum_num
    # All numbers are greater than 0
    def rand_sum(self, sum_num, n):

        arr = []
        sums = []
        for x in range(sum_num - 2 * n + 1):
            arr.append(0)

        sums.append(1)
        for y in range(n - 1):
            arr.append(1)
            sums.append(1)
        np.random.shuffle(arr)

        i = 0
        for a in arr:
            if a == 1:
                i += 1
            sums[i] += 1

        return sums
    ##########################################################################