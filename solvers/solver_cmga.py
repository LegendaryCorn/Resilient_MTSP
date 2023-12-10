###########################
# solver_cmga.py
#
# Solver that combines the clustering based market approach AND the GA approach.
# This will just reuse the algorithms; makes it so that this file isn't huge.
###########################

from solvers import solver
from solvers import solver_pstcxga
from solvers import solver_cmmtsp
import robot
import robot_manager
import evaluator
import numpy as np

class Individual_CMGA:

    ########################################################################## 
    # Initializes the individual.
    def __init__(self, chrom):
        self.chrom = chrom
        self.fitness = -1 # -1 means that the fitness is unspecified
        # Note that since I'm using a rank based selection algorithm, I'm just
        # going to use the path length as the fitness. Fitness should be minimized.
    ########################################################################## 

class Solver_CMGA(solver.Solver):

    ########################################################################## 
    # Initializes a solver; distance matrix and point positions included.
    def __init__(self, dist_mat, pts_pos):
        self.dist_mat = dist_mat
        self.pts_pos = pts_pos
    ########################################################################## 

    ##########################################################################  
    # The CMGA solver.
    # This solver WILL NOT work on the initialization step. It needs pts_start.
    def solve(self, robots, pts_visit, pts_start, config):

        # CMM
        solv_cmm = solver_cmmtsp.Solver_CMMTSP(self.dist_mat, self.pts_pos)
        cmm_best, cmm_len = solv_cmm.solve(robots, pts_visit, pts_start, config)

        # Fake set of robots for the SGA
        i = 0
        fake_robots = []
        fake_robot_mgr = robot_manager.RobotMgr(len(robots), self.dist_mat, self.pts_pos, config) # The robots need a robot manager
        for robo in robots:
            fake_robo = robot.Robot(fake_robot_mgr, robo.id)
            fake_robo.path = robo.path.copy()
            fake_robo.path_len = robo.path_len
            fake_robo.depot = robo.depot
            fake_robo.from_point = robo.from_point
            fake_robo.modify_path(cmm_best[i])
            fake_robots.append(fake_robo)
            i += 1

        # Seeded Genetic Algorithm
        solv_sga = solver_pstcxga.Solver_psTCXGA(self.dist_mat, self.pts_pos)
        sga_best, sga_len = solv_sga.solve(fake_robots, pts_visit, pts_start, config)

        # Return the best path
        return sga_best, sga_len
    ########################################################################## 