# Implementing eda as class based structure in python file
import warnings 
import pandas as pd
import numpy as np
import logging
warnings.simplefilter("ignore")
PATH = "Prediction_Logs/EDA.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
class EDA:
    # This is a class which implements EDA process

    def read_file(file_address):
        # Reading Files:
        """
            Method Name: read_file
            Description: Reads the csv files 
            Output: Returns the csv files
            On Failure: Raise Exception
        """
        logger.info("Inside the read_file function of EDA class")
        try:
            file = pd.read_csv(file_address,index_col='ID')
            logger.info("Successfully read the csv files from the read_file function of EDA class")

            return file
        except Exception as e:

            print("Error occured inside read_file function of EDA class"+str(e))
            raise Exception()

    def get_distinct_values(application,credit):
        #Getting Distinct values to work with:
        """
            Method Name: get_distinct_values
            Description: Gets the distinct value of particular columns of the dataset 
            Output: Makes distinct columns
            On Failure: Raise Exception 
        """
        logger.info("Inside the get_distinct_values function of EDA class")

        try:
            uniqueID = (list(set(application.index).intersection(set(credit.index))))
            application = application.loc[uniqueID]
            credit = credit.loc[uniqueID]
            application_clean = application.sort_values(by=application.columns.to_list())
            application_clean['cust_id'] = application.sum(axis=1).map(hash)
            grouped_cust = application.sum(axis=1).map(hash).reset_index().rename(columns={0: 'customer_id'})
            grouped_cust = grouped_cust.set_index('ID')
            credit_trsf = credit.merge(grouped_cust, how='inner', on='ID').reset_index()[
                ['customer_id', 'ID', 'MONTHS_BALANCE', 'STATUS']]
            cred_df_g = credit_trsf.sort_values(by=['customer_id', 'ID', 'MONTHS_BALANCE'],
                                                ascending=[True, True, False]).reset_index(drop=True)
            cred_df_g['link_ID'] = cred_df_g.groupby(['customer_id', 'ID'], sort=False).ngroup().add(1)
            cred_df_g.drop(columns=['ID'], inplace=True)
            cred_df_g = cred_df_g[['customer_id', 'link_ID', 'MONTHS_BALANCE', 'STATUS']]
            return cred_df_g,application_clean
            logger.info("Successfully executed the get_distinct function of EDA class")


        except Exception as e:

            print("Error occured inside get_distinct_values function of EDA class "+str(e))
            raise Exception()


    def label_data(cred_df_g,application_clean):
        # Labelling customer data:
        """
             Method Name: label_data
            Description: Labels the data 
            Output: Makes the labels on particular dataset
            On Failure: Raise Exception
        """
        logger.info("Inside the label_data function of EDA class")

        try:
            series1 = cred_df_g.groupby('customer_id').size()
            temp_df1 = series1.to_frame(name='months_in_book')
            series2 = cred_df_g.groupby(['customer_id'])['link_ID'].nunique()
            temp_df2 = series2.to_frame('contracts_nr')
            credit_clean = pd.merge(temp_df1, temp_df2, on='customer_id')

            application_clean['OCCUPATION_TYPE'] = application_clean['OCCUPATION_TYPE'].fillna('Not Available')
            application_clean['FLAG_OWN_CAR'] = application_clean['FLAG_OWN_CAR'].replace({'Y': 1, 'N': 0})
            application_clean['FLAG_OWN_REALTY'] = application_clean['FLAG_OWN_REALTY'].replace({'Y': 1, 'N': 0})

            credit_clean.reset_index(inplace=True)
            X=application_clean.reset_index().merge(credit_clean, left_on=application_clean.cust_id,right_on=credit_clean.customer_id, how='inner')
            X.drop(columns=['key_0', 'cust_id', 'customer_id']).set_index('ID')
            X.drop(columns=['FLAG_MOBIL'], inplace=True)
            X.drop(columns=['CNT_CHILDREN','contracts_nr','key_0'], inplace=True)

            logger.info("successfully merged the files and exited the  merging function")

            return X


        except Exception as e:
            print("Error occured inside the label_data function of EDA class"+str(e))
            raise Exception()




# This is for testing purposes
"""if __name__ == "__main__":
    try:
        e = EDA()
        df1,df2 = e.read_file()
        print(df1.head())
        print(df2.head())
        e.get_distinct_values()
        e.label_data()
        df3 = e.fill_values()
        print(df3)
    except Exception as e:
        print("Sorry error occured: "+str(e))
"""