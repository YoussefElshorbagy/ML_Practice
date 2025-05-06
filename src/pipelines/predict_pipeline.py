import os
import sys
import pandas as pd
from src.misc.exceptions import CustomException
from src.misc.logger import logging
from src.misc.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
        
    def predict(self, features):
        try:
            
            model_path = os.path.join('artifacts', 'model.pkl')
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')

            logging.info("Fetching model")
            model = load_object(model_path)
            logging.info("Fetching Preprocessor")
            preprocessor = load_object(preprocessor_path)
            logging.info("Fetched model and preprocessor")

            print("DEBUG!!!!!!!!!!!")

            logging.info("Transforming input data and predicting...")
            print('HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print(features)
            scaled_data = preprocessor.transform(features)
            result = model.predict(scaled_data)
            logging.info(f"Transformed data and predicted: {result}")

            return result

        except Exception as e:
            raise CustomException(e, sys)



class CustomData:
    def __init__(
        self, 
        gender: str, 
        race_ethnicity: str, 
        parental_level_of_education: str,
        lunch:str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):
        
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score
        

    def get_input_as_df(self):
        try:
            
            logging.info("Converting input data to dataframe")

            input_data_dict ={
                'gender': [self.gender],
                'race_ethnicity': [self.race_ethnicity],
                'parental_level_of_education': [self.parental_level_of_education],
                'lunch': [self.lunch],
                'test_preparation_course': [self.test_preparation_course],
                'reading_score': [self.reading_score],
                'writing_score': [self.writing_score],
            }

            return pd.DataFrame(input_data_dict)
        
        except Exception as e:
            raise CustomException(e, sys)


        