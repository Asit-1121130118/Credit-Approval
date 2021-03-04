import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
import warnings
import logging
warnings.simplefilter("ignore")
PATH = "Logs/Model_Tuning.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Model_Finder:


    def __init__(self):
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        logger.info('Entered the constructor of the class Model_finder')

    def get_best_params_for_random_forest(self,train_x,train_y):


        try:

            self.param_grid = {"n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                                "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2']}
            #self.param_grid = {"n_estimators": [10], "criterion": ['gini'],
                               #"max_depth": [4], "max_features": ["log2"]}


            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=5,  verbose=3)

            self.grid.fit(train_x, train_y)
            logger.info('Finding the best parameters for Random forest')


            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)

            self.clf.fit(train_x, train_y)
            logger.info('Successfully fitted a random forest classifier')


            return self.clf
        except Exception as e:
            print(e)
            raise Exception()

    def get_best_params_for_xgboost(self,train_x,train_y):



        try:
            self.param_grid_xgboost = {

                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
                #'learning_rate': [0.001],
                #'max_depth': [5],
                #'n_estimators': [100]

            }

            self.grid= GridSearchCV(XGBClassifier(objective='binary:logistic'),self.param_grid_xgboost, verbose=3,cv=5)

            self.grid.fit(train_x, train_y)
            logger.info('Finding the best parameters for Xgboost')


            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            self.xgb.fit(train_x, train_y)
            logger.info('Successfully fitted a random xgboost classifier')


            return self.xgb
        except Exception as e:
            print(e)
            raise Exception()


    def get_best_model(self,train_x,train_y,test_x,test_y):

        try:
            self.xgboost= self.get_best_params_for_xgboost(train_x,train_y)
            self.prediction_xgboost = self.xgboost.predict(test_x)

            logger.info('Finding the best model')

            if len(test_y.unique()) == 1:
                self.xgboost_score = accuracy_score(test_y, self.prediction_xgboost)

            else:
                self.xgboost_score = roc_auc_score(test_y, self.prediction_xgboost)

            self.random_forest=self.get_best_params_for_random_forest(train_x,train_y)
            self.prediction_random_forest=self.random_forest.predict(test_x)

            if len(test_y.unique()) == 1:
                self.random_forest_score = accuracy_score(test_y,self.prediction_random_forest)

            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest)

            if(self.random_forest_score <  self.xgboost_score):
                logger.info('Xgboost is the suitable model')
                logger.info('Params choose are (learning_rate=1, max_depth=5, n_estimators=50) ')
                return 'XGBoost',self.xgboost
            else:
                logger.info('Random Forest is the suitable model')
                return 'RandomForest',self.random_forest

        except Exception as e:
            print(e)

'''
if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    x = df.drop(columns=['customer_type'])
    y = df['customer_type']
    smk = SMOTETomek(random_state=42)
    X_res, y_res = smk.fit_sample(x,y)
    model = Model_Finder()

    x_train, x_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.3, random_state=42)
    print(model.get_best_model(x_train, y_train, x_test, y_test))
'''
