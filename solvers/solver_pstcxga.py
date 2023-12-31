###########################
# solver_tcxga.py
#
# Solver that uses a GA with TCX crossover.
###########################

from solvers import solver
import evaluator
import numpy as np

class Individual_psTCXGA:

    ########################################################################## 
    # Initializes the individual. Needs work.
    def __init__(self, chrom):
        self.chrom = chrom
        self.fitness = -1 # -1 means that the fitness is unspecified
        # Note that since I'm using a rank based selection algorithm, I'm just
        # going to use the path length as the fitness. Fitness should be minimized.
    ########################################################################## 

class Solver_psTCXGA(solver.Solver):

    ########################################################################## 
    # Initializes a solver; distance matrix and point positions included.
    def __init__(self, dist_mat, pts_pos):
        self.dist_mat = dist_mat
        self.pts_pos = pts_pos
    ##########################################################################

    ##########################################################################  
    # The new solver.
    # pts_visit is the points to be visited; this should contain all points for the initial run.
    # pts_start is the points to start at. This should be an empty array [] for the initial run.
    def solve(self, robots, pts_visit, pts_start, config):

        # GA parameters (will need external values)
        pop_size = config['PS_POP_SIZE']

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

        pop = self.genetic_algo(pts, pts_start, eval, robots, config)

        # From our final population, find the best individual, and return it.
        return chrom_to_path(pop[len(pop) - 1].chrom, pts_start, len(robots)), pop[len(pop) - 1].fitness # Should return a list of length num_robots with point arrays.
    ########################################################################## 

    ########################################################################## 
    # Contains all of the genetic algorithm operations.
    def genetic_algo(self, pts, pts_start, eval, robots, config):

        # Config
        pop_size = int(config['PS_POP_SIZE'])
        gen_count = int(config['PS_NUM_GENS'])
        p_crossover = config['PS_CRS_PROB']
        p_mutation1 = config['PS_MU1_PROB']
        p_mutation2 = config['PS_MU2_PROB']
        replacement_percent = config['PS_REP_PERC']
        rand_prop = config['PS_RND_PROP']


        # Sets up our new points
        lost_pts = pts.copy()
        paths = []
        for r in range(len(robots)):
            r_path = robots[r].path.copy()
            if len(pts_start) > 0:
                r_path.remove(pts_start[r])
            paths.append(r_path)
            for p in r_path:
                lost_pts.remove(p)

        # Sets up our population
        pop = []

        prop = int(pop_size * rand_prop)

        for p in range(pop_size - prop):
            ind = Individual_psTCXGA(path_to_chrom(rand_path_insert(lost_pts, paths)))
            ind.fitness = eval.eval_minmax(chrom_to_path(ind.chrom, pts_start, len(robots)))
            pop.append(ind)
        for p in range(prop):
            ind = Individual_psTCXGA(rand_chrom(pts, len(robots)))
            ind.fitness = eval.eval_minmax(chrom_to_path(ind.chrom, pts_start, len(robots)))
            pop.append(ind)
        pop = sort_pop(pop)

        # Do the genetic algorithm
        for gen in range(gen_count):
            children = []

            # Selection 
            # Assumes population is sorted worst to best!
            for i in range(pop_size):
                roulette = np.random.randint(0, pop_size * (pop_size + 1) / 2)
                r = 0
                for j in range(pop_size):
                    if r >= roulette:
                        break
                    r += j + 2
                ind = Individual_psTCXGA(pop[j].chrom.copy())
                children.append(ind)
            
            # Crossover
            for i in range(int(pop_size / 2)):
                ii = 2 * i
                if(np.random.random() < p_crossover):
                    new_chrom_1 = self.tcx_crossover(children[ii].chrom, children[ii + 1].chrom, len(robots))
                    new_chrom_2 = self.tcx_crossover(children[ii + 1].chrom, children[ii].chrom, len(robots))
                    children[ii].chrom = new_chrom_1
                    children[ii + 1].chrom = new_chrom_2
            
            # Mutation
            for i in range(pop_size):

                sep = children[i].chrom.index(-1)

                # First chromosome part mutation
                if(np.random.random() < p_mutation1):
                    swap = np.random.randint(0, sep, 2)
                    temp0 = children[i].chrom[swap[0]]
                    temp1 = children[i].chrom[swap[1]]
                    children[i].chrom[swap[0]] = temp1
                    children[i].chrom[swap[1]] = temp0
                
                # Second chromosome part mutation
                if(np.random.random() < p_mutation2):
                    swap = np.random.randint(0, len(robots), 2)
                    temp0 = children[i].chrom[sep + 1 + swap[0]]
                    temp1 = children[i].chrom[sep + 1 + swap[1]]
                    children[i].chrom[sep + 1 + swap[0]] = temp1
                    children[i].chrom[sep + 1 + swap[1]] = temp0
            
            # Replacement
            for child in children:
                child.fitness = eval.eval_minmax(chrom_to_path(child.chrom, pts_start, len(robots)))
            children = sort_pop(children)
            num_to_replace = int(pop_size * replacement_percent)
            best_worst = []
            for i in range(num_to_replace):
                best_worst.append(pop[i])
                best_worst.append(children[pop_size - 1 - i]) # Best performer is last!
            best_worst = sort_pop(best_worst)
            for i in range(num_to_replace):
                pop[i] = best_worst[2 * num_to_replace - 1 - i]
            pop = sort_pop(pop)

        return pop
    ##########################################################################  

    ##########################################################################
    # TCX crossover, contained in its own function because its really long.
    def tcx_crossover(self, chrom_mom, chrom_dad, num_robots):
        
        sep = chrom_mom.index(-1)
        new_dad = chrom_dad[0:sep].copy()
        paths = chrom_to_path(chrom_mom, [], num_robots)
        new_chrom = []
        new_mom = []

        for i in range(len(paths)):
            num1 = np.random.randint(0, len(paths[i]))
            num2 = np.random.randint(0, len(paths[i]))

            if num1 > num2:
                new_mom.append(paths[i][num2:num1+1].copy())
            else:
                new_mom.append(paths[i][num1:num2+1].copy())
            
            for gene in new_mom[i]:
                new_dad.remove(gene)
        
        if(len(new_dad) != 0):
            dad_points = np.sort(np.random.randint(0, len(new_dad), num_robots - 1))

        x = 0
        for j in range(len(new_dad)):
            while x < num_robots - 1 and dad_points[x] <= j:
                x += 1
            new_mom[x].append(new_dad[j])

        new_chrom = path_to_chrom(new_mom)

        return new_chrom
    ##########################################################################


########################################################################## 
# Sorts a population of individuals based on their fitness, from highest to lowest route length.
# Highest to lowest route length will make rank roulette selection easier (weight = 1 + index)
def sort_pop(pop):
    new_pop = []
    fit_arr = []

    for ind in pop:
        fit_arr.append(ind.fitness)

    inds = np.flip(np.argsort(fit_arr))

    for ind in inds:
        new_pop.append(pop[ind])

    return new_pop
########################################################################## 

########################################################################## 
# Converts a chromosome into a list of lists containing each path.
def chrom_to_path(chrom, pts_start, num_paths):
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
        if j >= route_lens[i] and i < len(paths) - 1:
            i += 1
            j = 0
        paths[i].append(chrom_val)
        j += 1
    return paths
########################################################################## 

########################################################################## 
# Converts a path into a chromosome.
def path_to_chrom(paths):

    chrom = []
    for path in paths:
        for i in path:
            chrom.append(i)
    
    chrom.append(-1)
    for path in paths:
        chrom.append(len(path))

    return chrom
########################################################################## 

##########################################################################
# Generates a random two-part chromosome
def rand_chrom(pts_list, n):
    
    chrom = pts_list.copy()
    np.random.shuffle(chrom)

    route_len = rand_sum(len(chrom), n)

    chrom.append(-1) # Signifies separation of two chromosomes
    for r_length in route_len:
        chrom.append(r_length)

    return chrom
##########################################################################

##########################################################################
# Inserts several points randomly into a list of paths.
def rand_path_insert(pts_to_add, paths):
    
    new_paths = []
    for path in paths:
        new_paths.append(path.copy())

    for pt in pts_to_add:
        i = np.random.randint(0, len(new_paths))
        j = np.random.randint(0, len(new_paths[i]) + 1)

        new_paths[i].insert(j, pt)

    return new_paths
##########################################################################

##########################################################################
# Generates a random set of n numbers that sum to sum_num
# All numbers are greater than 0
def rand_sum(sum_num, n):

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