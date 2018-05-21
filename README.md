# Hydrographic-Charting-Toolbox
### A collection of tools to process bathymetric raster data into areas safe for vessels of different draughts and create centre lines in these areas to create shipping lanes. Features of interest in the area can also be identified.

## How to add the toolbox
In ArcMap, simply add the 'Hydrographic Charting Toolbox' Toolbox to the ArcToolbox window.

## Using the Sample Data 
set the Workspace and Scratch Workspace in Environments
Add the Bathymetry and Bathymetry_Clip using the Add Data icon.
Navigate to the Create Shipping Lanes script in the ArcToolbox window and open it.
Add the Bathymetry (or Bathymetry_Clip, as the file is much smaller, and reduces the run time significantly) as the input bathymetry.
The recommended values for other required inputs can be found in the help section of the Parameters window.
Select if you want to have the 'safe channels' output as a vector or raster file (or both) and name the selected outputs.
Select if the line should be trimmed (this can be done seperately with the 'Trim Line Dangles' script, however it is recommended to select this in the main tool for ease of use).
Select if you want to find features (this will automatically run the 'Find Features' script once the Shipping Lanes are found. Again, this can be done Seperately with the dedicated tool, but can be done in the main tool for ease of use).
N.B. the files may not add to the window automatically upon completion of the script, in this case simply open them from the workspace defined, as with the Bathymetry.