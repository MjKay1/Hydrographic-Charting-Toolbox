# Import arcpy module
import arcpy

# Script arguments
Bathymetry = arcpy.GetParameterAsText(0)

Number_of_cells = arcpy.GetParameterAsText(1)
if Number_of_cells == '#' or not Number_of_cells:
    Number_of_cells = "50" # provide a default value if unspecified

DraftDepth = arcpy.GetParameterAsText(2)
if DraftDepth == '#' or not DraftDepth:
    DraftDepth = "12" # provide a default value if unspecified

rastercheck = arcpy.GetParameterAsText(3)

v12mDraft_tif = arcpy.GetParameterAsText(4)
if v12mDraft_tif == '#' or not v12mDraft_tif:
    v12mDraft_tif = "lane.tif" # provide a default value if unspecified
	
vectorcheck = arcpy.GetParameterAsText(5)

ExpandPolygon_shp2 = arcpy.GetParameterAsText(6)
if ExpandPolygon_shp2 == '#' or not ExpandPolygon_shp2:
    ExpandPolygon_shp2 = "lane.shp" # provide a default value if unspecified

CentreLine = arcpy.GetParameterAsText(7)
if CentreLine == '#' or not CentreLine:
    CentreLine = "centreLine.shp" # provide a default value if unspecified
	
trimcheck = arcpy.GetParameterAsText(8)

featurecheck = arcpy.GetParameterAsText(9)

Features = arcpy.GetParameterAsText(10)
if Features == '#' or not Features:
		Features = "%scratchWorkspace%\\Features" # provide a default value if unspecified

		
arcpy.env.overwriteOutput=True

# Local variables:
if rastercheck:
	Shrink__2_ = "%scratchWorkspace%\\Shrink"
	Expand__2_ = "%scratchWorkspace%\\Expand"
	ExpandPolygon_shp = "%scratchWorkspace%\\ExpandPolygon.shp"
ExpandPolygonVertices_shp = "%scratchWorkspace%\\ExpandPolygonVertices.shp"
Thiessen_shp = "%scratchWorkspace%\\Thiessen.shp"
Thiessen_Lines_shp = "%scratchWorkspace%\\Thiessen_Lines.shp"
Thiessen_Lines_Layer = "Thiessen_Lines_Layer"
Thiessen_Lines_Layer__2_ = Thiessen_Lines_Layer
ShrinkPolygon_shp = "%scratchWorkspace%\\ShrinkPolygon.shp"
Thiessen_Lines_Layer__3_ = Thiessen_Lines_Layer__2_
Thiessen_Lines_Dissolve1_shp = "%scratchWorkspace%\\Thiessen_Lines_Dissolve1.shp"
if vectorcheck:
	Shrink__2_2 = "%scratchWorkspace%\\Shrink"
	Expand__2_2 = "%scratchWorkspace%\\Expand"
	v12mDraft_tif2 = "%scratchWorkspace%\\v12mDraft.tif"

# Process: Reclassify
arcpy.AddMessage("Step 1/12 Started- Reclassifying Bathymetry")
if rastercheck:
	arcpy.gp.Reclassify_sa(Bathymetry, "VALUE", "-35.110001 -"+DraftDepth+" 1;-"+DraftDepth+" 0.570000 NoData", v12mDraft_tif, "DATA")
if vectorcheck:
	arcpy.gp.Reclassify_sa(Bathymetry, "VALUE", "-35.110001 -"+DraftDepth+" 1;-"+DraftDepth+" 0.570000 NoData", v12mDraft_tif2, "DATA")
arcpy.AddMessage("Step 1/12 Completed")

# Process: Shrink
arcpy.AddMessage("Step 2/12 Started- Shrinking Lanes")
if rastercheck:
	arcpy.gp.Shrink_sa(v12mDraft_tif, Shrink__2_, Number_of_cells, "1")
if vectorcheck:
	arcpy.gp.Shrink_sa(v12mDraft_tif2, Shrink__2_2, Number_of_cells, "1")
arcpy.AddMessage("Step 2/12 Completed")

# Process: Expand
arcpy.AddMessage("Step 3/12 Started- Expanding Lanes")
if rastercheck:
	arcpy.gp.Expand_sa(Shrink__2_, Expand__2_, Number_of_cells, "1")
if vectorcheck:
	arcpy.gp.Expand_sa(Shrink__2_2, Expand__2_2, Number_of_cells, "1")
arcpy.AddMessage("Step 3/12 Completed")

# Process: Raster to Polygon (2)
arcpy.AddMessage("Step 4/12 Started- Creating Polygon of Lanes")
if rastercheck:
	arcpy.RasterToPolygon_conversion(Expand__2_, ExpandPolygon_shp, "SIMPLIFY", "VALUE")
if vectorcheck:
	arcpy.RasterToPolygon_conversion(Expand__2_2, ExpandPolygon_shp2, "SIMPLIFY", "VALUE")
arcpy.AddMessage("Step 4/12 Completed")

# Process: Feature Vertices To Points
arcpy.AddMessage("Step 5/12 Started- Creating Points at Vertices")
if rastercheck:
	arcpy.FeatureVerticesToPoints_management(ExpandPolygon_shp, ExpandPolygonVertices_shp, "ALL")
if vectorcheck:
	arcpy.FeatureVerticesToPoints_management(ExpandPolygon_shp2, ExpandPolygonVertices_shp, "ALL")
arcpy.AddMessage("Step 5/12 Completed")

# Process: Create Thiessen Polygons
arcpy.AddMessage("Step 6/12 Started- Creating Thiessen Polygons")
arcpy.CreateThiessenPolygons_analysis(ExpandPolygonVertices_shp, Thiessen_shp, "ALL")
arcpy.AddMessage("Step 6/12 Completed")

# Process: Feature To Line
arcpy.AddMessage("Step 7/12 Started- Creating Lines from Thiessen Polygons")
arcpy.FeatureToLine_management("%scratchWorkspace%\\Thiessen.shp", Thiessen_Lines_shp, "", "ATTRIBUTES")
arcpy.AddMessage("Step 7/12 Completed")

# Process: Make Feature Layer
arcpy.AddMessage("Step 8/12 Started- Making Thiessen Lines into Feature Layer")
arcpy.MakeFeatureLayer_management(Thiessen_Lines_shp, Thiessen_Lines_Layer, "", "", "Shape Shape VISIBLE NONE;FID FID VISIBLE NONE;ID ID VISIBLE NONE;GRIDCODE GRIDCODE VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;Input_FID Input_FID VISIBLE NONE")
arcpy.AddMessage("Step 8/12 Completed")

# Process: Raster to Polygon
arcpy.AddMessage("Step 9/12 Started- Creating Polygon From Shrunk Raster")
arcpy.RasterToPolygon_conversion(Shrink__2_, ShrinkPolygon_shp, "SIMPLIFY", "VALUE")
arcpy.AddMessage("Step 9/12 Completed")

# Process: Select Layer By Location
arcpy.AddMessage("Step 10/12 Started- Selecting Lines within Shrunk Area")
arcpy.SelectLayerByLocation_management(Thiessen_Lines_Layer, "COMPLETELY_WITHIN", ShrinkPolygon_shp, "", "NEW_SELECTION", "INVERT")
arcpy.AddMessage("Step 10/12 Completed")

# Process: Delete Features
arcpy.AddMessage("Step 11/12 Started- Deleting External Lines")
arcpy.DeleteFeatures_management(Thiessen_Lines_Layer__2_)
arcpy.AddMessage("Step 11/12 Completed")

#check if trimming has been selected and run if so	
if trimcheck:
	
	# taken from The Polygon to Centerline Tool for ArcGIS (trim skeletons). (Dilts. 2015.) 
	# Process: Dissolve
	arcpy.AddMessage("Step 12/12 Started- Dissolving Lines")
	arcpy.Dissolve_management(Thiessen_Lines_Layer__3_, Thiessen_Lines_Dissolve1_shp, "GRIDCODE", "", "MULTI_PART", "DISSOLVE_LINES")
	arcpy.AddMessage("Step 12/12 Completed")

	# Process: Multipart To Singlepart
	arcpy.AddMessage("Line Trimming Started")
	arcpy.MultipartToSinglepart_management(Thiessen_Lines_Dissolve1_shp, CentreLine)

	# Process: Trim Line
	arcpy.TrimLine_edit(CentreLine, "", "DELETE_SHORT")
	arcpy.AddMessage("Line Trimming Completed")
	#end of section from Dilts. 2015

#if line trim not selected just dissolve the lines
else:
	# Process: Dissolve
	arcpy.AddMessage("Step 12/12 Started- Dissolving Lines")
	arcpy.Dissolve_management(Thiessen_Lines_Layer__3_, CentreLine, "GRIDCODE", "", "MULTI_PART", "DISSOLVE_LINES")
	arcpy.AddMessage("Step 12/12 Completed")
	
#check if features have been selected and run if so	
if featurecheck:

	# Local variables:
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
	
	
#clean up files
arcpy.Delete_management(Shrink__2_)
arcpy.Delete_management(Expand__2_)
arcpy.Delete_management(ExpandPolygon_shp)
arcpy.Delete_management(v12mDraft_tif2)
arcpy.Delete_management(ExpandPolygonVertices_shp)
arcpy.Delete_management(Thiessen_shp)
arcpy.Delete_management(Thiessen_Lines_shp)
arcpy.Delete_management(Thiessen_Lines_Layer)
arcpy.Delete_management(Thiessen_Lines_Layer__2_)
arcpy.Delete_management(Thiessen_Lines_Layer__3_)
arcpy.Delete_management(Thiessen_Lines_Dissolve1_shp)
arcpy.Delete_management(ShrinkPolygon_shp)
