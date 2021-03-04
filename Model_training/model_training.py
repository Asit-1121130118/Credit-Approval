
import pickle
from sklearn.model_selection import train_test_split
import data_loader
import tuner
import clustering
import warnings
import logging
#import imblearn
#from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import SMOTE

warnings.simplefilter("ignore")
PATH = "Logs/model_training.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Train_Model:

    def __init__(self):
        self.datapath="Data.csv"
        logger.info('Entered the constructor of Train_Model Class')

    def Training(self):

        logger.info('Entered the Main Training function')
        load = data_loader.DataGetter()

        data = load.get_data()
        logger.info('Successfully loaded the data from data_loader.py')

        clustering_obj = clustering.KMeansClustering()
        no_of_cluster = clustering_obj.elbow_plot(data)
        logger.info('Successfully created '+str(no_of_cluster)+'clusters')
        clustered_data = clustering_obj.create_clusters(data, no_of_cluster)
        logger.info('Successfully saved Clustering model')

        clusters = clustered_data['Cluster'].unique()

        for i in clusters:
            cluster_data = clustered_data[clustered_data['Cluster'] == i]  # filter the data for one cluster

            # Prepare the feature and Label columns
            cluster_features = cluster_data.drop(['customer_type', 'Cluster'], axis=1)
            cluster_label = cluster_data['customer_type']


            # resampling the imbalanced dataset
            oversample = SMOTE()
            #X, y = oversample.fit_resample(cluster_features, cluster_label)


            # splitting the data into training and test set for each cluster one by one
            x_train_init, x_test_init, y_train_init, y_test_init = train_test_split(cluster_features, cluster_label, test_size=.3, random_state=42)


            # creating oversampling synthetic data using borderlineSmote
            #oversample = BorderlineSMOTE(random_state=42, sampling_strategy=.15)
            #x_train, y_train = oversample.fit_sample(x_train_init, y_train_init)
            #x_test, y_test = oversample.fit_sample(x_test_init, y_test_init)

            model_finder = tuner.Model_Finder()  # object initialization

            # getting the best model for each of the clusters
            best_model_name, best_model = model_finder.get_best_model(x_train_init, y_train_init, x_test_init, y_test_init)

            # saving the best model to the directory.

            pickle.dump(best_model, open("Results/model/Modelforcluster"+str(i)+".sav", "wb"))


        logger.info('created best models')



if __name__ == "__main__":
    trainObj = Train_Model()
    data = trainObj.Training()
    print(data)


