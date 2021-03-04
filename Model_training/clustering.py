import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
import logging
import pandas as pd
import pickle
import os
PATH = "Logs/clustering.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler(PATH)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class KMeansClustering:
    """
            This class shall  be used to divide the data into clusters before training.


            """

    def __init__(self):
        logger.info("Entered the constructor of clustering")
        pass

    def elbow_plot(self,data):
        """

                        Elbow plot to decide the optimum number of clusters to the file.


        """
     #   self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        logger.info('Entered the elbow_plot method of the KMeansClustering class')
        wcss=[] # initializing an empty list

        #Deleting the PNG file to create the latest one, no option to override
        strFile = "./Results/Clustering/K-Means_Elbow.PNG"
        os.remove(strFile)

        try:
            for i in range (1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++', random_state=42) # initializing the KMeans object
                kmeans.fit(data) # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)
            plt.plot(range(1,11),wcss) # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            #plt.show()


            plt.savefig('Results/Clustering/K-Means_Elbow.PNG') # saving the elbow plot locally
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')
            logger.info('The optimum number of clusters is: '+str(self.kn.knee)+' . Exited the elbow_plot method of the KMeansClustering class')
        #    self.logger_object.log(self.file_object, 'The optimum number of clusters is: '+str(self.kn.knee)+' . Exited the elbow_plot method of the KMeansClustering class')
            return self.kn.knee

        except Exception as e:
        #    self.logger_object.log(self.file_object,'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:  ' + str(e))
         #   self.logger_object.log(self.file_object,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self,data,number_of_clusters):
        """
                                Method Name: create_clusters
                                Description: Create a new dataframe consisting of the cluster information.
                                Output: A datframe with cluster column
                                On Failure: Raise Exception



                        """
        logger.info('Entered the create_clusters method of the KMeansClustering class')
     #   self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data=data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            #self.data = self.data[~self.data.isin([np.nan, np.inf, -np.inf]).any(1)]
            self.y_kmeans=self.kmeans.fit_predict(data) #  divide data into clusters

      #      self.file_op = file_methods.File_Operation(self.file_object,self.logger_object)
       #     pickle.dumps(self.kmeans,'ClusteringModel') # saving the KMeans model to directory
            pickle.dump(self.kmeans, open("clustering_model.sav", "wb"))                                                                        # passing 'Model' as the functions need three parameters

            self.data['Cluster']=self.y_kmeans  # create a new column in dataset for storing the cluster information
            logger.info('succesfully created '+str(self.kn.knee)+ 'clusters. Exited the create_clusters method of the KMeansClustering class')
      #      self.logger_object.log(self.file_object, 'succesfully created '+str(self.kn.knee)+ 'clusters. Exited the create_clusters method of the KMeansClustering class')
            return self.data
        except Exception as e:
     #       self.logger_object.log(self.file_object,'Exception occured in create_clusters method of the KMeansClustering class. Exception message:  ' + str(e))
     #       self.logger_object.log(self.file_object,'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception()

'''
if __name__ == "__main__":
    data = pd.read_csv("data.csv")
    data.drop('customer_type',axis=1,inplace=True)

    clustering_obj = KMeansClustering()

    no_of_cluster = clustering_obj.elbow_plot(data)
    final_data = clustering_obj.create_clusters(data,no_of_cluster)
    final_data.to_csv('Results/Clustering/Clustered_Data.csv')
'''
