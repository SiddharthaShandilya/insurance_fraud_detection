# It contains all the configs required in the project

ARTIFACTS = {
    "ARTIFACTS_DIR": "artifacts",
    "DATABASE_DIR": {
        "SQL_DATABASE_DIR": "sql_data_dir",
        "SQL_TRAINING_DATABASE_NAME": "Insurance_fraud_validated_data_db",
        "SQL_TRAINING_VALIDATED_DATA_TABLE_NAME": "Validated_Raw_Data",
        "SQL_TRAINING_PROCESSED_DATA_TABLE_NAME": "Processed_Raw_Data",
    },
    "LOCAL_DATA_DIR": {
        "LOCAL_DATA_DIR_NAME": "local_data_dir",
        "VALIDATED_DATA_DIR": "valid_data",
        "BAD_DATA_DIR": "bad_data",
        "PROCESSED_DATA_DIR": "processed_data",
        "CLUSTERED_DATA_DIR": "clustered_data",
        "TRAINING_ARCHIVE_BAD_DATA_DIR": "Training_archive_bad_data",
        "VALIDATED_DATA_FILE_NAME": "model_training_validated_data_file.csv",
        "PROCESSED_DATA_FILE_NAME": "model_training_processed_data_file.csv",
        "CLUSTERED_DATA_FILE_NAME": "model_training_clustered_data_file.csv",
        "BAD_DATA_FILE_NAME": "model_training_validated_data_file.csv",
    },
    "GRAPHS_DIR": {
        "GRAPH_DIR_NAME": "graphs_dir",
        "ELBOW_GRAPH": "elbow_plot_cluster.png",
    },
    "CLUSTER_DIR": {"CLUSTER_DIR_NAME": "cluster_data_dir"},
    "MODEL_DIR": {
        "MODEL_DIR_NAME": "model_dir",
        "DATA_CLUSTERING_MODEL_DIR_NAME": "data_clustering_model",
        "DATA_CLUSTERING_MODEL_NAME": "k_means_model.h5",
        "TRAINED_MODEL_DIR": "prediction_model_dir",
    },
}

SOURCE_DATA_DIR = "../outside_data/insurance_fraud_data"  #
LOCAL_DATA_DIR = "../insurance_fraud_detection/artifacts/data"
VALID_FILE_SCHEMA_PATH = "../insurance_fraud_detection/schema_training.json"
