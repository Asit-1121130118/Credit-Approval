from datetime import datetime
from os import listdir
import os
import re
import json
import shutil
import pandas as pd



class Raw_Data_validation:



    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path = 'schema_training.json'



    def valuesfromschema(self):
        """
                get schema validations from json file

        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberofColumns = dic['NumberOfColumns']




        except ValueError:

            raise ValueError

        except KeyError:

            raise KeyError

        except Exception as e:

            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns


    def manualregx(self):

        regex = "['application']+['\_'']+[\d_]+[\d]+\.csv"

        return regex

    def creategoodbadrawdata(self):

        """
          temporary files to store good and bad files after stages of validation
                                              """

        try:
            path = os.path.join("Training_Raw_files_validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Training_Raw_files_validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

        except OSError as ex:

            raise OSError

    def delexistinggooddatafolder(self):
        """

            remove folder once job done and data is moved to DB

        """
        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')

        except OSError as s:

            raise OSError

    def delexistingbaddatafolder(self):

        """
        Also remove bad folder, which is after moving the files to the archive

                                                    """

        try:
            path = 'Training_Raw_files_validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')

        except OSError as s:

            raise OSError

    def movebadfilestoarchivebad(self):

        """
                                       bad folder to archive folder
                                                    """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        try:

            source = 'Training_Raw_files_validated/Bad_Raw/'
            if os.path.isdir(source):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'TrainingArchiveBadData/BadData_' + str(date)+"_"+str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)


                path = 'Training_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')


        except Exception as e:

            raise e




    def validationfilenameraw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
                    regex file name validation split by split.

                """

        #pattern = "['application']+['\_'']+[\d_]+[\d]+\.csv"
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.delexistingbaddatafolder()
        self.delexistinggooddatafolder()
        #create new directories
        self.creategoodbadrawdata()
        onlyfiles = [f for f in listdir(self.Batch_Directory)]
        try:

            for filename in onlyfiles:

                if (re.match(regex, filename)):
                    splitAtDot = re.split('.csv', filename)

                    splitAtDot = (re.split('_', splitAtDot[0]))
                    if (splitAtDot[0]) == 'application':
                        if len(splitAtDot[1]) == LengthOfDateStampInFile:
                            if len(splitAtDot[2]) == LengthOfTimeStampInFile:
                                shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Good_Raw")



                            else:
                                shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")


                        else:
                            shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")


                    else:
                        shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")

                else:
                    shutil.copy("Training_Batch_Files/" + filename, "Training_Raw_files_validated/Bad_Raw")





        except Exception as e:

            raise e




    def validatecolumnlength(self,NumberofColumns):
        """
                        if number of columns are not correct, move to bad folder

                      """
        try:


            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if csv.shape[1] == NumberofColumns:

                    pass
                else:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw")

        except OSError:

            raise OSError
        except Exception as e:

            raise e


    def validatemissingvaluesinwholecolumn(self):
        """
                                if whole column is empty, then moved to bad folder

                              """
        try:



            for file in listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)

                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move("Training_Raw_files_validated/Good_Raw/" + file,
                                    "Training_Raw_files_validated/Bad_Raw")

                        break
                if count==0:
                    #csv.rename(columns={"Unnamed: 0": "application"}, inplace=True) # if an important column has no header
                    csv.to_csv("Training_Raw_files_validated/Good_Raw/" + file, index=None, header=True)

        except OSError:

            raise OSError
        except Exception as e:

            raise e

    def replacemissingvalueswithnull(self):

        """
        in the validated file, replace all empty cells in csv with NULL value.
        """
        try:

            onlyfiles = [f for f in listdir('Training_FileFromDB')]
            for file in onlyfiles:
                csv = pd.read_csv(
                    'Training_FileFromDB' + "/" + file)
                csv.fillna('NULL', inplace=True)
                csv.to_csv('Training_FileFromDB' +
                            "/" + file, index=None, header=True)



        except Exception as e:
            raise e