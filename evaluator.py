###########################
# evaluator.py
#
# This will evaluate an mTSP problem and will output an evaluation.
# This evaluation can be used on the solvers.
# MUST include the LKH library.
###########################

import lkh

# Each run of the solver should have its own evaluator that is based on the current state.
class Evaluator:

    ########################################################################## 
    # Initializes the evaluator.
    # curr_path_len is how much of the current path the drone has left.
    # depot_list is the depot of each drone.
    # dist_mat is the distance matrix
    def __init__(self, curr_path_len, depot_list, dist_mat, pts_pos):
        self.curr_path_len = curr_path_len.copy()
        self.depot_list = depot_list.copy()
        self.dist_mat = dist_mat.copy()
        self.pts_pos = pts_pos
    ########################################################################## 

    ########################################################################## 
    # Returns the longest drone path; this drone path is to be minimized.
    def eval_minmax(self, paths):
        path_lengths = self.curr_path_len.copy()
        temp_depot_list = self.depot_list.copy()

        for i in range(len(paths)):
            
            if(len(paths[i]) < 1):
                return float('inf')

            if(temp_depot_list[i]) == -1: # for the case where the depots haven't been initialized
                temp_depot_list[i] = paths[i][0]

            for j in range(len(paths[i])):

                if j == len(paths[i]) - 1:
                    path_lengths[i] += self.dist_mat[paths[i][j]][temp_depot_list[i]]
                else:
                    path_lengths[i] += self.dist_mat[paths[i][j]][paths[i][j+1]]

        return max(path_lengths)
    ########################################################################## 

    ##########################################################################
    # Evaluates a set of nodes using LKH; note that this requires a starting point and a depot.
    # Add is equal to the robot's remaining path.
    def eval_lkh(self, start, depot, nodes, add):

        num_nodes = 2 + len(nodes)
        node_list = nodes.copy()
        node_list.insert(0,depot)
        node_list.insert(1,start)

        # Create a fake .tsp file
        problem_tsp  = "NAME: problem\n"
        problem_tsp += "TYPE: TSP\n"
        problem_tsp += "DIMENSION: " + str(num_nodes) + "\n"
        problem_tsp += "EDGE_WEIGHT_TYPE: EUC_2D\n"
        problem_tsp += "FIXED_EDGES_SECTION\n"
        problem_tsp += "1 2\n" # This guarantees that our robot starts at the start and ends at the depot
        problem_tsp += "-1\n"
        problem_tsp += "NODE_COORD_SECTION\n"
        i = 1
        for node in node_list:
            problem_tsp += str(i) + " " + str(int(self.pts_pos[node][0])) + " " + str(int(self.pts_pos[node][1])) + "\n"
            i += 1
        problem_tsp += "EOF"

        prob = lkh.LKHProblem.parse(problem_tsp)
        sol = lkh.solve(solver='lkh/LKH-3.exe', problem=prob)

        ind = sol[0].index(2)

        total_len = add
        arr = []
        for i in range(num_nodes - 1):
            i0 = (i + ind) % num_nodes
            i1 = (i + ind + 1) % num_nodes
            total_len += self.dist_mat[node_list[sol[0][i0] - 1]][node_list[sol[0][i1] - 1]]
            
            if i != 0:
                arr.append(node_list[sol[0][i0] - 1])

        return arr, total_len
    ##########################################################################