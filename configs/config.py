# It contains all the configs required in the project

ARTIFACTS = {
              "ARTIFACTS_DIR": "artifacts",
              "DATABASE_DIR":{
                            "DATABASE":"data",
                            "GOOD_DATA_DIR":"good_data",
                            "BAD_DATA_DIR":"bad_data"
                            },
              "MODEL_DIR":{
                            "TRAINED_MODEL_DIR": "model",
                            "BASE_MODEL_DIR": "base_model",
                            "BASE_MODEL_NAME": "base_model.h5",
                            "UPDATED_BASE_MODEL_NAME": "updated_base_model.h5"
                        },
}
LOG_DIR = {
            "CHECKPOINT_DIR": "checkpoints",
            "BASE_LOG_DIR": "base_model_dir",
            "TENSORBOARD_ROOT_LOG_DIR": "tensorboard_log_dir",
            "CALLBACKS_DIR": "callbacks"
        },
            

SOURCE_DATA_DIR= "../outside_data/insurance_fraud_data" #
LOCAL_DATA_DIR = "../insurance_fraud_detection/artifacts/data"
VALID_FILE_SCHEMA_PATH = "../insurance_fraud_detection/schema_training.json"
