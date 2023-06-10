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
