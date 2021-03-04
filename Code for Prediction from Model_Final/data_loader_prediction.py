import pandas as pd
import warnings
import logging
warnings.simplefilter("ignore")
PATH = "Prediction_Logs/data_loader.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Data_Getter:

    def __init__(self):

        data_file_path = 'EDA_Output/input_prediction.csv'
        self.data_file = data_file_path
        logger.info("Inside the DataGetter class constructor")

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the application data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

        """
        logger.info('Entered the get_data method of the Data_Getter class')
        try:
            self.data= pd.read_csv(self.data_file) # reading the data file
            logger.info('Data Load Successful.Exited the get_data method of the Data_Getter class')
            return self.data

        except Exception as e:
            logger.warning('Exception occured in get_data method of the Data_Getter class. Exception message: '+str(e))
            logger.warning('Application data Load Unsuccessful.Exited the get_data method of the Data_Getter class')
            raise Exception()


# This is for testing purposes

'''
if __name__ == "__main__":
    try:
        d = Data_Getter()
        print(d.get_data1())
    except Exception as e:
        print("Sorry there was an error in your code: "+str(e))
'''

