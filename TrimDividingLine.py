import arcpy

# Script arguments
inputLine = arcpy.GetParameterAsText(0)

CentreLine = arcpy.GetParameterAsText(1)
if CentreLine == '#' or not CentreLine:
    CentreLine = "TrimmedLine.shp" # provide a default value if unspecified

# Local Variables
Thiessen_Lines_Dissolve1_shp = "%scratchWorkspace%\\Thiessen_Lines_Dissolve1.shp"

# taken from The Polygon to Centerline Tool for ArcGIS (trim skeletons). (Dilts. 2015.) 
# Process: Dissolve
arcpy.AddMessage("Step 1/3 Started- Dissolving Lines")
arcpy.Dissolve_management(inputLine, Thiessen_Lines_Dissolve1_shp, "GRIDCODE", "", "MULTI_PART", "DISSOLVE_LINES")
arcpy.AddMessage("Step 1/3 Completed")

# Process: Multipart To Singlepart
arcpy.AddMessage("Step 2/3 Started - Breaking Line")
arcpy.MultipartToSinglepart_management(Thiessen_Lines_Dissolve1_shp, CentreLine)
arcpy.AddMessage("Step 2/3 Completed")

# Process: Trim Line
arcpy.AddMessage("Step 3/3 Started - Triming Dangles")
arcpy.TrimLine_edit(CentreLine, "", "DELETE_SHORT")
arcpy.AddMessage("Step 3/3 Completed")

#clean up files
arcpy.Delete_management(Thiessen_Lines_Dissolve1_shp)