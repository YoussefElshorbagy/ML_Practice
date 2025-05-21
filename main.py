
# from src.components import data_ingestion
# from src.components import model_training
# from src.components import data_transformation

# # if __name__ == "__main__":
# #     obj = data_ingestion.DataIngestion()
# #     train_data, test_data = obj.initiate_data_ingestion()
# #     print(train_data, test_data)



# if __name__ == "__main__":
#     data_transformer = data_transformation.DataTransformation()
#     train_arr, test_arr, preprocessor_file_path = data_transformer.initiate_data_transformation(train_path="artifacts/train.csv", test_path="artifacts/test.csv")

#     trainer = model_training.ModelTraining()
#     best_r2 = trainer.initiate_model_training(train_arr, test_arr)
#     print(best_r2)


import sys
from src.misc.exceptions import CustomException
from src.misc.logger import logging
from src.pipelines.predict_pipeline import PredictPipeline, CustomData
import streamlit as st
import pandas as pd

try:
    df = pd.read_csv('artifacts/train.csv')

    print(df['gender'].unique())

    st.title('Grade Prediction')

    # gender = st.selectbox('Gender', ['male', 'female'])
    # race_ethnicity = st.selectbox('Ethnicity', ['group A', 'group B', 'group C', 'group D'])
    # parental_level_of_education = st.selectbox('Parental Level of Education', ["high school", "some college", "associate's degree", "master's degree"])
    # lunch = st.selectbox('Lunch', ['standard', 'free/reduced'])
    # test_preparation_course = st.selectbox('Test Preparation Course', ['none', 'completed'])
    # reading_score = st.number_input('Reading Score')
    # writing_score = st.number_input('Writing Score')

    gender = st.selectbox('Gender', df['gender'].unique())
    race_ethnicity = st.selectbox('Ethnicity', df['race_ethnicity'].unique())
    parental_level_of_education = st.selectbox('Parental Level of Education', df['parental_level_of_education'].unique())
    lunch = st.selectbox('Lunch', df['lunch'].unique())
    test_preparation_course = st.selectbox('Test Preparation Course', df['test_preparation_course'].unique())
    reading_score = float(st.number_input('Reading Score'))
    writing_score = float(st.number_input('Writing Score'))

    input_data = CustomData(
        gender=gender,
        race_ethnicity=race_ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score
    )

    dataframe = input_data.get_input_as_df()
    predict_pipeline = PredictPipeline()
    result = predict_pipeline.predict(dataframe)[0]

    st.write(f'Predicted Math score is: {result}')

except Exception as e:
    raise CustomException(e, sys)

