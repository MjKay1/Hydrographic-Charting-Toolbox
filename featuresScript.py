# Import arcpy module
import arcpy

# Script arguments
Bathymetry = arcpy.GetParameterAsText(0)

Features = arcpy.GetParameterAsText(1)
if Features == '#' or not Features:
	Features = "%scratchWorkspace%\\Features" # provide a default value if unspecified

# Local Variables
Output_raster = "%scratchWorkspace%\\output_raster"
reslope = "%scratchWorkspace%\\reslope"
Expand_recla1 = "%scratchWorkspace%\\Expand_reslo1"


# Process: Slope
arcpy.AddMessage("Finding Features")
arcpy.AddMessage("Step 1/3 Started - Calculating Slopes")
arcpy.gp.Slope_sa(Bathymetry, Output_raster, "DEGREE", "1")
arcpy.AddMessage("Step 1/3 Completed")

# Process: Reclassify
arcpy.AddMessage("Step 2/3 Started - Finding Steep Features")
arcpy.gp.Reclassify_sa(Output_raster, "VALUE", "0 30.000000 NODATA;30 90 1", reslope, "DATA")
arcpy.AddMessage("Step 2/3 Completed")

# Process: Expand
arcpy.AddMessage("Step 3/3 Started - Displaying results")
arcpy.gp.Expand_sa(reslope, Expand_recla1, "200", "1")

# Process: Shrink
arcpy.gp.Shrink_sa(Expand_recla1, Features, "190", "1")
arcpy.AddMessage("Step 3/3 Completed")

arcpy.Delete_management(Output_raster)
arcpy.Delete_management(reslope)
arcpy.Delete_management(Expand_recla1)