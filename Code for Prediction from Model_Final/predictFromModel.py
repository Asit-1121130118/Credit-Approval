import pandas
import data_loader_prediction
from Prediction_Raw_Data_Validation import predictionDataValidation
import EDApipeline
import warnings
import logging
warnings.simplefilter("ignore")
PATH = "Prediction_Logs/Prediction.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



class Prediction:

    def __init__(self):
        self.datapath = "EDA_Output/input_prediction.csv"
        logger.info('Entered the constructor of Prediction_Model Class')

    def predictionFromModel(self):

        logger.info('Entered the predictionFrom_Model function')
        try:
            del_pred=predictionDataValidation.Prediction_Data_validation() #deletes the existing prediction file from last run!
            del_pred.deletePredictionFile()

            logger.info('Entered the Main Prediction function')
            data_getter=data_loader_prediction.Data_Getter()
            data=data_getter.get_data()
            logger.info('Successfully loaded the data from data_loader.py')
        except Exception as e:
            logger.warning("An Exception has occured in get_data function in Data_Getter class, Exception message: "+str(e))
            logger.warning("Data loading is unsuccessfull.Exitted the get_data function of the Data_Getter class")
            raise Exception()









