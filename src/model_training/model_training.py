import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score
from params import XGBOOST_HYPER_PARAMS, SVM_HYPER_PARAMS
import logging
import mlflow

class ModelTraining:
    """
    This class contain all the functions required for a successful training of model
    """

    def best_params_for_xgboost(
        self, fetaure_columns: pd.DataFrame, target_columns: pd.DataFrame
    ):
        """
        Method Name: best_params_for_xgboost
        Description: get the parameters for XGBoost Algorithm which give the best accuracy.
                        Use Hyper Parameter Tuning.
        Output: The model with the best parameters
        On Failure: Raise Exception

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        """
        logging.info("best_params_for_xgboost function is called")
        xgbr = xgb.XGBRegressor(seed=20)
        best_xgb_model = RandomizedSearchCV(
            estimator=xgbr,
            param_distributions=XGBOOST_HYPER_PARAMS,
            scoring="neg_mean_squared_error",
            n_iter=50,
            verbose=1,
        )
        best_xgb_model.fit(fetaure_columns, target_columns)
        logging.info(
            f"Hyper Parameter tuning for XGBoost is called, best params found is {best_xgb_model.best_params_} \n with best score of {best_xgb_model.best_score_}"
        )
        return best_xgb_model

    def best_params_for_svm(
        self, fetaure_columns: pd.DataFrame, target_columns: pd.DataFrame
    ):
        """
        Method Name: best_params_for_svm
        Description: get the parameters for the SVM Algorithm which give the best accuracy.
                     Use Hyper Parameter Tuning.
        Output: The model with the best parameters
        On Failure: Raise Exception

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None

        """
        logging.info("best_params_for_svm function is called")
        xgbr = xgb.XGBRegressor(seed=20)
        best_svm_model = RandomizedSearchCV(
            estimator=xgbr,
            param_distributions=SVM_HYPER_PARAMS,
            scoring="neg_mean_squared_error",
            n_iter=50,
            verbose=1,
        )
        best_svm_model.fit(fetaure_columns, target_columns)
        logging.info(
            f"Hyper Parameter tuning for SVM is called, best params found is {best_svm_model.best_params_} \n with best score of {best_svm_model.best_score_}"
        )
        return best_svm_model

    def calculate_best_model(
        self, feature_train, feature_test, target_train, target_test
    ):
        """
        Method Name: calculate_best_model
        Description: Find out the Model which has the best AUC score.
        Output: The best model name and the model object
        On Failure: Raise Exception

        Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        """
        logging.info("calculate_best_model function is called")
        try:
            with mlflow.start_run():
                xgboost = self.best_params_for_xgboost(feature_train, target_train)
                mlflow.log_params(xgboost.best_params_)
                mlflow.log_metric("Best Score for xg_boost on trained data",xgboost.best_score_)
                prediction_xgboost = xgboost.best_estimator_.predict(
                    feature_test
                )  # Predictions using the XGBoost Model

                if (
                    len(target_test.unique()) == 1
                ):  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                    xgboost_score = accuracy_score(target_test, prediction_xgboost)
                    logging.info("Accuracy for XGBoost:" + str(xgboost_score))  # Log AUC
                else:
                    xgboost_score = roc_auc_score(
                        target_test, prediction_xgboost
                    )  # AUC for XGBoost
                    logging.info("AUC for XGBoost:" + str(xgboost_score))  # Log AUC
                # storign the new score in mlflow
                mlflow.log_metric("AUC Score for XG_Boost", xgboost_score)
                ########### create best model for Random Forest ###########
                svm = self.best_params_for_svm(feature_train, target_train)
                mlflow.log_params(xgboost.best_params_)
                mlflow.log_metric("Best Score for SVM on trained data",xgboost.best_score_)
                prediction_svm = svm.best_estimator_.predict(
                    feature_test
                )  # prediction using the SVM Algorithm

                if (
                    len(target_test.unique()) == 1
                ):  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                    svm_score = accuracy_score(target_test, prediction_svm)
                    logging.info("Accuracy for SVM:" + str(svm_score))
                else:
                    svm_score = roc_auc_score(
                        target_test, prediction_svm
                    )  # AUC for Random Forest
                    logging.info("AUC for SVM:" + str(svm_score))
                mlflow.log_metric("AUC Score for SVM", svm_score)
                # comparing the two models
                if svm_score < xgboost_score:
                    return "XGBoost", xgboost.best_estimator_
                else:
                    return "SVM", svm.best_estimator_

        except Exception as e:
            logging.info(
                "Exception occured in get_best_model method of the Model_Finder class. Exception message:  "
                + str(e)
            )
            logging.info(
                "Model Selection Failed. Exited the get_best_model method of the Model_Finder class"
            )
            raise Exception()
