import arcpy
import csv
import json

work_dir = "C:\\Users\\Student\\Desktop\\ArcPy\\PYTS_1.1_Jul18_StudentData\\EsriTraining\\PYTS\\Data\\Default.gdb\\"

class EmptyRows(Exception):
    pass
    
def exercise_8():
    pass

def exercise_7():
    #variables
    outageXY = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\OutageXY2.csv"
    print("Variables are set.")
    

    #Append coordinates from csv in a list and print the first row
    outageCoords = []
    csvFile = open(outageXY, 'r')
    csvReader = csv.reader(csvFile)
    next(csvReader)
    
    try:
        row_count = 0
        for row in csvReader:
            outageCoords.append(row)
            row_count += 1
        if row_count == 0:
            raise EmptyRows(csvCount)
        print(outageCoords[0])

    except Exception as e:
        print(e)

def exercise_6():
    arcpy.env.overwriteOutput = True
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(103501)
    print("Modules imported and environments set.")

    #variables
    outageXY = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\OutageXY.csv"
    outConvexHull = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\Outages.gdb\CurrentAffectedArea"
    outputJoin = r"in_memory\outputJoin"
    serviceAreas = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\CountyData.gdb\ServiceAreas"
    print("Variables are set.")

    #Append coordinates from csv in a list
    outageCoords = []
    csvFile = open(outageXY, 'r')
    csvReader = csv.reader(csvFile)
    next(csvReader)
    for row in csvReader:
        outageCoords.append(row)

    #Create a multipoint geometry object from list of coordinates
    outagePoints = (arcpy.Multipoint(arcpy.Array([arcpy.Point(*coords) for coords in outageCoords])))
    print("Geometry object created")

    #Create outage boundary using convex hull
    convexHull = outagePoints.convexHull()
    arcpy.CopyFeatures_management(convexHull, outConvexHull)
    print("Outage boundary created")

    #Use Spatial Join to identify affected areas
    arcpy.SpatialJoin_analysis(serviceAreas,outagePoints,outputJoin)
    print("Spatial join finished.")

    #Search join output
    sFields = ['Join_Count', 'ServArNu']
    exp = '"Join_Count" = 1'
    print("Affected service areas")
    with arcpy.da.SearchCursor(outputJoin,sFields,exp) as sCursor:
        for row in sCursor:
            print("Service Area: {}".format(row[1]))

    print("Analysis complete.")


# creates new feature class in the working directory
# returns the path of the new feature class
def create_new_feature_class(fc, fc_copy):
    global work_dir
    print("started creating new feature class")
    filepath = work_dir + fc
    desc = arcpy.Describe(filepath)
    dPath = desc.path
    dName = desc.baseName
    dGeometry = desc.shapeType
    dCoord = desc.spatialReference

    newName = f'{dName}_{fc_copy}'
    arcpy.CreateFeatureclass_management(dPath, newName, dGeometry, None,"", "", dCoord)
    print(f'created new feature class name: {newName}')

    return work_dir + fc_copy

# write to csv
# write_csv(type: list, type: string)
def write_csv(text, filename):
    csvFile = open(f"{filename}.csv", "w")
    csvFile.write(text)
    csvFile.close()
    print(f"written to {filename}")

def set_env():
    print("Setting up env")
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = r"C:\Users\Student\Desktop\ArcPy\PYTS_1.1_Jul18_StudentData\EsriTraining\PYTS\Data\Default.gdb"

def update_cursor(feature_class):
    global work_dir
    # get the path to the desired feature class
    fc_path = work_dir + feature_class
    # create list of fields
    uFields =  ["SquFoot", "TaxValue", "PriceSquFt"]

    # create Update Cursor
    with arcpy.da.UpdateCursor(fc_path,uFields) as uCursor:
        for row in uCursor:
            row[2] = row[1]/row[0] # price per sqft = taxvalue / sqfoot
            uCursor.updateRow(row)
            print(f"sqft: {row[0]}, TaxValue: {row[1]}, PriceSquFt: {row[2]}")
            
def search_cursor(feature_class, query):
    global work_dir
    print("start search_cursor(feature_class)")
    fc_path = work_dir + feature_class
    # create new fields
    sFields = ["Parcel_ID", "Owner_Name", "Phone_Number", "PriceSquFt"]
    parcel_list = ["Parcel_Id,Owner_Name,Phone_Number,_PriceSquFt"]

    with arcpy.da.SearchCursor(fc_path, sFields, query) as sCursor:
        for row in sCursor:
            row_text = f'{row[0]},{row[1]},{row[2]},{row[3]}'
            parcel_list.append(row_text)
        
    text_body = '\n'.join(parcel_list)
    csv_name = "AssessmentParcels"
    write_csv(text_body, csv_name)

# create a function that:
# 1. if sqft < 1800, set tax to 0
def assignment_1(feature_class, query):
    global work_dir
    # define feature class to look into
    fc_path = work_dir + feature_class
    # define field in question0
    fields = ["SquFoot", "TaxValue"]
    updated_fields = ["SquFoot,TaxValue,NewTax"]
    with arcpy.da.UpdateCursor(fc_path, fields, query) as uCursor:
        for row in uCursor:
            # check if sqft < 1800
            sqft = row[0]
            tax = row[1]
            if sqft < 1800:
                row[1] = 0
                uCursor.updateRow(row)
            updated_fields.append(f'{sqft},{tax}, {row[1]}')
    text_body = '\n'.join(updated_fields)
    csv_name = "assigment_01"
    write_csv(text_body, csv_name)        
                
# delete rows with 1000 < sqft < 2000
def assignment_2(feature_class, query):
    global work_dir
    # define feature class to look into
    fc_path = work_dir + feature_class
    # define field in question
    fields = ["Street_Name", "Parcel_ID", "Owner_Name","SquFoot"]
    output_fields = ["Street_Name,Parcel_ID,Owner_Name,SquFoot"]
    
    with arcpy.da.UpdateCursor(fc_path, fields, query) as uCursor:
        for row in uCursor:
            street = row[0]
            parcel_id = row[1]
            owner = row[2]
            sqft = row[3]
            output_fields.append(f'{street},{parcel_id},{owner}, {sqft}')
            uCursor.deleteRow()
    
    text_body = '\n'.join(output_fields)
    csv_name = "assigment_02"
    write_csv(text_body, csv_name)        

def main():
    print("start of file")
    # insert functions here
    set_env()
    # update_cursor("ParcelPts")
    # assignment_2("ParcelPts", "Street_Name = 'Washington Street'")
    exercise_7()
    print("end of file")

if __name__=='__main__':
    main()