###########################
# solver_cmmtsp.py
#
# Solver that uses a clustering based market approach.
###########################

from solvers import solver
import evaluator
import numpy as np

class Solver_CMMTSP(solver.Solver):

    ########################################################################## 
    # Initializes a solver; distance matrix and point positions included.
    def __init__(self, dist_mat, pts_pos):
        self.dist_mat = dist_mat
        self.pts_pos = pts_pos
    ########################################################################## 

    ##########################################################################  
    # The CM-MTSP solver.
    # This solver WILL NOT work on the initialization step. It needs pts_start.
    def solve(self, robots, pts_visit, pts_start, config):

        # Sets up the evaluator
        lens = []
        depots = []
        for robot in robots:
            lens.append(max(robot.path_len, 0)) # path_len is -1 if there's no path
            depots.append(robot.depot)
        eval = evaluator.Evaluator(lens, depots, self.dist_mat)

        # Specifies the points that need to be visited
        pts = pts_visit.copy()      
        for pt_st in pts_start:
            pts.remove(pt_st)

        clustered_pts = self.k_means(pts, len(robots))

        # From our final population, find the best individual, and return it.
        return []
    ########################################################################## 

    ########################################################################## 
    # Calculates the clusters given a set of points and a number of clusters.
    def k_means(self, pts, n):

        old_means = np.zeros((n, len(self.pts_pos[0])))
        new_means = np.zeros((n, len(self.pts_pos[0])))
        clusters = []

        init_means = np.random.choice(len(pts), n)
        # Pick random starting points for means
        for i in range(n):
            new_means[i] = self.pts_pos[init_means[i]].copy()

        while not np.all(np.equal(old_means, new_means)):

            clusters = []
            for i in range(n):
                clusters.append([])
            closest_pt = []

            for pt in pts:
                pt_pos = self.pts_pos[pt]
                closest = -1
                closest_dist = np.inf
                for i in range(n):
                    sub = pt_pos - new_means[i]
                    if np.dot(sub, sub) < closest_dist:
                        closest = i
                        closest_dist = np.dot(sub, sub)
                closest_pt.append(closest)

            cluster_means = np.zeros((n, len(self.pts_pos[0])))

            for c in range(len(closest_pt)):
                clusters[closest_pt[c]].append(pts[c])
                cluster_means[closest_pt[c]] += self.pts_pos[pts[c]]
            
            old_means = new_means.copy()
            for i in range(n):
                new_means[i] = cluster_means[i] / len(clusters[i])

        print(clusters, new_means)

        return clusters
    ########################################################################## 