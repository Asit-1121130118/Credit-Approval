from rawvalidation import Raw_Data_validation
import dboperation
class predictionvalidationapplication:
    def __init__(self):
        pass
    def datavalidationapplication(self):
        validraw = Raw_Data_validation('Prediction_Batch_Files')
        dBOperation = dboperation.dBOperation()
        LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns = validraw.valuesfromschema()
        regx = validraw.manualregx()
        validraw.delexistingbaddatafolder()
        validraw.delexistinggooddatafolder()
        validraw.creategoodbadrawdata()
        validraw.validationfilenameraw(regx, LengthOfDateStampInFile, LengthOfTimeStampInFile)
        validraw.validatecolumnlength(NumberOfColumns)
        validraw.validatemissingvaluesinwholecolumn()
        validraw.replacemissingvalueswithnull()
        dBOperation.createTableDb('Prediction', column_names)
        dBOperation.insertIntoTableGoodData('Prediction')
        validraw.delexistinggooddatafolder()
        validraw.movebadfilestoarchivebad()
        dBOperation.selectingDatafromtableintocsv('Prediction')



