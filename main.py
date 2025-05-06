
from src.components import data_ingestion
from src.components import model_training
from src.components import data_transformation

# if __name__ == "__main__":
#     obj = data_ingestion.DataIngestion()
#     train_data, test_data = obj.initiate_data_ingestion()
#     print(train_data, test_data)



if __name__ == "__main__":
    data_transformer = data_transformation.DataTransformation()
    train_arr, test_arr, preprocessor_file_path = data_transformer.initiate_data_transformation(train_path="artifacts/train.csv", test_path="artifacts/test.csv")

    trainer = model_training.ModelTraining()
    best_r2 = trainer.initiate_model_training(train_arr, test_arr)
    print(best_r2)
