###########################
# evaluator.py
#
# This will evaluate an mTSP problem and will output an evaluation.
# This evaluation can be used on the solvers.
###########################

# Each run of the solver should have its own evaluator that is based on the current state.
class Evaluator:

    ########################################################################## 
    # Initializes the evaluator.
    # curr_path_len is how much of the current path the drone has left.
    # depot_list is the depot of each drone.
    # dist_mat is the distance matrix
    def __init__(self, curr_path_len, depot_list, dist_mat):
        self.curr_path_len = curr_path_len.copy()
        self.depot_list = depot_list.copy()
        self.dist_mat = dist_mat.copy()
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