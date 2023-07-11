import numpy as np

# This contains params to be used by the stages to train or predict
INPUT_FILE_NAME_REGEX = "['fraudDetection']+['\_'']+[\d_]+[\d]+\.csv"
TARGET_COLUMN_NAME = "fraud_reported_1"  # after one hot encoding the value column name chnage to fraud_reported_1
CLUSTER_COLUMN_NAME = "cluster"
# list of columns where scaling is needed
LIST_OF_COLUMNS_FOR_SCALING = [
    "months_as_customer",
    "policy_deductable",
    "umbrella_limit",
    "capital-gains",
    "capital-loss",
    "incident_hour_of_the_day",
    "number_of_vehicles_involved",
    "bodily_injuries",
    "witnesses",
    "injury_claim",
    "property_claim",
    "vehicle_claim",
]
# list of columns with string datatype variables [ DATA TRANSFORMATION  ]
COLUMNS_WITH_STRING_DATATYPE = [
    "policy_bind_date",
    "policy_state",
    "policy_csl",
    "insured_sex",
    "insured_education_level",
    "insured_occupation",
    "insured_hobbies",
    "insured_relationship",
    "incident_state",
    "incident_date",
    "incident_type",
    "collision_type",
    "incident_severity",
    "authorities_contacted",
    "incident_city",
    "incident_location",
    "property_damage",
    "police_report_available",
    "auto_make",
    "auto_model",
    "fraud_reported",
]


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
    "age",
    "total_claim_amount",
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

# PARAMS FOR HYPER_PARAMETER_TUNING

SVM_HYPER_PARAMS = {
    "kernel": ["rbf", "sigmoid"],
    "C": [0.1, 0.5, 1.0],
    "random_state": [0, 100, 200, 300],
}

XGBOOST_HYPER_PARAMS = {
    "max_depth": [3, 5, 6, 10, 15, 20],
    "learning_rate": [0.01, 0.1, 0.2, 0.3, 0.4, 0.5],
    "subsample": [0.5, 0.6, 0.7, 0.8, 0.9],
    "colsample_bytree": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "colsample_bylevel": [0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    "n_estimators": [100, 200, 300, 400, 450, 500, 540, 580, 600],
}
