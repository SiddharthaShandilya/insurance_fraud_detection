import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
import pandas as pd
from configs.config import ARTIFACTS
from params import TARGET_COLUMN_NAME, CLUSTER_COLUMN_NAME, LIST_OF_COLUMNS_FOR_SCALING
from src.data_processing.data_preprocessing import RawDataPreProcessing
from src.model_training.model_training import ModelTraining
from sklearn.model_selection import train_test_split
import joblib

STAGE = "STAGE_04_MODEL_TRAINING"  ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a",
)


def main():
    ## getting the pre_processed_data file path
    clusterd_data_file_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["LOCAL_DATA_DIR_NAME"],
        ARTIFACTS["LOCAL_DATA_DIR"]["CLUSTERED_DATA_DIR"],
        ARTIFACTS["LOCAL_DATA_DIR"]["CLUSTERED_DATA_FILE_NAME"],
    )
    model_dir_path = os.path.join(
        ARTIFACTS["ARTIFACTS_DIR"],
        ARTIFACTS["MODEL_DIR"]["MODEL_DIR_NAME"],
        ARTIFACTS["MODEL_DIR"]["TRAINED_MODEL_DIR"],
    )
    model_training_cls = ModelTraining()
    # reading the data file with clustered columns
    combined_clustered_data = pd.read_csv(clusterd_data_file_path)
    logging.info(
        f" total number of cluster present {combined_clustered_data[CLUSTER_COLUMN_NAME].unique()}"
    )
    logging.info(
        f"Picking all the columns of cluster {values}\n Total data points {combined_clustered_data.shape}"
    )
    for values in combined_clustered_data[CLUSTER_COLUMN_NAME].unique():
        logging.info(f"Model training started for cluster {values}")
        # seperating the values for one cluster
        clustered_data: pd.DataFrame = combined_clustered_data.loc[
            combined_clustered_data[CLUSTER_COLUMN_NAME] == values
        ]
        logging.info(
            f"Picking all the columns of cluster {values}\n Total data points {clustered_data.shape}"
        )
        label = clustered_data[TARGET_COLUMN_NAME]
        feature = clustered_data.drop(
            [TARGET_COLUMN_NAME, CLUSTER_COLUMN_NAME], axis=1
        )  # we don't need cluster column for model training
        # splitting the data into test and train set
        feature_train, feature_test, target_train, target_test = train_test_split(
            feature, label, test_size=0.33, random_state=42
        )
        # scaling the data fields
        feature_train_scaled = RawDataPreProcessing.scale_numerical_columns(
            data=feature_train, columns_for_scaling=LIST_OF_COLUMNS_FOR_SCALING
        )
        feature_test_scaled = RawDataPreProcessing.scale_numerical_columns(
            data=feature_test, columns_for_scaling=LIST_OF_COLUMNS_FOR_SCALING
        )
        best_model_name, best_model = model_training_cls.calculate_best_model(
            feature_train_scaled, feature_test_scaled, target_train, target_test
        )
        # creatin gthe directry before saving the model
        model_cluster_dirpath = os.path.join(model_dir_path, f"model_cluster_{values}")
        create_directories([model_cluster_dirpath])
        trained_model_filename = os.path.join(
            model_dir_path, f"model_cluster_{values}", f"{best_model_name}.h5"
        )
        joblib.dump(best_model, trained_model_filename)
        logging.info(
            f"Model {best_model_name} succesfully trained for cluster {values} and stroed at {trained_model_filename}"
        )


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
