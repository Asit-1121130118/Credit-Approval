import sqlite3
from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd
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



class Prediction_Data_validation:

    """
               This class shall be used for handling all the validation done on the Raw Prediction Data!!.

               """
    def __init__(self):

        logger.info('Entered the constructor of the class Prediction_Data_validation')


    def deletePredictionFile(self):
        """
                                            Method Name: deletePrevious Prediction files
                                            Description: This method deletes the previous prediction files.
                                            Output: None
                                            On Failure: OSError

                                                    """
        logger.info('Start of deleting prediction files')
        try:
            if os.path.exists('Prediction_Output_File/Predictions.csv'):
                os.remove('Prediction_Output_File/Predictions.csv')
                logger.info("Previous prediction files deleted succesfully!!!")

        except OSError as s:
            logger.warning("Error while Deleting Previous Prediction files : %s" %s)
            raise OSError




