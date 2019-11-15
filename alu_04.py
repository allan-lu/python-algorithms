###########################################################################
#
# Allan Lu
# 10/02/2019
# GTECH 731 - Green
# Homework 4
#
# Calculating the centroid of a polygon composed of polygon lots
#
# Input: GeoJSON polygon file of coordinates data from PLUTO
# Output: Centroid point of the overall polygon, graphed
#
# Process:
#   Define area function
#   Define decomposed centroid function
#   Define centroid function
#   Read polygon GeoJSON into dictionary
#       Plot polygon
#       Find and plot centroid of polygon
#   Display graph
#
###########################################################################

# json library lets us convert strings to and from json format
import json

# Imports matplotlib for creating plots
import matplotlib.pyplot as plt


# Calculates the area of the polygon
# Parameter: a list of points
# The first and last coordinates in the list must be the same
# aka (x[0],y[0]) == (x[n], y[n])
def find_area(points):
    # Creates two lists of only the x and y values of a coordinate
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    # Calculate the area
    area = 0
    for i in range(len(x) - 1):
        area += x[i] * y[i + 1] - x[i + 1] * y[i]
    area /= 2
    return area


# Calculates the centroids of each smaller polygon that makes up the larger overall selection
# Parameter: a list of points/coordinates
def find_decomposed_centroid(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    # Finds the area of the polygon
    area = find_area(points)

    # Calculate the x and y values of the centroid
    c_x = 0
    c_y = 0
    for i in range(len(x) - 1):
        c_x += (x[i] + x[i + 1]) * (x[i] * y[i + 1] - x[i + 1] * y[i])
        c_y += (y[i] + y[i + 1]) * (x[i] * y[i + 1] - x[i + 1] * y[i])
    c_x /= 6 * area
    c_y /= 6 * area

    # Define the centroid as a list containing the x and y value
    c_point = [c_x, c_y]
    return c_point


# Calculates the centroid of the overall polygon
# Parameter: a polygon dictionary in geojson format
def find_geometric_centroid(polygon):
    # Create a list of areas and centroid coordinates
    area_list = []
    centroid_list = []
    for feature in polygon['features']:
        points_list = feature["geometry"]["coordinates"][0][0]
        area_list.append(find_area(points_list))
        centroid_list.append(find_decomposed_centroid(points_list))

    # Calculate the centroid of the entire polygon using the above created lists
    x = [p[0] for p in centroid_list]
    y = [p[1] for p in centroid_list]
    c_x = 0
    c_y = 0
    for i in range(len(x)):
        c_x += x[i] * area_list[i]
        c_y += y[i] * area_list[i]
    c_x /= sum(area_list)
    c_y /= sum(area_list)

    # Define the overall centroid as a list
    c_point = [c_x, c_y]
    return c_point


# Opens the source file
file_name = 'D:\Hunter 2019 Fall\GTECH 731\pluto.geojson'
with open(file_name, "r") as file:
    # Reads the data into a string variable
    data = file.read()

    # Loads the data into a dictionary variable
    dic = json.loads(data)

    # Plot the the "decomposed" smaller polygons which in reality are the building lots
    for feature in dic['features']:
        points_list = feature["geometry"]["coordinates"][0][0]
        x = [p[0] for p in points_list]
        y = [p[1] for p in points_list]
        plt.plot(x, y, zorder=0, alpha=0.5)

    # Find and plot the centroid of the entire selected polygon
    polygon_centroid = find_geometric_centroid(dic)
    plt.scatter(polygon_centroid[0], polygon_centroid[1], s=200, color='black', marker='*', zorder=10)

# Display to graph
plt.show()