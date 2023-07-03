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
        "TRAINING_ARCHIVE_BAD_DATA_DIR": "Training_archive_bad_data",
        "VALIDATED_DATA_FILE_NAME": "model_training_validated_data_file.csv",
        "PROCESSED_DATA_FILE_NAME": "model_training_processed_data_file.csv",
        "BAD_DATA_FILE_NAME": "model_training_validated_data_file.csv",
    },
    "GRAPHS_DIR": {
        "GRAPH_DIR_NAME": "graphs_dir",
        "ELBOW_GRAPH": " elbow_plot_cluster.png",
    },
    "CLUSTER_DIR": {"CLUSTER_DIR_NAME": "cluster_data_dir"},
    "MODEL_DIR": {
        "TRAINED_MODEL_DIR": "model",
        "BASE_MODEL_DIR": "base_model",
        "BASE_MODEL_NAME": "base_model.h5",
        "UPDATED_BASE_MODEL_NAME": "updated_base_model.h5",
    },
}
LOG_DIR = (
    {
        "CHECKPOINT_DIR": "checkpoints",
        "BASE_LOG_DIR": "base_model_dir",
        "TENSORBOARD_ROOT_LOG_DIR": "tensorboard_log_dir",
        "CALLBACKS_DIR": "callbacks",
    },
)


SOURCE_DATA_DIR = "../outside_data/insurance_fraud_data"  #
LOCAL_DATA_DIR = "../insurance_fraud_detection/artifacts/data"
VALID_FILE_SCHEMA_PATH = "../insurance_fraud_detection/schema_training.json"

COLUMNS_TO_IGNORE_FOR_MODEL_TRAINING = [
    "policy_number",
    "policy_bind_date",
    "policy_state",
    "insured_zip",
    "incident_location",
    "incident_date",
    "incident_state",
    "incident_city",
    "insured_hobbies",
    "auto_make",
    "auto_model",
    "auto_year",
]
COLUMNS_TO_IMPUTE_FOR_MODEL_TRAINING = [
    "collision_type",
    "property_damage",
    "police_report_available",
]
COLUMNS_TO_ENCODE_FOR_MODEL_TRAINING = [
    "policy_csl",
    "insured_education_level",
    "incident_severity",
    "insured_sex",
    "property_damage",
    "police_report_available",
    "fraud_reported",
]

MAPPING_CATEGORICAL_COLUMNS = {
    "policy_csl": {"100/300": 1, "250/500": 2.5, "500/1000": 5},
    "insured_education_level": {
        "JD": 1,
        "High School": 2,
        "College": 3,
        "Masters": 4,
        "Associate": 5,
        "MD": 6,
        "PhD": 7,
    },
    "incident_severity": {
        "Trivial Damage": 1,
        "Minor Damage": 2,
        "Major Damage": 3,
        "Total Loss": 4,
    },
    "insured_sex": {"FEMALE": 0, "MALE": 1},
    "property_damage": {"NO": 0, "YES": 1},
    "police_report_available": {"NO": 0, "YES": 1},
    "fraud_reported": {"N": 0, "Y": 1},
}
