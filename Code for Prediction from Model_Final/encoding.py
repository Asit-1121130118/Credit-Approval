import pandas as pd
class Encoding:
    def encode(self,X):
        try:
            category_cols = [x for x in X.columns if
                             x.startswith('CODE_') or x.startswith('NAME_') or x.startswith('OCCUPATION_')]
            categories_df = X[category_cols]
            df_onehot = pd.get_dummies(categories_df, drop_first=True)
            X.drop(columns=category_cols, inplace=True)
            X = pd.concat([df_onehot, X], axis=1)
            X['FLAG_WORK_PHONE'] = X['FLAG_WORK_PHONE'].astype('uint8')
            X['FLAG_PHONE'] = X['FLAG_PHONE'].astype('uint8')
            X['FLAG_EMAIL'] = X['FLAG_EMAIL'].astype('uint8')
            X.drop(columns=['customer_id', 'cust_id'], inplace=True)

            return X

        except Exception as e:
            print(e)





