class LicenseError(Exception):
    pass

class SpatialRefProjError (Exception):
    pass


import arcpy
from arcpy import env
from arcpy.sa import *
import os
import arcpy.mp as mapping

try:
	#Check for spatial analyst license
    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
    else:
        raise LicenseError
    #Modeling polygon --- roadless
    demRaster = arcpy.GetParameterAsText(0)
    dscRaster = arcpy.Describe(demRaster)
 
    if dscRaster.spatialReference.type != "Projected":
        raise SpatialRefProjError


    # Set overwrite option
    env.overwriteOutput = True
    #Set extent based on users input
    ext = arcpy.GetParameterAsText(2) 
    if ext == "DEFAULT" or ext == "MAXOF" or ext == "MINOF":
        env.extent = dscRaster.extent      
    else:
        env.extent = ext
	
    analysisWindow = arcpy.GetParameterAsText(1)
    
    
     #Set message about running
    arcpy.AddMessage("Running Roughness ......")
    tmp1 = FocalStatistics(demRaster,analysisWindow,"STD")
    
    outRaster = SquareRoot(tmp1)
        
    

    outRasterName = arcpy.GetParameterAsText(3)
    outRaster.save (outRasterName)

    #Set message about running
    arcpy.AddMessage("Roughness Complete")
    #arcpy.AddMessage("Initial extent:  " + str(ext))
    #arcpy.AddMessage("Geographic extent: "+ str(newExt))                             

    


except SpatialRefProjError:
    arcpy.AddError ("Spatial Data must use a projected coordinate system to run")

except LicenseError:
    arcpy.AddError ("Spatial Analyst license is unavailable") 	

finally:
    arcpy.CheckInExtension("Spatial")
   # arcpy.Delete_management("forGettingLoc")
