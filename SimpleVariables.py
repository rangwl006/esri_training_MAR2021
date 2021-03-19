try:
    import arcpy
    print("Arcpy successfully imported")

except ImportError:
    print("Could not import arcpy")

def setup_env():
    print("setup_env")
    arcpy.env.overwriteOutput = True

# add shape file to geodatabase
def copy_features(work_dir):
    # output = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\Default.gdb\AffectedAreaAppCurrent"
    output = work_dir + "AffectedAreaApp.shp"
    try:
        arcpy.management.CopyFeatures(out_class, output)
        print("Successfully copied features into database")
        
    except argisscripting.ExecuteError:
        print(argisscripting)

# calculate kernel density from points
def calc_kernel_density(work_dir):
    output = work_dir + "AffectedAreaApp.shp"
    try:
        outKD = arcpy.sa.KernelDensity(output, 'NONE')
        print("Successfully computed kernel density")

    except:
        print("operation failed: could not calculate kernel density")

def describe_object(work_dir):
    filepath = work_dir + "ParcelPts"
    desc = arcpy.Describe(filepath)
    dPath = desc.path
    print(f'dPath: {dPath}')

def create_new_feature_class(work_dir):
    print("started creating new feature class")
    filepath = work_dir + "ParcelPts"
    desc = arcpy.Describe(filepath)
    dPath = desc.path
    dName = desc.baseName
    dGeometry = desc.shapeType
    dCoord = desc.spatialReference

    newName = f'{dName}_New'
    print(f' new feature class name: {newName}')
    arcpy.CreateFeatureclass_management(dPath, newName, dGeometry, None,"", "", dCoord)
    print("end of create_new_feature_class")

def create_feature_class_ws(work_dir):
    print("create feature class in a loop")
    # set new workspace
    arcpy.env.workspace = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\CountyData.gdb"
    out_ws = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\Default.gdb"
    fcList = arcpy.ListFeatureClasses("", "Point")
    for fc in fcList:
        outputFc = f'{out_ws}\{fc}_copy'
        arcpy.CopyFeatures_management(fc, outputFc)
        print(f'copied feature class: {outputFc}')

if __name__=='__main__':
    setup_env()
    work_dir = "C:\\Users\\Student\\Desktop\\ArcPy\\PYTS_1.1_Jul18_StudentData\\EsriTraining\\PYTS\\Data\\"
    create_feature_class_ws(work_dir + "CountyData.gdb\\")
    print("eof")

