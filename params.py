# This contains params to be used by the stages to train or predict
INPUT_FILE_NAME_REGEX = "['fraudDetection']+['\_'']+[\d_]+[\d]+\.csv"
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

COLUMN_NAME_FOR_PREDICTION = "fraud_reported_1" # after one hot encoding the value column name chnage to fraud_reported_1
