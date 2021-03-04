from rawvalidation import Raw_Data_validation
import dboperation
class trainvalidationapplication:
    def __init__(self):
        pass
    def datavalidationapplication(self):
        validraw = Raw_Data_validation('Training_Batch_Files')
        dBOperation = dboperation.dBOperation()
        LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns = validraw.valuesfromschema()
        regx = validraw.manualregx()
        #validraw.delexistingbaddatafolder()
        #validraw.delexistinggooddatafolder()
        #validraw.creategoodbadrawdata()
        validraw.validationfilenameraw(regx, LengthOfDateStampInFile, LengthOfTimeStampInFile)
        validraw.validatecolumnlength(NumberOfColumns)
        validraw.validatemissingvaluesinwholecolumn()

        dBOperation.createTableDb('Training', column_names)
        dBOperation.insertIntoTableGoodData('Training')
        validraw.delexistinggooddatafolder()
        validraw.movebadfilestoarchivebad()
        dBOperation.selectingDatafromtableintocsv('Training')
        validraw.replacemissingvalueswithnull()



