############################################################################################
#
# Calculating the volumes of all buildings in NYC
#
# Input: Spatial data file of all buildings in Manhattan
#        Elevation point data, including rooftops
# Output: Volume of every building, calculated by polygon area * rooftop elevation
#
# Process:
#   Create workspace environment
#   Map only the fields we wish to keep in the output feature layer
#   Join the elevation to all the building polygons that contain the point feature
#   Add a volume field to the new output feature
#   Calculate the volume using the rooftop elevation and polygon area
#   Remove all extra fields leaving only volume and those that were in the original file
#
############################################################################################

# ArcPy package lets us perform geoprocessing analyses
import arcpy

# Create workspace environment and declare variables for feature layers
arcpy.env.workspace = "INSERT PATH TO DATABASE"

buildings = "INSERT PATH TO BUILDINGS FILE"
elevation =  "INSERT PATH TO ELEVATION FILE"
out_feature = "output.shp"

# Delete output file if it already exists in the workspace
if arcpy.Exists(out_feature):
    arcpy.Delete_management(out_feature)

# Map fields from input files to keep in the output file
fieldmappings = arcpy.FieldMappings()
fieldmappings.addTable(buildings)
fieldmappings.addTable(elevation)
keep1 = ["BIN_NO", "ELEVATION"]
for field in fieldmappings.fields:
    if field.name not in keep1:
        fieldmappings.removeFieldMap(fieldmappings.findFieldMapIndex(field.name))

# Spatially join all building polygons and the elevation points they contain
# Add elevation value to newly created feature class
arcpy.SpatialJoin_analysis(buildings, elevation, out_feature, "JOIN_ONE_TO_ONE",
                           "KEEP_COMMON", fieldmappings, "CONTAINS")

# Add a volume field to the new output feature class
arcpy.AddField_management(out_feature, "VOLUME", "FLOAT")

# Calculate the volume field
arcpy.CalculateField_management(out_feature, "VOLUME", "!shape.area! * !ELEVATION!", "PYTHON_9.3")

# Remove all extra fields leaving only volume and those that were in the original shapefile
keep2 = [f.name for f in arcpy.ListFields(buildings)]
keep2.append("VOLUME")
for field in arcpy.ListFields(out_feature):
    if field.name not in keep2:
        arcpy.DeleteField_management(out_feature, field.name)

# OPTIONAL (Extremely Slow)
# Adds the VOLUME field directly into manh_bldgs.shp
# arcpy.JoinField_management(buildings, "FID", out_feature, "FID", "VOLUME")
