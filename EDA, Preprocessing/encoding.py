import pandas as pd
class Encoding:
    def encode(self,datawith_y):
        try:
            category_cols = [x for x in datawith_y.columns if
                             x.startswith('CODE_') or x.startswith('NAME_') or x.startswith('OCCUPATION_')]
            categories_df = datawith_y[category_cols]
            df_onehot = pd.get_dummies(categories_df, drop_first=True)
            datawith_y.drop(columns=category_cols, inplace=True)
            datawith_y = pd.concat([df_onehot, datawith_y], axis=1)
            datawith_y['FLAG_WORK_PHONE'] = datawith_y['FLAG_WORK_PHONE'].astype('uint8')
            datawith_y['FLAG_PHONE'] = datawith_y['FLAG_PHONE'].astype('uint8')
            datawith_y['FLAG_EMAIL'] = datawith_y['FLAG_EMAIL'].astype('uint8')
            datawith_y['customer_type'] = datawith_y['customer_type'].replace({'good': 0, 'bad': 1}).astype('uint8')
            datawith_y.drop(columns=['customer_id', 'cust_id'], inplace=True)

            return datawith_y

        except Exception as e:
            print(e)





