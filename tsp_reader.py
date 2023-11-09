###########################
# tsp_reader.py
#
# This code will read .tsp files.
# I re-used this code from a previous assignment in a different class.
# Works with EUC_2D and GEO coordinates.
###########################

import numpy as np

########################################################################## 
# Reads an input .tsp file.
def read_tsp_file(filename):
    f = open(filename)
    
    point_list = []
    name = ""
    c_type = ""
    PI = 3.141592

    for line in f:
        split_line = line.replace(':',' ').split()
        
        ##########################################
        # Checks
        if len(split_line) == 0:
            continue
        if split_line[0] == 'NAME':
            name = split_line[1]
        if split_line[0] == 'EDGE_WEIGHT_TYPE':
            c_type = split_line[1]
        if split_line[0] == 'EOF':
            break
        ##########################################

        ##########################################
        # New point
        if split_line[0].isnumeric():

            # Euclidean Coordinates
            if c_type == "EUC_2D":
                point_list.append([float(split_line[1]), float(split_line[2])])

            # Latitude/Longitude
            if c_type == "GEO":
                degx = np.floor(float(split_line[1]))
                degy = np.floor(float(split_line[2]))
                minx = float(split_line[1]) - degx
                miny = float(split_line[2]) - degy
                lat = PI * (degx + 5.0 * minx / 3.0) / 180.0
                long = PI * (degy + 5.0 * miny / 3.0) / 180.0
                point_list.append([lat, long])

        ##########################################


    return name, c_type, np.array(point_list) # Return the problem name, coordinate types, and the array of points
########################################################################## 

########################################################################## 
# Gets the distances between all points, so calculations only have to
# be performed once.
def get_distances(points, c_type):

    dist = np.zeros((len(points),len(points)), dtype=int) # dist[i][i] = 0, so no changes needed

    # Euclidean distnace
    if c_type == "EUC_2D": # Splitting this up for the sake of not having to do n^2 variable checks
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                distance = round(np.sqrt(np.sum(np.multiply(points[j] - points[i], points[j] - points[i])))) # round function replicates nint behavior
                dist[i][j] = distance
                dist[j][i] = distance # Symmetrical

    # Global coordinate distance
    elif c_type == "GEO":
        RRR = 6378.388
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                q1 = np.cos(points[i][1] - points[j][1])
                q2 = np.cos(points[i][0] - points[j][0])
                q3 = np.cos(points[i][0] + points[j][0])
                distance = int(RRR * np.arccos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
                dist[i][j] = distance
                dist[j][i] = distance 
    else:
        print("ERROR: Invalid coordinate system type.")
        return None

    return dist # Return a 2D array of distances
########################################################################## 