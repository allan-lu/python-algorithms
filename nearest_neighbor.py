##############################################################################################
#
# Calculating the nearest neighbor index with ArcPy and plain Python
#
# Input: spatial data file of elementary schools in Manhattan
# Output: observed mean distance, expected mean distance, nearest neighbor index, z-score
#
# Python Version: Uses Python 3.6 from ArcGIS Pro
#
# Process:
#   With ArcPy:
#       Use AverageNearestNeighbor to get the Average Nearest Neighbor Summary from shapefile
#   With Plain Python:
#       Read GeoJSON file and load into a directory
#       Append each coordinate into a list
#       For each point, create a list of distances from that point and all other points
#       For each list of distances, find the minimum distance and append to a new list
#       Calculate the observed and expected mean distances
#       Calculate the nearest neighbor ratio
#
##############################################################################################

# Math module provides access to mathematical functions such as square root
import math

# ArcPy package lets us perform geoprocessing analyses
import arcpy

# JSON library lets us convert strings to and from json format
import json

# Declare the bounding rectangle area as float variable
given_bounding_rect = 1760000000.0
# From the resulting bounding rectangle when performing Nearest Neighbor Analysis in ArcMap
calc_bounding_rect = 747896332.677655


"""
USING ARCPY
"""


data = "INSERT PATH TO FILE"

# Prints the five average nearest neighbor analysis values
# from the given bounding rectangle area
arcpy.AverageNearestNeighbor_stats(data, "EUCLIDEAN_DISTANCE", "NO_REPORT", given_bounding_rect)

# if no area is provided, ArcPy will calculate its own bounding rectangle area
arcpy.AverageNearestNeighbor_stats(data, "EUCLIDEAN_DISTANCE")


"""
USING PLAIN PYTHON
"""


def get_distance(p, p_list):
    """
    :param p: reference point
    :param p_list: list of points
    :return: list of distances from that point to all other points in the list
    """
    d_list = [math.sqrt(((p_list[index][0]-p[0]) ** 2) + ((p_list[index][1]-p[1])**2))
              for index in range(len(p_list))
              if index - p_list.index(p) != 0]
    return d_list


# Opens the source file
file_name = "INSERT PATH TO FILE"
with open(file_name) as f:
    # Reads and loads data into a dictionary
    data = f.read()
    d = json.loads(data)

    # Creates a list of points from the dictionary
    point_list = [feature["geometry"]["coordinates"] for feature in d["features"]]

    # Creates a list of the distances of each point and their nearest neighbor
    min_distance_list = [min(get_distance(point, point_list)) for point in point_list]

    # Calculates the observed and expected mean minimum distances
    obs_mean_dist = sum(min_distance_list) / len(point_list)
    exp_mean_dist = 0.5/math.sqrt(len(point_list) / given_bounding_rect)

    # Calculates the nearest neighbor ratio
    nn_index = obs_mean_dist / exp_mean_dist

    # Calculates the z-score
    z_score = (obs_mean_dist-exp_mean_dist) * math.sqrt(len(point_list)**2/given_bounding_rect) / 0.26136

    # Prints the average nearest neighbor values
    # from the given bounding area
    print "Average Nearest Neighbor Summary Using Provided Bounding Rectangle"
    print "Observed Mean Distance: %6f ft" % obs_mean_dist
    print "Expected Mean Distance: %6f ft" % exp_mean_dist
    print "Nearest Neighbor Ratio: %6f" % nn_index
    print "z-score: %6f" % z_score

    # using the calculated bounding area
    exp_mean_dist = 0.5 / math.sqrt(len(point_list) / calc_bounding_rect)
    nn_index = obs_mean_dist / exp_mean_dist
    z_score = (obs_mean_dist - exp_mean_dist) * math.sqrt(len(point_list) ** 2 / calc_bounding_rect) / 0.26136
    print "\nAverage Nearest Neighbor Summary Using ArcPy Calculated Bounding Rectangle"
    print "Observed Mean Distance: %6f ft" % obs_mean_dist
    print "Expected Mean Distance: %6f ft" % exp_mean_dist
    print "Nearest Neighbor Ratio: %6f" % nn_index
    print "z-score: %6f" % z_score
