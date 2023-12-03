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
        eval = evaluator.Evaluator(lens, depots, self.dist_mat, self.pts_pos)

        # Specifies the points that need to be visited
        pts = pts_visit.copy()      
        for pt_st in pts_start:
            pts.remove(pt_st)

        # 3 Steps

        clustered_pts = self.k_means(pts, len(robots)) # Clustering

        paths, paths_len = self.auction(clustered_pts, robots, pts_start, eval) # Auctioning

        improved_paths, improved_paths_len = self.path_improve(paths, paths_len, robots, pts_start, eval) # Improving

        # Return the paths
        return improved_paths
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
                if len(clusters[i]) == 0:
                    new_means[i] = old_means[i]
                else:
                    new_means[i] = cluster_means[i] / len(clusters[i])

        return clusters
    ########################################################################## 
    
    ########################################################################## 
    # The auction function
    def auction(self, clusters, robots, pts_start, eval):

        auctioned_paths = []
        auctioned_path_lens = []
        auctioned_clusters = []
        unassigned_clusters = list(range(len(clusters)))
        for robot in robots:
            auctioned_paths.append([])
            auctioned_path_lens.append(-1)
            auctioned_clusters.append(-1)

        for c in unassigned_clusters:
            cluster = clusters[c]
            bids = []
            for i in range(len(robots)):
                p, p_len = eval.eval_lkh(pts_start[i], robots[i].depot, cluster, robots[i].path_len)

                if(auctioned_clusters[i] == -1):
                    bids.append([p, p_len])
                else:
                    if p_len < auctioned_path_lens[i]:
                        bids.append([p, p_len])
                    else:
                        bids.append([[], -1]) # No bid

            # Give to lowest bidder
            min_cost = np.inf
            min_ind = -1
            for b in range(len(bids)):
                if(bids[b][1] < min_cost and bids[b][1] != -1):
                    min_cost = bids[b][1]
                    min_ind = b

            if(auctioned_clusters[min_ind] == -1): # If the robot isn't exchanging
                auctioned_paths[min_ind] = bids[min_ind][0]
                auctioned_path_lens[min_ind] = bids[min_ind][1]
                auctioned_clusters[min_ind] = c
            else:
                unassigned_clusters.append(auctioned_clusters[min_ind])
                auctioned_paths[min_ind] = bids[min_ind][0]
                auctioned_path_lens[min_ind] = bids[min_ind][1]
                auctioned_clusters[min_ind] = c

        return auctioned_paths, auctioned_path_lens
    ########################################################################## 

    ########################################################################## 
    # Improvement function; only does MinMax improvement (we don't have variable speed)
    def path_improve(self, paths, paths_len, robots, pts_start, eval):

        new_paths = paths.copy()
        new_paths_len = paths_len.copy()

        cont = True
        while cont:
            
            cont = False
            max_len = np.max(new_paths_len)
            max_r = np.argmax(new_paths_len)

            for r in range(len(robots)):
                
                if r == max_r:
                    continue

                swap1, swap1_len = eval.eval_lkh(pts_start[r], robots[r].depot, new_paths[max_r], robots[r].path_len)
                swap2, swap2_len = eval.eval_lkh(pts_start[max_r], robots[max_r].depot, new_paths[r], robots[max_r].path_len)

                if swap1_len < max_len and swap2_len < max_len:
                    new_paths[r] = swap1
                    new_paths_len[r] = swap1_len
                    new_paths[max_r] = swap2
                    new_paths_len[max_r] = swap2_len
                    cont = True
                    break

        return paths, paths_len
    ########################################################################## 