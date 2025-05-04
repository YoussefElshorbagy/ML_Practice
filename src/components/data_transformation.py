import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.misc.exceptions import CustomException
from src.misc.logger import logging
from src.misc.utils import save_object
from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
    preprocessor_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):      ## Seperate Categorical columns from Numerical columns and prepare the transformation pipeline for each, respectively
        ''' 
        This function is responsible for data tranformation

        '''

        logging.info("Creating Data Transformation Object")

        try:
            numerical_columns = [
                'writing_score', 
                'reading_score'
                ]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("StandardScaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("OneHotEncoded", OneHotEncoder()),
                    ("StandardScaler", StandardScaler(with_mean=False))
                ]
            )

            preprocessing_obj = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessing_obj

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformation(self, train_path, test_path):
        try:

            logging.info("Fetching training and testing data")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Fetched training and testing data")
            logging.info("Fetching preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()                                                   ## Create the preprocessing object

            logging.info("Fetched preprocessing object")

            dependent_feature = "math_score"

            independent_features_train_df = train_df.drop(dependent_feature, axis=1)
            dependent_features_train_df = train_df[dependent_feature]                                                ## Split the independent and dependent features

            independent_features_test_df = test_df.drop(dependent_feature, axis=1)
            dependent_features_test_df = test_df[dependent_feature]

            logging.info("Applying preprocessor object on training and testing sets")

            independent_features_train_arr = preprocessing_obj.fit_transform(independent_features_train_df)         ## Apply the preprocessing obejct on the data
            independent_features_test_arr = preprocessing_obj.transform(independent_features_test_df)

            train_arr = np.c_[independent_features_train_arr, np.array(dependent_features_train_df)]                ## Recombine Transformed Independent Features with the Output Feature
            test_arr = np.c_[independent_features_test_arr, np.array(dependent_features_test_df)]

            save_object(
                file_path = self.data_transformation_config.preprocessor_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)