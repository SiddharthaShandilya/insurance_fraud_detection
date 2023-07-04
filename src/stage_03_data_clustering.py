import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories, save_to_csv
import random
from src.data_processing.data_clustering import KMeansClustering
from configs.config import ARTIFACTS
from params import COLUMN_NAME_FOR_PREDICTION
import pandas as pd


STAGE = "stage_03_data_clustering"  ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)


def main():
    kmeans_cluster = KMeansClustering()
    logging.info("Instantiating KMeansClustering class")
    preocessed_data_file_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
        ARTIFACTS["LOCAL_DATA_DIR"]["PROCESSED_DATA_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["PROCESSED_DATA_FILE_NAME"],
    )
    clustered_data_dir_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
        ARTIFACTS["LOCAL_DATA_DIR"]["CLUSTERED_DATA_DIR"],
    )
    clustered_data_file_name = os.path.join(
        ARTIFACTS["LOCAL_DATA_DIR"]["CLUSTERED_DATA_FILE_NAME"]
    )
    clustered_data_file_path = os.path.join(
        clustered_data_dir_path, clustered_data_file_name
    )
    logging.info(f"Fetching data from the csv file at {preocessed_data_file_path}")
    data: pd.DataFrame = pd.read_csv(preocessed_data_file_path)
    Y: pd.DataFrame = data[COLUMN_NAME_FOR_PREDICTION]
    X: pd.DataFrame = data.drop(COLUMN_NAME_FOR_PREDICTION, axis=1)
    total_cluster_count = kmeans_cluster.elbow_graph(data=X)
    data_with_cluster: pd.DataFrame = kmeans_cluster.create_cluster(
        data=X, number_of_cluster=total_cluster_count
    )
    data_with_cluster[COLUMN_NAME_FOR_PREDICTION] = Y
    create_directories([clustered_data_dir_path])
    save_to_csv(dataframe=data_with_cluster, file_path=clustered_data_file_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
