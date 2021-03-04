import numpy as np
import pandas as pd

import os
import sys

# Reading Files:
application=pd.read_csv('application_record.csv',index_col='ID')
credit=pd.read_csv('credit_record.csv',index_col='ID')

# Getting Distinct values to work with:
uniqueID=(list(set(application.index).intersection(set(credit.index))))
application=application.loc[uniqueID]
credit=credit.loc[uniqueID]
application_clean = application.sort_values(by = application.columns.to_list())
application_clean['cust_id'] = application.sum(axis=1).map(hash)
grouped_cust = application.sum(axis=1).map(hash).reset_index().rename(columns={0:'customer_id'})
grouped_cust = grouped_cust.set_index('ID')
credit_trsf = credit.merge(grouped_cust, how = 'inner', on = 'ID').reset_index()[['customer_id','ID', 'MONTHS_BALANCE', 'STATUS']]
cred_df_g = credit_trsf.sort_values(by=['customer_id', 'ID', 'MONTHS_BALANCE'], ascending = [True, True, False]).reset_index(drop=True)
cred_df_g['link_ID'] = cred_df_g.groupby(['customer_id','ID'], sort = False).ngroup().add(1)
cred_df_g.drop(columns = ['ID'], inplace=True)
cred_df_g = cred_df_g[['customer_id', 'link_ID', 'MONTHS_BALANCE', 'STATUS']]


# Labelling customer data:
cred_df_g['monthly_behaviour'] = np.where( cred_df_g.STATUS.isin(['2','3','4','5']), 'b', 'g' )
cred_df_g.groupby(['customer_id', 'monthly_behaviour']).size()
cust_behaviour = pd.DataFrame( round( cred_df_g.groupby(['customer_id', 'monthly_behaviour']).size() / cred_df_g.groupby(['customer_id']).size() * 100, 2), columns = ['behaviour_score']).reset_index().set_index('customer_id')
bad_cust = \
cust_behaviour[ ( (cust_behaviour.monthly_behaviour=='g') & (cust_behaviour.behaviour_score <= 50) ) | \
    ( (cust_behaviour.monthly_behaviour=='b') & (cust_behaviour.groupby('customer_id').size()==1) )        ]
bad_cust['customer_type'] = 'bad'
bad_cust.drop(columns=['monthly_behaviour', 'behaviour_score'], inplace=True)
good_cust = \
    cust_behaviour[( (cust_behaviour.monthly_behaviour=='g') & (cust_behaviour.behaviour_score > 50) ) |
        ( (cust_behaviour.monthly_behaviour=='g') & (cust_behaviour.groupby('customer_id').size()==1) )]
good_cust['customer_type'] = 'good'
good_cust.drop(columns=['monthly_behaviour', 'behaviour_score'], inplace=True)
credit_clean = pd.concat([bad_cust, good_cust])
credit_clean['months_in_book'] = cred_df_g.groupby('customer_id').size()
credit_clean['contracts_nr'] = cred_df_g.groupby(['customer_id'])['link_ID'].nunique()

#Fill val (temp)
application_clean['OCCUPATION_TYPE']=application_clean['OCCUPATION_TYPE'].fillna('Not Available')
application_clean['FLAG_OWN_CAR']=application_clean['FLAG_OWN_CAR'].replace({'Y':1,'N':0})
application_clean['FLAG_OWN_REALTY']=application_clean['FLAG_OWN_REALTY'].replace({'Y':1,'N':0})

#Merging:
credit_clean.reset_index(inplace=True)
datawith_y=application_clean.reset_index().merge(credit_clean, left_on=application_clean.cust_id, right_on=credit_clean.customer_id, how='inner')
datawith_y.drop(columns=['key_0','cust_id','customer_id']).set_index('ID')
datawith_y.drop(columns=['FLAG_MOBIL'],inplace=True)
data = datawith_y
data.set_index('ID')
datawith_y.drop(columns=['CNT_CHILDREN','contracts_nr','key_0'],inplace=True)

#clubbing:


Occupation = {
    'Managers' : 'Occup1',
    'Realty agents' : 'Occup1',
    'Drivers' : 'Occup2',
    'Accountants' : 'Occup2',
    'IT staff' : 'Occup2',
    'Private service staff' : 'Occup2',
    'High skill tech staff' : 'Occup2',
    'HR staff' : 'Occup3',
    'Core staff' : 'Occup3',
    'Laborers' : 'Occup4',
    'Security staff' : 'Occup4',
    'Sales staff' : 'Occup4',
    'Not Available' : 'Occup5',
    'Secretaries' : 'Occup5',
    'Medicine staff' : 'Occup5',
    'Waiters/barmen staff' : 'Occup5',
    'Cleaning staff' : 'Occup6',
    'Cooking staff' : 'Occup6',
    'Low-skill Laborers' : 'Occup6'
}
datawith_y['OCCUPATION_TYPE'] = datawith_y['OCCUPATION_TYPE'].replace(Occupation)

#Ecoding:

category_cols  = [x for x in datawith_y.columns if x.startswith('CODE_') or x.startswith('NAME_') or x.startswith('OCCUPATION_') ]
categories_df=datawith_y[category_cols]
df_onehot = pd.get_dummies(categories_df, drop_first=True)
datawith_y.drop(columns = category_cols, inplace= True)
datawith_y = pd.concat([df_onehot, datawith_y], axis = 1)
datawith_y['FLAG_WORK_PHONE']=datawith_y['FLAG_WORK_PHONE'].astype('uint8')
datawith_y['FLAG_PHONE']=datawith_y['FLAG_PHONE'].astype('uint8')
datawith_y['FLAG_EMAIL']=datawith_y['FLAG_EMAIL'].astype('uint8')
datawith_y['customer_type']=datawith_y['customer_type'].replace({'good':0,'bad':1}).astype('uint8')
datawith_y.drop(columns=['customer_id','cust_id'],inplace=True)

# Saving files
datawith_y.to_csv('Data.csv')
'''X = datawith_y.drop(columns=['customer_type'])
Y = datawith_y['customer_type']

X.to_csv('X.csv')
Y.to_csv('Y.csv')'''
