from configs.config import ARTIFACTS
import os, logging
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from typing import List
import joblib
from utils.common import create_directories


class KMeansClustering:
    """
    This class shall  be used to divide the data into clusters before training.

    Written By: siddhartha shandilya
    Version: 1.0
    Revisions: None
    """

    def __init__(self) -> None:
        self.graph_dir_path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"],
            ARTIFACTS["GRAPHS_DIR"]["GRAPH_DIR_NAME"],
        )
        self.elbow_graph_dir_path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"],
            ARTIFACTS["GRAPHS_DIR"]["GRAPH_DIR_NAME"],
        )
        self.elbow_graph_file_name = os.path.join(
            ARTIFACTS["GRAPHS_DIR"]["ELBOW_GRAPH"]
        )
        self.cluster_data_dir_path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"],
            ARTIFACTS["CLUSTER_DIR"]["CLUSTER_DIR_NAME"],
        )
        self.cluster_model_dir_path = os.path.join(
            ARTIFACTS["ARTIFACTS_DIR"],
            ARTIFACTS["MODEL_DIR"]["MODEL_DIR_NAME"],
            ARTIFACTS["MODEL_DIR"]["DATA_CLUSTERING_MODEL_DIR_NAME"],
        )
        self.cluster_model_file_name = ARTIFACTS["MODEL_DIR"][
            "DATA_CLUSTERING_MODEL_NAME"
        ]

    def elbow_graph(self, data: pd.DataFrame) -> int:
        """

        Method Name: elbow_plot
        Description: This method saves the plot to decide the optimum number of clusters to the file.
        Output: A picture saved to the directory
        On Failure: Raise Exception

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None

        """
        logging.info("elbow_graph function is called ")
        wcss: List = []
        try:
            for i in range(1, 11):
                kmeans = KMeans(
                    n_clusters=i, init="k-means++", random_state=42
                )  # initializing the KMeans object
                kmeans.fit(data)  # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)
            plt.plot(
                range(1, 11), wcss
            )  # creating the graph between WCSS and the number of clusters
            plt.title("The Elbow Method")
            plt.xlabel("Number of clusters")
            plt.ylabel("WCSS")
            # plt.show()
            create_directories([self.elbow_graph_dir_path])

            plt.savefig(
                os.path.join(self.elbow_graph_dir_path, self.elbow_graph_file_name)
            )  # saving the elbow plot locally
            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(
                range(1, 11), wcss, curve="convex", direction="decreasing"
            )
            logging.info(
                "The optimum number of clusters is: "
                + str(self.kn.knee)
                + " . Exited the elbow_plot method of the KMeansClustering class"
            )
            return self.kn.knee
        except Exception as e:
            logging.info(
                "Exception occured in elbow_plot method of the KMeansClustering class. Exception message:  "
                + str(e)
            )
            logging.info(
                "Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class"
            )
            raise IOError()

    def create_cluster(self, data: pd.DataFrame, number_of_cluster: int) -> None:
        """
        This function will create a kmeans model that will seperate the data into respective cluster
        """
        try:
            logging.info("create_cluster function is called")
            k_means = KMeans(
                n_clusters=number_of_cluster, init="k-means++", random_state=42
            )
            logging.info(
                f"saving the data clustering model to {self.cluster_model_dir_path}"
            )
            create_directories([self.cluster_model_dir_path])

            joblib.dump(
                k_means,
                os.path.join(self.cluster_model_dir_path, self.cluster_model_file_name),
            )
            logging.info("Successfully saved the data clustering model")

            k_means_model = k_means.fit_predict(data)
            data["cluster"] = k_means_model
            logging.info("The cluster value is added to the dataframe")
            return data
        except KeyError as e:
            logging.info(f"Exception occured at create_cluster method :{e}")
        except IOError as ioe:
            logging.info(f"Exception occured at while creating directory :{ioe}")
