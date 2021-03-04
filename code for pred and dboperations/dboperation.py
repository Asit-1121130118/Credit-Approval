import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
import pandas as pd



class dBOperation:
    """
     Sql lite ops.

      """
    def __init__(self):
        self.path = 'Prediction_Database/'
        self.badFilePath = "Prediction_Raw_files_validated/Bad_Raw"
        self.goodFilePath = "Prediction_Raw_files_validated/Good_Raw"


    def dataBaseConnection(self,DatabaseName):

        """
                creating a connection to the DB

                """
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')


        except ConnectionError:

            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):
        """
                        if table exists, alter it else, create one.

                        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()


            else:

                for key in column_names.keys():
                    type = column_names[key]



                    try:

                        conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key, dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))


                conn.close()




        except Exception as e:

            conn.close()

            raise e


    def insertIntoTableGoodData(self,Database):

        """
        all good folder files to be moved to DB.
        """
        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]



        for file in onlyfiles:
            try:
                add_data = pd.read_csv(goodFilePath + "/" + file)
                add_data.to_sql('Good_Raw_Data', conn, if_exists='append', index=False)
                conn.commit()

            except Exception as e:
                conn.rollback()

                shutil.move(goodFilePath+'/' + file, badFilePath)

                conn.close()
                raise e

        conn.close()



    def selectingDatafromtableintocsv(self,Database):

        """
                               move data from DB to CSV files
                               Delete the DB onve csv is created.
                               if we want to append future records then do not delete table, then changes to create table is required to avoid, table already exists.

        """

        self.fileFromDb = 'Prediction_FileFromDB/'
        self.fileName = 'InputFile.csv'

        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            sqlDelete = "DELETE FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlDelete)
            conn.commit()



        except Exception as e:
            raise e